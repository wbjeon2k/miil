---
title: 사용 가능 자원 조회
author: Woongbae Jeon
date: 2024-04-17
category: Jekyll
layout: post
---

사용 가능한 자원을 정확히 알 수 있는 방법입니다.  
<http://10.20.22.87:8888/lab/workspaces/auto-h/tree/check_resource.ipynb>  
위 링크에 있는 `ipynb` 파일에 있는 cmd와 동일합니다.

각 옵션 옆에 붙어있는 숫자는 해당 column의 글자 개수 입니다.
내용이 길어서 길이가 잘린다면 글자 개수를 늘려봅시다.
```bash
# example
sinfo -p srun -NO "CPUs:8" # CPU 개수 정보가 8칸으로 표시됨
sinfo -p srun -NO "CPUs:24" # CPU 개수 정보가 24칸으로 표시됨
```

#### 각 서버별 현재 사용가능한 자원 조회

`sinfo -p srun -NO "CPUs:8,CPUsState:16,Memory:9,AllocMem:10,GresUsed:50,NodeList:14"`

실행하면 아래와 같은 표가 출력됩니다.  
![avail](/miil/assets/sinfo_avail.png)

- CPUS(A/I/O/T) : I(Idle) 가 배정 받을 수 있는 개수. A(Alloc): 현재 사용중. T(Total): 전체
- MEMORY, ALLOCMEM : ( MEMORY - ALLOCMEM ) 이 현재 사용 가능함. MEMORY는 총량, ALLOCMEM은 현재 사용량.
- GRES_USED: 사용중인 GPU들. GPU type 별로 몇 개가 사용되는 중인지 파악 가능.

- CPUS(A/I/O/T) : I(Idle) is the number of idle cpus available. A(Alloc): currently used. T(Total) : Total number of cpus.
- GRES_USED: GPUs under use. It is able to check the number of currently used GPUs per each type.

#### 각 서버별 CPU/GPU/MEM 자원 총량

`sinfo -p sbatch -NO "CPUs:8,Memory:9,Gres:35,NodeList:14"`

실행하면 아래와 같은 표가 출력됩니다.  
![total](/miil/assets/sinfo_total.png)

서버에 있는 자원 총량이 표시됩니다.  
MEMORY: 메모리 총량(SWAP 제외) 입니다. MB 단위.  
GRES: GPU 종류별로 개수가 표시됩니다. (서버2 참조)