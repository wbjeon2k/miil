---
title: (Expected) FAQ
author: Woongbae Jeon
date: 2024-03-16
layout: post
---

### Q. Slurm은 왜 쓰나요?

해당 문서 참조 바랍니다. [PDF](https://github.com/wbjeon2k/miil/blob/master/slurm_introduction.pdf)

<!--[1]:{{ wbjeon2k.github.io/miil }}/miil/slurm_introduction.pdf-->

### Q. GPU type을 여러개 사용하고 싶습니다

만약 gpu 4개를 쓴다면,  
`--gres=gpu:A8000:3, gpu:RTX3090:1` 과 같은 형태로 배정받을 수 있습니다.  

### Q. GPU를 번호별로 배정 받을 수 있나요?

*UPD 20250429*  

번호를 지정하여 배당을 받을수는 없습니다.  

예를 들어, `Q8000`이 `0~7` 까지 있는데 4개를 배정받는다 가정한다면,  
Slurm은 해당 8개 중에서 4개를 *아무거나* 배정해서 줍니다.  
보통은 `0,1,2,3` 식으로 배정을 하지만, `0,2,3,7` 식으로 배정을 할 수도 있습니다.

또는, 실제로 사용하는 GPU는 `0,2,3,7` 이지만  
`CUDA_VISIBLE_DEVICES=0,1,2,3` 으로 새로 mapping이 **됩니다.**.  
(`CUDA_VISIBLE_DEVICES`는 envirionment variable 이니까 충분히 가능.)

따라서 할당을 받은 후에 `$CUDA_VISIBLE_DEVICES` 를 확인하고,  
거기에 맞춰서 GPU device를 사용 해야합니다.

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

    asdf 기타등등
    ```

CPU/GPU/Mem 중 하나라도 최대 사용량 OR 현재 배정받을 수 있는 양을 초과한다면  
자리가 빌 때 까지 기다리게 됩니다. 배정 가능한 양을 [여기](https://wbjeon2k.github.io/miil/pages/resource-access/)를 읽어보고 확인합시다.

### Q. nvidia-smi, nvcc 깔고 싶어요

nvcc(Cuda Toolkit), nvidia-smi 설치는 필요 없습니다.  
PyTorch가 cuda toolkit 버전에 맞춰서 컴파일 돼서 나오기 때문에,  
로컬에서 `nvcc -V` 안돼도 쓰는데에 전혀 문제가 없습니다.  

자세한 내용은 옆에 링크들을 통해서 알아봅시다. [Ref1](https://www.reddit.com/r/pytorch/comments/13siy1d/confused_about_when_to_manually_install_cuda_for/) [Ref2](https://discuss.pytorch.org/t/is-nvidia-driver-already-included-cuda-and-cuda-toolkit/184411/2)

### Q. srun으로 배정을 받으면 알림이 오나요?

아니요, 알림을 보내는 시스템이 없습니다. 수시로 확인 해야합니다.

### Q. --nodes=1 에서 개수를 더 늘릴 수 있나요?

*UPD20240630: multi-node multi-gpu training이 가능해지면 늘릴 수 있습니다.*
*UPD20250429: nfs들이 추가됨에 따라 아래 내용을 일부 수정.*

현재 MIIL Cluster 환경에서는 `--nodes=1` 의 사용이 권장됩니다.  

NFS들을 통해서 모든 computing node에서 접속 가능한 디스크는 있지만,  
multi-node training에 필요한 통신이 제대로 되는지는 확인 된 바 없습니다.  

### Q. Disk Quota를 알고 싶어요

![quota_example](/miil/assets/quota_example.png)

사용하고 있는 서버로 이동해서, `quota` 를 실행하면 디렉토리 별 quota 내역이 나옵니다.

NFS에 대해서는, NFS가 mount된 노드에서 quota 실행시 조회 가능합니다.  
(*e.g. /nfs1 quota 조회 하려면 workstation2 에서 quota 실행.*)

각 디스크별 quota 상세 용량은 별도 문서 참조.

### Q. Workstation을 사용하고 싶어요

현재 `workstation[1-3]` 은 Slurm의 `workstation` 파티션에**만** 배정 되어 있습니다.

워크스테이션은 한 번에 한 사람만 쓸 수 있도록 설정 하였기 때문입니다.

`-p <partition_name>` 을 통해서 적절하게 선택하면 됩니다.

```bash
# srun example
srun -p workstation --gres=gpu:1 -w workstation1 -J example --pty /bin/bash # correct usage
srun -p srun --gres=gpu:1 -w workstation1 -J example --pty /bin/bash # incorrect. workstation not in srun partition
```