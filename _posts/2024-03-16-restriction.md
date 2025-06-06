---
title: Resource Restriction
author: Woongbae Jeon
date: 2024-03-16
layout: post
---

### 자원 제한 현황

|Name | 1인당 최대GPU개수 | 서버 당 최대GPU개수 | 최소GPU개수 | 최대 제출가능 작업 | 최대 실행가능 작업 |  
|----|:---|:---|:---|:---|:---|  
|srun    |   gres/gpu=2 | gres/gpu=2 | gres/gpu=1 | 1개 | 1개 |
|sbatch  |   gres/gpu=12 | gres/gpu=4 | gres/gpu=1 | 8개 | 6개 |
|workstation  |  gres/gpu=2 | gres/gpu=2 | gres/gpu=1 | 1개 | 1개 |

|Name | 기본 CPU개수 | 서버당 최대CPU개수 | 1개 작업 최대 cpu | 기본 메모리(MB) | 최대 메모리(MB) | 기본 배정 시간 | 최대 배정 시간|  
|----|:---|:---|:---|:---|:---|:---|:---|
|srun  | 8 per gpu|24|24| 28300(30G)|135000(128G)| 없음| 1440(1day)|
|sbatch| 8 per gpu|64|32| 28300(30G)|135000(128G)| 2880(2days)| 10080(7days)|
|workstation | 8 per gpu|32|32| 28300(30G)|135000(128G)| 2880(2days)| 4320(3days)|

### GPU 사용량 제한

GPU 사용량 제한에는 크게 시간적 제한과 양적 제한이 있습니다.

GPU 사용량 제한은 partition(srun/sbatch) 별로 다르게 책정 되었습니다.  
이는 debugging 등 실시간으로 할당이 필요한 작업을 하기 위한 srun 작업들이 자원을 과도하게 점거해서  
정작 중요한 sbatch 실험 작업들이 리소스를 못 받아서 오래 기다리는 현상(starvation)을 방지하기 위함입니다.

위 표를 통해서 GPU 사용량 제한을 확인하고,  
sbatch/srun을 통해 자원을 할당 받을 때 참고하세요.  
(예: 서버5는 gpu 3개 비어 있으니까 4개 신청하면 기다리겠네)  
(예2: 지금 gpu를 5개 쓰고 있으니까 최대 3개를 더 쓸수 있겠네) 

- 최대 GPU개수(`MaxTRESPerUser`) : 1 사람이 최대로 사용할 수 있는 GPU 개수입니다.
    <br> 모든 `srun` 및 `sbatch` 작업에서 사용되는 gpu 개수를 합쳤을 때 8개를 넘길 수 없습니다.
    <br> `e.g. srun job A 1개, sbatch job B 3개 쓰고 있을 때 / sbatch job C에 최대 4개 가능`
- 서버 당 최대GPU개수(`MaxTRESPerNode`) : 1개의 서버에서 최대로 사용할 수 있는 GPU의 개수입니다.
    <br> `e.g. server2에 GPU 8개 있지만, 최대 4개 사용 가능.`
- 최소GPU개수(`MinTRES`) : 최소로 사용을 해야하는 GPU 개수입니다. 1개로 설정 되어있습니다. <br>
    (i.e. GPU 사용 안하면 Slurm 제출하지 말라는 의미입니다.)
- 최대 실행가능 작업(`MaxJobsPerUser`) : 1 사람이 최대로 실행할 수 있는 작업 개수입니다. `srun`과 `sbatch` 전부 포함입니다.
    <br> `e.g. 제한이 4개라면 srun 1개, sbatch 3개 가능 / sbatch 5개 불가능`
- 최대 제출가능 작업(`MaxSubmitJobsPU`) : 1 사람이 최대로 접수할 수 있는 작업 개수입니다. `srun`과 `sbatch` 전부 포함입니다.
    <br> `e.g. 제한이 8개인데 srun 1개, sbatch 4개 실행 중이라면? sbatch 최대 3개 접수 가능.`

더 자세히 알고싶거나 직접 Slurm 을 통해 확인해보고 싶다면 다음 cmd를 사용하세요.  
`sacctmgr show qos format=name,MaxTRESPerUser,MaxTRESPerNode,MinTRES,MaxJobsPerUser,MaxSubmitJobsPU`

- 기본 배정시간 : `sbatch` 는 2일(2880 mins) 입니다.
- 최대 배정시간 : `sbatch` 는 7일, `srun`은 1일 입니다.
    <br> 최대 배정시간을 넘긴 작업은 자동으로 종료 및 삭제됩니다.
    <br> 너무 큰 실험을 한꺼번에 많이 돌리지 마세요.

### 메모리 제한

위 표에 표시된 메모리 제한은 hard limit이 아닙니다.  
128G를 초과한다고 해서 바로 종료되지 않습니다.  
예를 들어, 128G를 배정 신청 했는데 실제로 128G보다 메모리를 더 쓴다고 즉시 종료되지 않습니다.  
(과도하게 초과시에는 자동으로 종료될 수도 있지만, 테스트를 할 수 없어서 모릅니다.)

마찬가지로, 배정 받은 메모리보다 많이 쓴다고 즉시 종료되지 않습니다.  
예를 들어, 32G를 배정 신청 했는데 실제로 32G보다 더 쓴다고 즉시 종료되지 않습니다.  

다만, 과도하게 사용량보다 적거나 많이 배정받지는 말아주세요.  

- 배정된 메모리 양을 많이 초과해서 쓰면 모든 작업에 메모리 초과가 날 수 있습니다. <br> 배정된 메모리가 남아있어서 작업들이 밀려오는데, 실제 메모리가 부족해서 초과 될 수 있습니다.
- 배정된 메모리보다 너무 적게 쓰면 다른 사람이 못 쓸수도 있습니다.

작업들이 배정받을 메모리가 부족하다면 계속 기다릴수도 있습니다.  
(GPU가 남아도 메모리가 부족해서 새로운 작업이 대기(PD) 상태에 들어갈 수 있음.)  
`python gc.collect()` 등을 활용해서 불필요한 메모리 사용을 줄여봅시다.

### CPU 제한

메모리와 다르게, CPU는 자동으로 사용 개수를 늘리지 않습니다.  
메모리와 마찬가지로, 배정 받을 개수가 부족하면 대기 상태에 들어갑니다.  

- 서버 당 최대 cpu 개수: `max_gpu_per_node`, 한 명의 사용자가 1개 노드에서 사용할 수 있는 gpu 최대 개수. <br>
  예: job1 에서 16개, job2에서 32개 쓰고있다면 job3에서 16개 가능
- 1개 작업 최대 cpu: `max_cpu_per_job`, 어떤 작업이던 최대 사용 가능한 cpu 32개. <br>
  gpu, mem등 다른 리소소들과 전혀 관계 없음.

### Disk 사용량 제한

개인별 디스크 사용량 제한량은 대략 `디스크 용량/10` 정도라고 보면 됩니다.

*required: 반드시 있는 것 / optional: 로컬디스크 상황에 따라 없을수도 있음*

#### /home, /nfs, /data

개인별로 자유롭게 쓸 수 있는 공간입니다.  
디스크 사용량 제한 아래에서는 파일 및 디렉토리 생성이 자유롭습니다.

#### /dataset

*서버 용량에 따라서 없는 경우도 있습니다.*  
*`/dataset` 이 없다면 `/home/<user>` , `nfs` 또는 `/data` 을 용량 제한 내에서 사용 해주세요*  

공통적으로 많이 쓰이는 데이터셋들을 저장하는 디렉토리 입니다.  

ImageNet 등 대용량 데이터셋을 저장할 때,  
제한된 개인별 디스크 사용량을 소모하는것을 방지하기 위해서 별도로 생성되었습니다.  

추가 하고자 하는 데이터셋을 자유롭게 추가해도 좋지만,  
데이터셋이 아닌 개인 파일들 (특히 `*.pth`, `*.npy` 등) 을 저장하는 등 어뷰징 하면 삭제 하겠습니다.

### Quota 현황

각 서버에서 `quota` 실행시 확인할 수 있습니다.

![quota_example](/miil/assets/quota_example.png)

| nodename | path | size(GB) |
|------|------|------:|
|master |  /home | 32G |
|server1 | /home | 45G |
|server1 | /data | 300G |
|server2 | /home | 50G |
|server2 | /data | 600G |
|server2 | /dataset | 0G |
|server3 | /home | 300G |
|server3 | /data | 330G |
|server4 | /home | 400G |
|server5 | /home | 150G |
|server5 | /data | 150G |
|server5 | /nfs2 | 250G |
|server6 | /home | 150G |
|server6 | /data | 150G |
|workstation1 | /home | 60G |
|workstation2 | /home | 60G |
|workstation2 | /nfs1 | 250G |
|workstation3 | /home | 80G |
|workstation3 | /nfs3 | 500G |
|workstation3 | /nfs4 | 500G |
