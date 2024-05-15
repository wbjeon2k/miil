---
title: Update Records
author: Woongbae Jeon
date: 2024-04-17
category: Jekyll
layout: post
---

#### UPD 20240418

- 기본 할당되는 CPU의 양이 1개밖에 안되는거 fix
- 사용가능한 자원 조회 페이지 업데이트
- UPD 페이지 업데이트
- Restriction 페이지 업데이트

#### UPD 20240419

- FAQ update

#### UPD 20240422

- 사용 예시 추가
- FAQ update

#### UPD 20240423

- 서버3 GPU 할당 오류 해결
- list-of-gpus 업데이트

#### UPD 20240508

- 서버4 개장
- list-of-gpus 업데이트
- MaxTrexPerUser gres/gpu=12 조정

#### UPD 202405014

- restrictions cpu 개수 내용 업데이트
- 최대 실행 가능 job 개수 6개로 수정

#### UPD 20240515

- `CUDA_VISIBLE_DEVICE`를 srun/sbatch 에서 override 해서 할당받지 않은 gpu를 사용할 수 있음
  <br> reported by 태환,위범
- TaskProlog, cgroup, read-only env var 등 을 활용하여 해결할 것으로 예상됨