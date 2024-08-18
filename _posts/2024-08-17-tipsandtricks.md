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