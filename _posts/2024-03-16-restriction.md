---
title: Resource Restriction
author: Woongbae Jeon
date: 2024-03-16
category: Restriction
layout: post
---

### GPU 사용량 제한

GPU 사용량 제한에는 크게 시간적 제한과 양적 제한이 있습니다.

GPU 사용량 제한은 partition(srun/sbatch) 별로 다르게 책정 되었습니다.  
이는 debugging 등 실시간으로 할당이 필요한 작업을 하기 위한 srun 작업들이 자원을 과도하게 점거해서  
정작 중요한 sbatch 실험 작업들이 리소스를 못 받아서 오래 기다리는 현상(starvation)을 방지하기 위함입니다.

아래 표를 통해서 GPU 사용량 제한을 확인하고,  
sbatch/srun을 통해 자원을 할당 받을 때 참고하세요. (예: 서버5는 gpu 3개 비어 있으니까 4개 신청하면 기다리겠네)

|Name | 최대GPU개수 | 최소GPU개수 |  기본배정시간 |  최대배정시간 |  메모리제한 |
|------|:------|:------|:------|:------|:------|
|srun  |   gres/gpu=2  |  gres/gpu=1 | 1 day | 1 day | 128G |
|sbatch  |   gres/gpu=4 |   gres/gpu=1 | 2 days | 7 days | 128G |

### 메모리 제한

위 표에 표시된 메모리 제한은 hard limit이 아닙니다.  
128G를 초과한다고 해서 바로 종료되지 않습니다.  
다만, 이후에 배정되는 작업들이 들어갈 공간이 부족하다면 계속 기다릴수도 있습니다.  
(GPU가 남아도 메모리가 부족해서 새로운 작업이 대기(PD) 상태에 들어갈 수 있음.)  
`python gc.collect()` 등을 활용해서 불필요한 메모리 사용을 줄여봅시다.

### Disk 사용량 제한

개인별 디스크 사용량 제한량은 대략 `디스크 용량/10` 정도라고 보면 됩니다.

#### /data

개인별로 자유롭게 쓸 수 있는 공간입니다.  
디스크 사용량 제한 아래에서는 파일 및 디렉토리 생성이 자유롭습니다.

#### /dataset (Optional)

공통적으로 많이 쓰이는 데이터셋들을 저장하는 디렉토리 입니다.  

ImageNet 등 대용량 데이터셋을 저장할 때,  
제한된 개인별 디스크 사용량을 소모하는것을 방지하기 위해서 별도로 생성되었습니다.  

추가 하고자 하는 데이터셋을 자유롭게 추가해도 좋지만,  
데이터셋이 아닌 개인 파일들 (특히 `*.pth`, `*.npy` 등) 을 저장하는 등 어뷰징 하면 삭제 하겠습니다.

#### Quota 현황

| nodename | / size,quota | /home size,quota | /data size,quota | /data1 size,quota | /data2 size,quota | data3 size,quota |
|----------|--------|------------|------------|-------------|-------------|------------:|
|server1 | 246G, 20G | 600G, 45G | 1.8T, 300G |
|server2 | 210G, 20G | 630G, 50G | 8.5T, 600G |
|server3 |
|server4 |
|server5 |
|server6 |
|workstation1 | 567G | 344G |
|workstation2 | 567G | 344G |
|workstation3 | 567G | 344G |
