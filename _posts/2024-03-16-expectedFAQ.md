---
title: (Expected) FAQ
author: Woongbae Jeon
date: 2024-03-16
category: FAQ
layout: post
---

# (Expected) FAQ

### Q. sbatch 작업을 srun 파티션에 제출하거나 vice versa의 경우 어떻게 되나요?

srun 작업을 sbatch에 제출하면 제출이 즉시 거부되거나, 제출 되더라도 3분 이내에 취소됩니다.  
해당 작업들이 취소 되었다고 알림이 가지는 않습니다.

### Q. srun으로 배정을 받으면 알림이 오나요?

아니요, 알림을 보내는 시스템이 없습니다. 수시로 확인 해야합니다.