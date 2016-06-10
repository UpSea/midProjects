# -*- coding: utf-8 -*-
'''
参考：http://blog.csdn.net/h820911469/article/details/20136411

1.格式化U盘
2.将grub4dos引导程序安装到U盘mbr
3. 将grub4dos拷贝入U盘根目录
4.编辑U盘根目录下menu.lst


笔记本有一块硬盘，分3个区，第一个区安装有ubuntu14.04引导程序
有一个软盘镜像文件，其中包含有一个可引导操作系统，保存在U盘根目录下

menu.lst如下内容：

title commandline
commandline

title Ubuntu.Grub2Loader
kernel (hd1,0)/boot/grub/i386-pc/core.img
boot

title floppy (fd0)
map --mem (hd0,0)/haribote.img (fd0)
map --hook
chainloader (fd0)+1
rootnoverify (fd0)

主要麻烦出现在通过采用grub1的grub4dos引导采用grub2的ubuntu14.04
ubuntu好像在9之前使用grub1引导，之后使用grub2。
1和2的区别在于1使用menu.lst，2使用grub.cfg。这两文件格式不同，我没找到对应关系不能方便的合并。
(hdx.y)表示的是第x个硬盘的第个分区，0为基数。
hd以bios中设定的引导顺序为准，是个变量。
例如，笔记本只有一个硬盘，应编号hd0。
插入U盘作为第一启动设备之后，U盘编号为hd0，原有硬盘为hd1.
'''