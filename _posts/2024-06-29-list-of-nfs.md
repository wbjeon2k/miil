---
title: List of NFSs
author: Woongbae Jeon
date: 2024-06-29
layout: post
---

### Network File Storage(NFS)

마치 로컬 디스크를 사용하듯, 디스크를 네트워크로 연결하는 시스템을 의미합니다.  

서버 재부팅 후에 자동으로 mount가 되지 않는 증상이 있습니다.  
서버 관리 작업 후 nfs 접속이 되지 않으면, 관리자에게 알려주세요.  

#### NFS0

- Physical Location : Workstation 2
- Size : 1.8 TB
- `/nfs0`
- `@seungb` 의 CC3M data 보관 전용으로 사용됩니다.

#### NFS1

- Physical Location : Workstation 2
- Size : 1.8 TB
- `/nfs1`
- Quota : 250G per user

#### NFS2

- Physical Location : Server 5
- Size : 1.8 TB
- `/nfs2`
- Quota : 250G per user

#### NFS3

- Physical Location : workstation3
- Size : 3.7 TB
- `/nfs3`
- Quota : 500G per user

#### NFS4

- Physical Location : workstation3
- Size : 3.7 TB
- `/nfs4`
- Quota : 500G per user