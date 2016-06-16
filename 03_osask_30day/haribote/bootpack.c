/* bootpack */

#include "bootpack.h"
#include <stdio.h>

#define KEYCMD_LED		0xed		//mid  LED 的状态，EDxx 数据。其中， xx 的 bit 0 代表 ScrollLock ， bit 1 代表 NumLock ， bit 2 代表 CapsLock

void keywin_off(struct SHEET *key_win);
void keywin_on(struct SHEET *key_win);
void close_console(struct SHEET *sht);
void close_constask(struct TASK *task);

void HariMain(void)
{
	struct BOOTINFO *binfo = (struct BOOTINFO *) ADR_BOOTINFO;	//mid 固定内存地址作为启动信息的储存位置
	struct SHTCTL *shtctl;			//mid 普通局部变量
	char s[40];
	//mid fifo为中断缓冲，keycmd为任务发向键盘的键的缓冲
	//mid keycmd用于操作键盘灯
	//mid 键盘事件的接收者为窗口，窗口接收到键盘消息后根据其处理逻辑对键盘消息进行处理
	//mid 当用户按下caplock之类的键盘状态切换键之后，需要切换键盘状态
	//mid 键盘本身无内部状态指示切换权利，处理逻辑如下
	//mid caplock，当前程序接受消息，当前程序将该消息发送给cpu，cpu操作键盘状态切换
	struct FIFO32 fifo, keycmd;
	int fifobuf[128], keycmd_buf[32];
	int mx, my, i, new_mx = -1, new_my = 0, new_wx = 0x7fffffff, new_wy = 0;
	unsigned int memtotal;
	struct MOUSE_DEC mdec;
	struct MEMMAN *memman = (struct MEMMAN *) MEMMAN_ADDR;
	unsigned char *buf_back, buf_mouse[256];
	struct SHEET *sht_back, *sht_mouse;
	struct TASK *task_a, *task;
	static char keytable0[0x80] = {
		0,   0,   '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '^', 0x08, 0,
		'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '@', '[', 0x0a, 0, 'A', 'S',
		'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', ':', 0,   0,   ']', 'Z', 'X', 'C', 'V',
		'B', 'N', 'M', ',', '.', '/', 0,   '*', 0,   ' ', 0,   0,   0,   0,   0,   0,
		0,   0,   0,   0,   0,   0,   0,   '7', '8', '9', '-', '4', '5', '6', '+', '1',
		'2', '3', '0', '.', 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
		0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
		0,   0,   0,   0x5c, 0,  0,   0,   0,   0,   0,   0,   0,   0,   0x5c, 0,  0
	};
	static char keytable1[0x80] = {
		0,   0,   '!', 0x22, '#', '$', '%', '&', 0x27, '(', ')', '~', '=', '~', 0x08, 0,
		'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '`', '{', 0x0a, 0, 'A', 'S',
		'D', 'F', 'G', 'H', 'J', 'K', 'L', '+', '*', 0,   0,   '}', 'Z', 'X', 'C', 'V',
		'B', 'N', 'M', '<', '>', '?', 0,   '*', 0,   ' ', 0,   0,   0,   0,   0,   0,
		0,   0,   0,   0,   0,   0,   0,   '7', '8', '9', '-', '4', '5', '6', '+', '1',
		'2', '3', '0', '.', 0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
		0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,   0,
		0,   0,   0,   '_', 0,   0,   0,   0,   0,   0,   0,   0,   0,   '|', 0,   0
	};
	int key_shift = 0, key_leds = (binfo->leds >> 4) & 7, keycmd_wait = -1;
	int j, x, y, mmx = -1, mmy = -1, mmx2 = 0;
	//mid key_win 为当前图层
	struct SHEET *sht = 0, *key_win, *sht2;
	int *fat;
	unsigned char *nihongo;
	struct FILEINFO *finfo;
	extern char hankaku[4096];

	init_gdtidt();
	init_pic();		//mid 初始化中断
	io_sti(); /* IDT/PIC的初始化已经完成，于是开放CPU的中断 */
	fifo32_init(&fifo, 128, fifobuf, 0);	//mid 中断缓冲区
	*((int *) 0x0fec) = (int) &fifo;
	init_pit();		//mid 初始化时钟
	init_keyboard(&fifo, 256);	//mid 初始化键盘中断缓冲区,将中断缓冲区的256开始的部分分配给键盘中断用于储存数据
	enable_mouse(&fifo, 512, &mdec);	//mid 设置mded的阶段
	io_out8(PIC0_IMR, 0xf8); /* 设定PIT和PIC1以及键盘为许可(11111000) */
	io_out8(PIC1_IMR, 0xef); /* 开放鼠标中断(11101111) */
	fifo32_init(&keycmd, 32, keycmd_buf, 0);

	memtotal = memtest(0x00400000, 0xbfffffff);				//mid 4,194,304 to 3,221,225,471 :  4M-3G
	memman_init(memman);
	//mid 将某位置开始的size个内存登记为可用
	memman_free(memman, 0x00001000, 0x0009e000);			//mid 4,096 - 647,168  :  4K-600K
	memman_free(memman, 0x00400000, memtotal - 0x00400000);	//mid 4,194,304 to  :  4M-

	init_palette();
	shtctl = shtctl_init(memman, binfo->vram, binfo->scrnx, binfo->scrny);	//mid 向内存管理结构申请sheets管理内存
	task_a = task_init(memman);
	fifo.task = task_a;
	task_run(task_a, 1, 2);
	//mid 0x0fe4 是个变量地址，用来储存shtctl的地址，此地址在程序的很多地方都在使用，如此直接使用内存地址读写数据感觉不好，该定义为一个恰当命名地址常量，或者是一个函数，不知小日本有何深意
	*((int *) 0x0fe4) = (int) shtctl;
	task_a->langmode = 0;

	//mid 1.申请一个可用图层作为background
	sht_back  = sheet_alloc(shtctl);
	//mid 2.位background图层申请图像记录内存(显存)
	buf_back  = (unsigned char *) memman_alloc_4k(memman, binfo->scrnx * binfo->scrny);
	//mid 3.关联图层管理对象和显存
	sheet_setbuf(sht_back, buf_back, binfo->scrnx, binfo->scrny, -1); /* 无透明色 */
	//mid 4.初始化显存
	init_screen8(buf_back, binfo->scrnx, binfo->scrny);

	//mid 控制台窗口创建，运行并显示
	key_win = open_console(shtctl, memtotal);

	//mid 鼠标绘制图层创建
	sht_mouse = sheet_alloc(shtctl);
	sheet_setbuf(sht_mouse, buf_mouse, 16, 16, 99);
	init_mouse_cursor8(buf_mouse, 99);
	mx = (binfo->scrnx - 16) / 2; /* 计算坐标使其位于画面中央 */
	my = (binfo->scrny - 28 - 16) / 2;

	//mid 移动图层窗口
	sheet_slide(sht_back,  0,  0);
	sheet_slide(key_win,   32, 4);
	sheet_slide(sht_mouse, mx, my);
	sheet_updown(sht_back,  0);
	sheet_updown(key_win,   1);
	sheet_updown(sht_mouse, 2);
	//mid keywin_on 这个函数的功能很简单，先是改变窗口的颜色，然后向命令行窗口任务的 FIFO 发送 2 这个值用来显示光标。
	keywin_on(key_win);

	/* 为了避免和键盘当前状态冲突，在一开始先进行设置 */
	fifo32_put(&keycmd, KEYCMD_LED);
	fifo32_put(&keycmd, key_leds);

	//mid 将文件分配表FAT从磁盘镜像中读出，解压到fat中
	fat = (int *) memman_alloc_4k(memman, 4 * 2880);
	file_readfat(fat, (unsigned char *) (ADR_DISKIMG + 0x000200));
	//mid 从磁盘文件中检索nihongo.fnt字体文件的储存信息，包括大小，位置
	finfo = file_search("nihongo.fnt", (struct FILEINFO *) (ADR_DISKIMG + 0x002600), 224);
	if (finfo != 0) {
		i = finfo->size;
		//mid 获取加载到内存中的字体文件的地址
		nihongo = file_loadfile2(finfo->clustno, &i, fat);
	} else {
		//mid 如果没有字体文件信息，则生成
		nihongo = (unsigned char *) memman_alloc_4k(memman, 16 * 256 + 32 * 94 * 47);
		for (i = 0; i < 16 * 256; i++) {
			nihongo[i] = hankaku[i]; /*没有字库，半角部分直接复制英文字库*/
		}
		for (i = 16 * 256; i < 16 * 256 + 32 * 94 * 47; i++) {
			nihongo[i] = 0xff; /* 没有字库，全角部分以0xff填充 */
		}
	}
	*((int *) 0x0fe8) = (int) nihongo;
	
	//mid fat在此的目的就是为了检索字体文件，完成使命后释放内存
	memman_free_4k(memman, (int) fat, 4 * 2880);

	//mid 进入操作系统事件处理循环
	//mid 操作系统处理为一个不断读取键盘和鼠标消息的无限循环
	//mid 获取消息后将消息加入当前窗口任务的待处理fifo队列
	//mid 每个fifo对消息的处理方式都可以自定义
	//mid 以console为例，为一无限循环，不断读取其待处理消息列表，并处理之，直到遇到关闭窗口的鼠标操作
	//mid 所有cmd命令都通过cons_runcmd处理，又分为内置系统命令和应用程序命令
	//mid 应用程序命令单独用cmd_app处理
	//mid 每个sonsole的命令执行时都会分配timer定时器，表示其将参与cpu时间分配
	//mid 最后，一个被成功加载入系统的应用程序会被通过start_app启动
	for (;;) {
		//mid 对键盘状态的反向控制，比如某个程序想让键盘处于caplock状态
		if (fifo32_status(&keycmd) > 0 && keycmd_wait < 0) {
			/* 如果存在向键盘控制器发送的数据，则发送它 */
			keycmd_wait = fifo32_get(&keycmd);
			wait_KBC_sendready();
			io_out8(PORT_KEYDAT, keycmd_wait);
		}
		io_cli();
		if (fifo32_status(&fifo) == 0) {
			/* FIFO为空，当存在搁置的绘图操作时立即执行*/
			if (new_mx >= 0) {
				io_sti();
				sheet_slide(sht_mouse, new_mx, new_my);
				new_mx = -1;
			} else if (new_wx != 0x7fffffff) {
				io_sti();
				sheet_slide(sht, new_wx, new_wy);
				new_wx = 0x7fffffff;
			} else {
				task_sleep(task_a);
				io_sti();
			}
		} else {
			i = fifo32_get(&fifo);
			io_sti();
			if (key_win != 0 && key_win->flags == 0) { /*窗口被关闭*/
				if (shtctl->top == 1) { /*当画面上只剩鼠标和背景时*/
					key_win = 0;
				} else {
					key_win = shtctl->sheets[shtctl->top - 1];
					keywin_on(key_win);
				}
			}
			if (256 <= i && i <= 511) { /* 键盘数据*/
				if (i < 0x80 + 256) { /*将按键编码转换为字符编码*/
					if (key_shift == 0) {
						s[0] = keytable0[i - 256];
					} else {
						s[0] = keytable1[i - 256];
					}
				} else {
					s[0] = 0;
				}
				if ('A' <= s[0] && s[0] <= 'Z') { /*当输入字符为英文字母时*/
					if (((key_leds & 4) == 0 && key_shift == 0) ||
							((key_leds & 4) != 0 && key_shift != 0)) {
						s[0] += 0x20; /*将大写字母转换为小写字母*/
					}
				}
				if (s[0] != 0 && key_win != 0) {							//mid 命令处理，一般字符、退格键、回车键
					fifo32_put(&key_win->task->fifo, s[0] + 256);
				}
				if (i == 256 + 0x0f && key_win != 0) {	/* Tab键 */
					keywin_off(key_win);
					j = key_win->height - 1;
					if (j == 0) {
						j = shtctl->top - 1;
					}
					key_win = shtctl->sheets[j];
					keywin_on(key_win);
				}
				if (i == 256 + 0x2a) { /*左Shift ON */
					key_shift |= 1;
				}
				if (i == 256 + 0x36) { /*右Shift ON */
					key_shift |= 2;
				}
				if (i == 256 + 0xaa) { /*左Shift OFF */
					key_shift &= ~1;
				}
				if (i == 256 + 0xb6) { /*右Shift OFF */
					key_shift &= ~2;
				}
				if (i == 256 + 0x3a) {	/* CapsLock */
					key_leds ^= 4;
					fifo32_put(&keycmd, KEYCMD_LED);
					fifo32_put(&keycmd, key_leds);
				}
				if (i == 256 + 0x45) {	/* NumLock */
					key_leds ^= 2;
					fifo32_put(&keycmd, KEYCMD_LED);
					fifo32_put(&keycmd, key_leds);
				}
				if (i == 256 + 0x46) {	/* ScrollLock */
					key_leds ^= 1;
					fifo32_put(&keycmd, KEYCMD_LED);
					fifo32_put(&keycmd, key_leds);
				}
				if (i == 256 + 0x3b && key_shift != 0 && key_win != 0) {	/* Shift+F1 */
					//mid 关闭当前active的应用程序窗口，不能关闭console窗口
					task = key_win->task;
					if (task != 0 && task->tss.ss0 != 0) {
						cons_putstr0(task->cons, "\nBreak(key) :\n");
						io_cli(); /*强制结束处理时禁止任务切换*/
						task->tss.eax = (int) &(task->tss.esp0);
						task->tss.eip = (int) asm_end_app;
						io_sti();
						task_run(task, -1, 0); /*为了确实执行结束处理，如果处于休眠状态则唤醒*/
					}
				}
				if (i == 256 + 0x3c && key_shift != 0) {	/* Shift+F2 */
					//mid 打开一个新的console窗口
					if (key_win != 0) {
						keywin_off(key_win);
					}
					key_win = open_console(shtctl, memtotal);
					sheet_slide(key_win, 32, 4);
					sheet_updown(key_win, shtctl->top);
					keywin_on(key_win);
				}
				if (i == 256 + 0x57) {	/* F11 */
					sheet_updown(shtctl->sheets[1], shtctl->top - 1);
				}
				if (i == 256 + 0xfa) { /*键盘成功接收到数据*/
					keycmd_wait = -1;
				}
				if (i == 256 + 0xfe) { /*键盘没有成功接收到数据*/
					wait_KBC_sendready();
					io_out8(PORT_KEYDAT, keycmd_wait);
				}
			} else if (512 <= i && i <= 767) { /* 鼠标数据*/
				if (mouse_decode(&mdec, i - 512) != 0) {
					/* 已经收集了3字节的数据，移动光标 */
					mx += mdec.x;
					my += mdec.y;
					if (mx < 0) {
						mx = 0;
					}
					if (my < 0) {
						my = 0;
					}
					if (mx > binfo->scrnx - 1) {
						mx = binfo->scrnx - 1;
					}
					if (my > binfo->scrny - 1) {
						my = binfo->scrny - 1;
					}
					new_mx = mx;
					new_my = my;
					if ((mdec.btn & 0x01) != 0) { /* 按下左键 */
						if (mmx < 0) {
							/*如果处于通常模式*/
							/*按照从上到下的顺序寻找鼠标所指向的图层*/
							for (j = shtctl->top - 1; j > 0; j--) {
								sht = shtctl->sheets[j];
								x = mx - sht->vx0;
								y = my - sht->vy0;
								if (0 <= x && x < sht->bxsize && 0 <= y && y < sht->bysize) {
									if (sht->buf[y * sht->bxsize + x] != sht->col_inv) {
										sheet_updown(sht, shtctl->top - 1);
										if (sht != key_win) {
											keywin_off(key_win);
											key_win = sht;
											keywin_on(key_win);
										}
										if (3 <= x && x < sht->bxsize - 3 && 3 <= y && y < 21) {
											mmx = mx; /*进入窗口移动模式*/
											mmy = my;
											mmx2 = sht->vx0;
											new_wy = sht->vy0;
										}
										if (sht->bxsize - 21 <= x && x < sht->bxsize - 5 && 5 <= y && y < 19) {
											//mid 单击窗口X按钮
											if ((sht->flags & 0x10) != 0) { /*该窗口是否为应用程序窗口？*/
												//mid 关闭应用程序窗口处理
												task = sht->task;
												cons_putstr0(task->cons, "\nBreak(mouse) :\n");
												io_cli(); /*强制结束处理时禁止任务切换*/
												task->tss.eax = (int) &(task->tss.esp0);
												task->tss.eip = (int) asm_end_app;
												io_sti();
												task_run(task, -1, 0);
											} else {
												//mid 关闭console处理
												task = sht->task;
												sheet_updown(sht, -1); /*暂且隐藏该图层*/
												keywin_off(key_win);
												key_win = shtctl->sheets[shtctl->top - 1];
												keywin_on(key_win);
												io_cli();
												fifo32_put(&task->fifo, 4);
												io_sti();
											}
										}
										break;
									}
								}
							}
						} else {
							/*如果处于窗口移动模式*/
							x = mx - mmx; /*计算鼠标指针移动量*/
							y = my - mmy;
							new_wx = (mmx2 + x + 2) & ~3;
							new_wy = new_wy + y;
							mmy = my;
						}
					} else {
						/*没有按下左键*/
						mmx = -1; /*切换到一般模式*/
						if (new_wx != 0x7fffffff) {
							sheet_slide(sht, new_wx, new_wy); /*固定图层位置*/
							new_wx = 0x7fffffff;
						}
					}
				}
			} else if (768 <= i && i <= 1023) { /*命令行窗口关闭处理*/
				close_console(shtctl->sheets0 + (i - 768));
			} else if (1024 <= i && i <= 2023) {
				close_constask(taskctl->tasks0 + (i - 1024));
			} else if (2024 <= i && i <= 2279) { /*只关闭命令行窗口*/
				sht2 = shtctl->sheets0 + (i - 2024);
				memman_free_4k(memman, (int) sht2->buf, 256 * 165);
				sheet_free(sht2);
			}
		}
	}
}
//mid 使窗口标题栏变暗，用于表示失去焦点，不在接受键盘消息
void keywin_off(struct SHEET *key_win)
{
	change_wtitle8(key_win, 0);
	if ((key_win->flags & 0x20) != 0) {
		fifo32_put(&key_win->task->fifo, 3); /*命令行窗口光标OFF */
	}
	return;
}
//mid 使窗口变亮，使其成为当前活动窗口后做此操作，以通知user
void keywin_on(struct SHEET *key_win)
{
	change_wtitle8(key_win, 1);
	if ((key_win->flags & 0x20) != 0) {
		fifo32_put(&key_win->task->fifo, 2); /*命令行窗口光标ON */
	}
	return;
}

struct TASK *open_constask(struct SHEET *sht, unsigned int memtotal)
{
	struct MEMMAN *memman = (struct MEMMAN *) MEMMAN_ADDR;
	struct TASK *task = task_alloc();
	int *cons_fifo = (int *) memman_alloc_4k(memman, 128 * 4);
	task->cons_stack = memman_alloc_4k(memman, 64 * 1024);
	task->tss.esp = task->cons_stack + 64 * 1024 - 12;
	task->tss.eip = (int) &console_task;							//mid	指明当前task的入口函数地址
	task->tss.es = 1 * 8;
	task->tss.cs = 2 * 8;
	task->tss.ss = 1 * 8;
	task->tss.ds = 1 * 8;
	task->tss.fs = 1 * 8;
	task->tss.gs = 1 * 8;
	*((int *) (task->tss.esp + 4)) = (int) sht;
	*((int *) (task->tss.esp + 8)) = memtotal;
	task_run(task, 2, 2); /* level=2, priority=2 */
	fifo32_init(&task->fifo, 128, cons_fifo, task);
	return task;
}

struct SHEET *open_console(struct SHTCTL *shtctl, unsigned int memtotal)
{
	struct MEMMAN *memman = (struct MEMMAN *) MEMMAN_ADDR;
	struct SHEET *sht = sheet_alloc(shtctl);
	unsigned char *buf = (unsigned char *) memman_alloc_4k(memman, 256 * 165);
	sheet_setbuf(sht, buf, 256, 165, -1); /*无透明色*/
	make_window8(buf, 256, 165, "console", 0);
	make_textbox8(sht, 8, 28, 240, 128, COL8_000000);
	sht->task = open_constask(sht, memtotal);
	sht->flags |= 0x20;	/*有光标*/
	return sht;
}

void close_constask(struct TASK *task)
{
	struct MEMMAN *memman = (struct MEMMAN *) MEMMAN_ADDR;
	task_sleep(task);
	memman_free_4k(memman, task->cons_stack, 64 * 1024);
	memman_free_4k(memman, (int) task->fifo.buf, 128 * 4);
	task->flags = 0; /*用来替代task_free(task); */
	return;
}

void close_console(struct SHEET *sht)
{
	struct MEMMAN *memman = (struct MEMMAN *) MEMMAN_ADDR;
	struct TASK *task = sht->task;
	memman_free_4k(memman, (int) sht->buf, 256 * 165);
	sheet_free(sht);
	close_constask(task);
	return;
}
