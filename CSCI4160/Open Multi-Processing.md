### **Open Multi-Processing**

==What is OpenMP?== 是一种规范API，不同的编译器有不同的实现方式(Intel用pthread) 有**easy parallelization**但不保证efficient use of shared memory。他假设都是parallelizable jobs没有race conditions/deadlocks等，Parallelism is expressed as threads。
==执行模型--Fork-Join== 从一个master thread开始，到parallel region先fork a team of parallel threads，等所有的threads complete, synchronize and terminate就join
<font color=green>1. Data Scoping</font>: OpenMP共享内存模型, 可以explicitly define scope (private/shared)
<font color=green>2. Nested Parallelism</font>: 并行区里面套并行区
<font color=green>3. Dynamic Thread</font>: 动态调整并行区的线程数量
==创建Parallel Regions==
![image-20260418031235754](C:\Users\31670\AppData\Roaming\Typora\typora-user-images\image-20260418031235754.png)
==Synchronization 同步==
<font color=green>**High level**</font> **critical**：确保代码块同一时间只有一个线程执行  **atomic**：针对特定内存地址的原子更新  **barrier**：让所有线程在此等待，直到大家都到达这个点  **ordered**：按照循环原本的顺序执行 
<font color=green>**Low level**</font> **flush**：确保所有threads看到的共有数据是一致的(可能只在cache更新了没有写回zhu'cheng'xu)  **locks**：显式地加锁和解锁，类似于 pthread 的互斥锁 