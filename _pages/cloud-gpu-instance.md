---
title: GPU Instance 신청 안내
author: Woongbae Jeon
date: 2025-08-13
category: Jekyll
layout: post
---

2026.02.12 현재는 접수를 받지 않는 상태입니다.

<!-- #### 신청 링크

**신청 접수 링크** : <https://forms.gle/d82jSnhpe6DHMSY59>  

필히 아래 내용을 정독 후 신청 바랍니다.  
신청 후에는 관리자(@jwb) 에게 슬랙으로 신청 했다고 알려주세요.

#### 가능한 서비스 선정 기준

학과 지침을 간단히 요약하면 아래와 같습니다.  

- **서버가 국내에 있을 것**
- 기업체 클라우드의 경우, [KISA Certified](https://isms.kisa.or.kr/main/csap/issue;jsessionid=D7AAB1FC540E02A7FD60915B740B9E90/) 목록에 있어야 함.
- 연구비 결제가 가능해야함. ( 세부 내용은 생략 )

#### 가능한 서비스 목록

교비 집행 등 비용처리 과정이 전부 정리 된 서비스만 기재됩니다.  

##### 성균관대 HPC 클러스터

- 홈페이지 : <https://supercom.skku.edu/supercom/use.do>
- 주요 특기 사항
  - A100(VRAM 80G)를 0.1개 단위로 신청. (refer to [NVIDIA Multi Instance GPU](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/index.html))
  - 개인별로 신청 후 SKKU HPC에 VPN을 발급받아 접속하여 사용.
  - SKKU HPC 내의 A100 40개를 분배하는 시스템이라서, 대기열이 발생하여 실제 배정까지 시간이 걸릴 수 있음. ( 얼마나 걸리는지는 과거 기록이 없어서 미지수 )
- NVIDIA MIG
  - 0.1개씩 배정한다는 말 자체가 NVIDIA MIG를 지원한다는 의미.
  - 1개의 GPU를 여러개로 쪼개서 사용할 수도 있음.
  - e.g A100 80G 1개를 VRAM 16G 짜리 GPU 5개로 쪼개서 사용 가능
  - 물론 전부 합쳐서 80G VRAM을 통으로 사용할 수도 있음.
- MIG를 쓴다면, 이하 자료 외에도 추가로 사용 방법 자료를 찾아보기를 매우 권장함.
- [Guide1](https://github.com/rh-aiservices-bu/gpu-partitioning-guide), [Guide2](https://massedcompute.com/faq-answers/?question=How%20to%20configure%20NVIDIA%20MIG%20in%20a%20Docker%20container?)
- [필수 서류](https://supercom.skku.edu/supercom/notice.do?mode=view&articleNo=47815&article.offset=0&articleLimit=10) : 비용 계산기로 계산한 비용, 사용 신청서, VPN 신청서
- 신청서 "결제 재원" 은 "**산단 회계(→연구비카드 온라인 결제)**" 로 체크.

##### NHN Cloud

연구비 결제 관련해서 절차 준비중입니다.

##### Others

GCP / AWS "하등급" instance에 대해서는 KISA certified 되었는데,  
해당 "하등급" instance가 정확히 어떤 서비스 인지 GCP / AWS 에서는 조회가 안됨.  
KISA 문의 대기중.  

사용 가능 여부 및 비용처리 정리 되는대로 추가 예정. -->