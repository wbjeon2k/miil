---
title: (Expected) FAQ
author: Woongbae Jeon
date: 2024-03-16
layout: post
---

### Q. sbatch 작업을 srun 파티션에 제출하거나 vice versa의 경우 어떻게 되나요?

srun 작업을 sbatch에 제출하면 제출이 즉시 거부되거나, 제출 되더라도 3분 이내에 취소됩니다.  
해당 작업들이 취소 되었다고 알림이 가지는 않습니다.

### Q. 기본으로 배정되는 CPU/Mem 보다 더 많이 할당하고 싶어요

- `srun` 을 실행시킬때, `--cpus-per-gpu=<N>`, `--gres=gpu:<N>`, `--mem=<N>GB` 을 통해 배정받고자 하는 자원의 개수를 직접 지정하여 늘리면 됩니다.
- `sbatch` 스크립트에 `--cpus-per-gpu=<ncpus>`, `--gres=<list>`, `--mem=<size>` 를 수정합니다.
```bash
#!/bin/bash
#예시
#SBATCH --job-name=jobfromjwb
#SBATCH --partition=sbatch
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --nodelist=server1
#SBATCH --output=sbatch.out
#할당 자원 개수를 직접 정합니다.
#SBATCH --cpus-per-gpu=<ncpus>
#SBATCH --gres=<list>
#SBATCH --mem=<size>

~asdf 기타등등~
```

CPU/GPU/Mem 중 하나라도 최대 사용량 OR 현재 배정받을 수 있는 양을 초과한다면  
자리가 빌 때 까지 기다리게 됩니다. 배정 가능한 양을 [여기](https://wbjeon2k.github.io/miil/pages/resource-access/)를 읽어보고 확인합시다.

### Q. srun으로 배정을 받으면 알림이 오나요?

아니요, 알림을 보내는 시스템이 없습니다. 수시로 확인 해야합니다.