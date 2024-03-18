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
정작 중요한 sbatch 실험 작업들이 리소스를 못 받아서 오래 기다리는 현상을 방지하기 위함입니다.

아래 표를 통해서 GPU 사용량 제한을 확인하고,  
sbatch/srun을 통해 자원을 할당 받을 때 참고하세요. (예: 서버5는 gpu 3개 비어 있으니까 4개 신청하면 기다리겠네)

|Name | MaxTRESPerNode | MinTRES |  DefaultTime |  MaxTime |  MaxMemPerNode |
|------|:------|:------|:------|:------|:------|
|srun  |   gres/gpu=2  |  gres/gpu=1 | 1 day | 1 day | 128G |
|sbatch  |   gres/gpu=4 |   gres/gpu=1 | 2 days | 7 days | 128G |

### Disk 사용량 제한

개인별 디스크 사용량 제한량은 대략 `디스크 용량/15` 정도라고 보면 됩니다.

데이터셋 업로드 전용 계정 `data` 가 각 서버별로 제공 될 예정입니다.  
해당 계정으로는 `/data` 아래의 디렉토리만 접근 가능하고,  
`/data` 및 하위 디렉토리는 모든 사람들이 접근 가능합니다.  