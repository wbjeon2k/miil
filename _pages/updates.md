---
title: Update Records
author: Woongbae Jeon
date: 2024-04-17
category: Jekyll
layout: post
---

#### UPD 20250512

- AIGS Cluster 사용 방법 추가

#### UPD 20250429

- readme.md 수정
- restrictions.md 디스크 별 quota 용량 최신화
- 기타 추가 내용 작성 및 수정

#### UPD 20240904

- workstation 관련 내용 FAQ에 추가

#### UPD 20240630

- nfs1, nfs2 추가
  - nfs1, nfs2가 추가 되었습니다.
  - 모든 컴퓨팅 노드에서 접근 가능합니다.
  - 자세한 정보는 왼쪽 'list of NFSs' 참조

- workstation 1,2,3 추가
  - workstation 들이 전부 추가 되었습니다.
  - 기본적으로 2일, 최대 3일 이용 가능합니다.
  - 일단은 한 번에 한 사람만 쓸 수 있도록 하였습니다.


#### UPD 20240625

- server5, server6 추가
  - 서버 5,6이 Slurm cluster에 추가 되었습니다.
  - 이로서 모든 서버들이 Slurm 관리하에 통합 되었습니다.

- RAM 증설 실패
  - 업체와의 소통 오해로 RAM 발주를 다시 할 예정입니다.

- TODO:
  - NFS가 총 3개, 전체 용량으로는 도합 7TB가 추가 될 예정입니다.
  - 워크스테이션의 1.8TB SSD 1EA
  - 서버5의 1.8TB SSD 1EA ( RAM과 함께 구입 )
  - 서버6의 3.5TB SSD 1EA
  - 이를 통해서 서버 로컬 디스크 수요를 많이 줄일 수 있을것으로 예상됩니다.
  - 도합 7TB지만, 개별 디스크 용량은 이보다 작다는 것을 참고해주시면 감사하겠습니다.

#### UPD 20240613

**Major update**

- GPU backdoor prevention
  - Slurm을 통해 할당받지 않은 gpu를 사용하는 경로들을 (상당수) 막았습니다.
  - ConstraintDevices: `cgroup.conf` 추가, `nvidia-smi` 시 할당 받은 개수만큼만 표시
  - vscode-server: vscode-server를 통해서 remote session 만들면 `/etc/profile.d` 가 우회되는 현상 있었음. 수동으로 vscode-server session들을 cgroup 이동.
  - manual counting: Slurm-allocated numbers 와 실제 사용중인 개수가 많이 차이나면 rogue 프로세스 종료. `srun` 할당 후 gpu 유휴중인 경우 고려하였음. PID, Parent PID, Grand Parent PID 에서 slurm spawn 검출되지 않았는데 gpu 접근시 종료.

- TODO : Incoming updates
  - 6월 말 서버 4,5,6 RAM 증설, 서버4 disk 증설
  - 서버 5,6 slurm cluster 통합
  - 서버 5,6 백업 공지
  - 전체 의견 수렴 (단체 미팅때?)
  - 워크스테이션 cluster 추가
  - 워크스테이션2에 NFS 추가

##### UPD 20240418

- 기본 할당되는 CPU의 양이 1개밖에 안되는거 fix
- 사용가능한 자원 조회 페이지 업데이트
- UPD 페이지 업데이트
- Restriction 페이지 업데이트

##### UPD 20240419

- FAQ update

##### UPD 20240422

- 사용 예시 추가
- FAQ update

##### UPD 20240423

- 서버3 GPU 할당 오류 해결
- list-of-gpus 업데이트

##### UPD 20240508

- 서버4 개장
- list-of-gpus 업데이트
- MaxTrexPerUser gres/gpu=12 조정

##### UPD 202405014

- restrictions cpu 개수 내용 업데이트
- 최대 실행 가능 job 개수 6개로 수정

##### UPD 20240515

- `CUDA_VISIBLE_DEVICE`를 srun/sbatch 에서 override 해서 할당받지 않은 gpu를 사용할 수 있음
  <br> reported by 태환,위범
- TaskProlog, cgroup, read-only env var 등 을 활용하여 해결할 것으로 예상됨