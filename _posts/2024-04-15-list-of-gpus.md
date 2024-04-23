---
title: List of GPUs
author: Woongbae Jeon
date: 2024-04-15
layout: post
---

### Server1

|GPU Type | 개수 | Slurm GRES Code|  
|--------|------|--------|  
|RTX3090 | 3 | `--gres=gpu:RTX3090:<n>`|

### Server2

|GPU Type | 개수 | Slurm GRES Code|  
|--------|------|--------|  
|RTX3090 | 2 | `--gres=gpu:RTX3090:<n>`|
|Quadro 8000 | 6 | `--gres=gpu:Q8000:<n>`|

### Server3

PCI 및 Slurm 버그로 인해서 다음과 같이 사용 바랍니다.  
`A600x` 는 똑같은 A6000 GPU들, `A500x`는 똑같은 A5000 GPU들로,  
성능이나 사용하는데 차이는 없습니다. 할당 오류를 해결하기 위한 번호 부여입니다.

|GPU Type | 개수 | Slurm GRES Code|  
|--------|------|--------|  
|A5001 | 1 | `--gres=gpu:A5001:<n>`|
|A6001 | 1 | `--gres=gpu:A6001:<n>`|
|A5002 | 1 | `--gres=gpu:A5002:<n>`|
|A5003 | 1 | `--gres=gpu:A5003:<n>`|
|A6000 | 4 | `--gres=gpu:A6000:<n>`|