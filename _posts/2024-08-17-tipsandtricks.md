---
title: Tips and Tricks
author: Woongbae Jeon
date: 2024-08-17
layout: post
---

꿀팁들을 정리하는 곳 입니다.

### Enable Pytorch DDP in server4,5

*@jjlee*  

```bash
export NCCL_P2P_DISABLE=1
```

[Pytorch DDP](https://pytorch.org/tutorials/beginner/ddp_series_intro.html) 가 서버 4,5 에서만 동작하지 않는 경우가 있습니다.  

이 때는 `NCCL_P2P_DISABLE=1` 으로 환경변수를 바꿔주면 됩니다. [추가정보](https://github.com/NVIDIA/nccl/issues/570)

### Using CPU taskset (with sbatch)

*@hwan*

[taskset](https://man7.org/linux/man-pages/man1/taskset.1.html) 을 통해서 각 command 별로 cpu를 배정하는 예시입니다.  

sbatch/srun 을 통해서 cpu를 배정 받게되면,  
`taskset -cp` 를 통해서 해당 node 의 physical cpu id를 아래 예시처럼 확인 할 수 있습니다.  

![tasksetcp](/assets/tasksetcp.png)

위 예시와 같이, 8개 cpu들이 연속적인 id로 배정되지 않습니다.

따라서 `expand_cores` 를 통해 list 형태로 바꿔주고,  
`build_cpu_lists` 를 통해 묶음들을 만들어 주면 됩니다.

```bash
#!/bin/bash
# Thanks to @hwan for sharing!
# Job name:
#SBATCH --job-name=Distill
#
# Partition:
#SBATCH --partition=sbatch
#
# Request one node:
#SBATCH --nodes=1
#   
# Specify the node's name
#SBATCH --nodelist=server1
#SBATCH --output=Log-cpu-checkout
#SBATCH --gres=gpu:2
#SBATCH --cpus-per-gpu=8
#SBATCH --time=02-00
# !SBATCH 제출시 GPU 최소 1개 이상 신청 해야 접수됨!
#
## Command(s) to run (example):
export PATH="/home/hwan/miniconda3/bin:$PATH"
export NCCL_P2P_DISABLE=1

source ~/.bashrc
# source activate distill
#!/bin/bash

# 🧠 설정: N개씩 나누기
N=4  # 예: 4개씩 → 필요하면 외부 인자 $1 로도 받을 수 있음

# 현재 bash 프로세스의 CPU affinity 가져오기
CPU_AFFINITY=$(taskset -cp $$ | awk -F': ' '{print $2}')
echo "Current CPU affinity: $CPU_AFFINITY"

# CPU 범위 확장 함수 (e.g., "0-3,8" → 0 1 2 3 8)
expand_cores() {
    local range=$1
    local cores=()
    IFS=',' read -ra parts <<< "$range"
    for part in "${parts[@]}"; do
        if [[ "$part" == *"-"* ]]; then
            start=${part%-*}
            end=${part#*-}
            for ((i=start; i<=end; i++)); do
                cores+=("$i")
            done
        else
            cores+=("$part")
        fi
    done
    echo "${cores[@]}"
}

# N개씩 나누어 CPU_LISTS 배열 생성
build_cpu_lists() {
    local n=$1
    shift
    local -a cores=("$@")
    local total=${#cores[@]}
    local i=0
    CPU_LISTS=()
    while (( i < total )); do
        chunk=("${cores[@]:i:n}")
        cpu_list=$(IFS=','; echo "${chunk[*]}")
        CPU_LISTS+=("$cpu_list")
        ((i += n))
    done
}

# 실행
ALL_CORES=$(expand_cores "$CPU_AFFINITY")
read -a CORE_ARRAY <<< "$ALL_CORES"
build_cpu_lists "$N" "${CORE_ARRAY[@]}"

# 결과 확인 (echo만)
for i in "${!CPU_LISTS[@]}"; do
    echo "taskset --cpu-list ${CPU_LISTS[$i]} python main.py"
done

```