---
title: AIGS Cluster 사용 안내
author: Woongbae Jeon
date: 2025-05-11
category: Jekyll
layout: post
---

#### 신청 링크

**신청 접수 링크** : <https://forms.gle/FwhEvVNzRHbfyjit7>  
**신청 접수 현황** : <https://docs.google.com/spreadsheets/d/1m04x79PqbX0N2pF5luOKsmy3oNTCpzYb6f31e39tTMk/edit?usp=sharing>

클러스터 운영 방침 (by 문영제 선생님) : <https://bit.ly/aigs-inst-notify>

#### UNIST AIGS Cluster

UNIST AIGS에서 제공하는 GPU 클러스터 사용 방법입니다.  
기존에는 개인별로 계정을 발급 받아서 사용했지만,  
2025년 5월 부터 **연구실별로 계정을 발급 받아서** 사용하는 것으로 변경 되었습니다.

또한, 연구실 별로 사용 가능한 토큰을 매 년 발급받는 형식으로 변경 되었습니다.

따라서 연구실 별 별도 관리자가 신청 내역을 취합하고 제출하는 방식으로 변경 되었습니다.  

#### 사용 신청 방법 요약

0. **본 사용 안내 페이지 정독, 사용규칙 준수**
1. 사용 기간, 사용하고자 하는 GPU Type 및 개수 결정
2. **매 주 화요일까지** [신청접수링크](<https://forms.gle/FwhEvVNzRHbfyjit7>) 를 통한 접수
3. Slack 통해서 관리자(2025.05 현재 @jwb) 에게 알림
4. `slurmmaster` 에서 배정받은 pod 접속
5. 풀로드 걸어서 알차게 쓰기

#### AIGS Cluster 현황

- AIGS Cluster는 Kubernetes(k8s) 로 관리됩니다. 따라서 발급받은 각 pod은 Docker container 이며, 가상머신 으로 생각하시면 편합니다.
- Cluster에서 발급받은 `miil` 계정으로 pod 생성후, `slurmmaster` 를 통해서 ssh 포워딩을 제공하고, `slurmmaster` 에서 접속하는 방식으로 사용합니다.
- 3개의 GPGPU 노드가 2개의 스토리지 노드에 연결 되어 있습니다.
  - k8s1(쿠버네티스1) : A100, H200이 있는 고성능 노드.
  - k8s2(쿠버네티스2) : A6000, 3090이 있는 보급형 노드.
  - node1 : A100 8EA 단독 서버 (i.e. 신청시 8개 전부 사용 신청)
  - Data1 : k8s1, node1 이 연결 되어있음.
  - Data2 : k8s2 가 연결 되어있음.
  - 스토리지 노드 별 계정 동기화 / 데이터 동기화는 없음.
- GPUs per node:
  - k8s1 : A100-80G 16EA, H200 0EA (연말에 H200 추가 예정)
  - ~~k8s2 : A6000 14EA, 3090 15EA (6월 중에 사용 가능 예정)~~
  - node1 : A100-80G 8EA, node1 신청시 k8s1 신청 불가능.
- 신청시 (최대)사용 기간
  - k8s1, k8s2 : 1주일
  - node1 단독서버: 2주일
  - 연장 신청을 통해서 이어서 사용 가능.

#### Step by Step

##### 사용 할 Docker Image 준비

- container 는 image를 실행 했을 때 생기는 instance를 의미합니다.
  - e.g. Ubuntu image 파일을 Docker로 실행하면 Ubuntu container(\sim VM) 생성
- Default image가 있어서, 개별로 image를 준비하지 않아도 사용 가능합니다.
- 개별로 image를 준비하면, 실행 환경 준비하는 시간을 단축시킬 수 있기에 권장 하는바 입니다. (아닌 경우도 있음)
- Image build with Dockerfile : 상세 내용은 [외부자료](https://docs.docker.com/get-started/docker-concepts/building-images/) 참조
  - 사용할 apt,pip,conda 패키지들 파악
  - Dockerfile 작성 : 요리의 레시피에 해당.
    - 내가 원하는 세팅을 만들기 위해 필요한 과정 작성
    - e.g. Ubuntu base image에 `xyz` command로 Pytorch부터 깔고...
  - Docker build : dockerfile 레시피대로 Docker가 조리 시작.
    - `--platform` 에서 arm64 / amd64 설정 유의.
  - Push to DockerHub, pod 생성시 pull 하기 위함.
- TL;DR : default image 쓰거나 / dockerhub push 하여 준비

##### 신청 접수 및 배정

- **매주 화요일까지** [신청링크](https://forms.gle/Fw5oNhGS2C2Gd1Me8) 를 통해서 접수
- 배정 결과는 목요일 오후에 관리자에게 전달 됨.
- 관리자는 신청 된 사양대로 pod 준비
- pod 준비 되면 `slurmmaster` 터널링 후 전달.
- 접수 한 개수보다 적게 배정 될 수 있음. (e.g. 4개 신청, 2개 배정)
  - 해당 경우 발생시, **신청 한 사람 모두 1개 이상 배정** 을 우선으로 함.
  - e.g. A가 gpu 2개, B가 gpu 4개 신청 후 최종 2개 배정받음. 이 때 1개씩 분배.
- Emergency 항목 : 배정된 개수가 신청 인원보다 적을 시, 우선적으로 배정 받아야 함을 미리 알리기 위함.
  - e.g. 3명이 신청했는데 gpu 2개 배정 받음. Emergency 체크 한 사람이 있으면 우선 배정 시도.
  - e.g. Emergency 체크 안 한 사람이 2명, 배정된 gpu는 1개. 둘 중 아무나 pass 가능.
  - Emergency 인원이 배정 개수보다 많으면 **당사자들 끼리 협의 후 관리자에게 통보 해주세요.**

##### 실제 사용

- 사용 할 데이터셋이 용량이 크면 미리 관리자에게 연락 및 상의 해야함.
  - 관리자가 `scp` 등 간단한 작업으로 옮길 수 있도록 준비 해야함.
  - `/home/miil` 에 업로드 하면 pod에서 사용 가능.
  - 대형 트래픽 발생으로 정보보안팀 제재시 연구실 계정 전체 차단됨.
- 관리자가 `miil@slurmmaster` 에서 각 pod별로 ssh tunneling.
- 사용자 별로 ssh port 전달.
- 전달 받은 port를 가지고 `slurmmaster` 에서 접속해서 사용.
  - e.g. `ssh -p 8192 root@localhost` 를 `slurmmaster` 에서 실행
  - 추가 포워딩 해서 사용하는 등 기타 사용 방법은 자유
- 초기 pw : `miil@<user_id>`, `user_id`는 연구실 서버 id와 동일.
  - 바꾸고 싶으면 `chpasswd` 사용.
- 접속 후 `/home/miil` 로 이동하여 사용.
  - pod의 `/home/miil` 과 실제 클러스터의 `/home/miil` 이 매핑 되어있음.
  - 따라서 pod 안에서 `/home/miil/asdf.out` 생성시 클러스터 에서도 보임. vice versa.

##### 실제 사용 예시

![step1](/miil/assets/aigscluster/step1.png)

사용자 : 관리자에게 dataset 업로드 요청.  
관리자 : `/home/miil` 아래에 데이터셋 저장.  

![step2](/miil/assets/aigscluster/step2.png)

관리자: pod 생성. 정상적으로 생성 됐는지 확인.

![step3](/miil/assets/aigscluster/step3.png)

관리자: `slurmmaster` 에서 ssh 터널 생성.

![step4](/miil/assets/aigscluster/step4.png)

관리자 : 터널링 된 port 번호 전달  
사용자 : 해당 port로 접속. `ssh -p <port> root@localhost`.

![step5](/miil/assets/aigscluster/step5.png)

사용자 : `/home/miil` 로 이동, 데이터셋 등 파일 사용 가능.  
(step 1 에서 `/dataset` 에 만든 파일이 pod에서 접속 가능한 것을 확인 가능.)  

#### 주의 사항

- 대형 트래픽 발생하여 연구실 계정 페널티 먹는 경우, **문제를 일으킨 사람은 추후 신청에서 불이익이 있을 수 있습니다**.
- (50G 이상의) 데이터셋을 pod에서 다운 받는 경우, 아래 예시와 같이 양식을 작성하여 `unisecurity01@unist.ac.kr` 로 미리 연락 바랍니다.
```
1) 작업자명: OOO(1xx동 x층 xxx-x), 010-0000-0000
2) 작업기간: 202x.MM.DD(x요일)~202x.MM.DD(x요일) 연속 작업
3) 작업 시스템: AI 모델 학습 연구용 GPU 서버, Ubuntu, xx.xx.xx.xx
   (AIGS cluster의 경우 10.0.7.72)
4) 수집대상 (범위): DATASET_NAME
5) 수집정보(데이터): DATASET_INFO, 데이터셋 웹페이지(GH repo 주소도 가능)
6) 작업 목적과 내용: XYZ 연구에 지속적으로 사용 예정
```

- 연구실별 신청 가능한 GPU 개수 : k8s1 8개, k8s2 8개(3090 + A6000)
- 1개의 pod은 1개의 gpu type 사용.
- **!!GPU 할당 실패시 연구실 계정 접속이 차단됨!!**
  - GPU 배정 못 받았는데 클러스터 접속해서 GPU 사용하는걸 막기 위함.
  - 클러스터 운영팀에서 차단하므로 연구실 관리자가 할 수 있는게 없음.
  - 따라서 중요 데이터는 항상 백업을 해야함.
- GPU 할당 개수가 줄어든 경우, 사용중인 container를 삭제 후 재설정 해야함.
  - e.g. GPU 3개 쓰는 pod P1 가정. miil 전체가 2개 할당 받음. P1 삭제후 P2 배정.
  - 미리 조치 하지 않은 경우, 클러스터 측에서 개수를 맞추기 위해서 삭제함.
  
- `Emergency 체크 한 사람 \geq 배정 gpu 개수` 일 때, 당사자들끼리 협의 후 관리자에게 안내 부탁드립니다.

- 