# -*- coding: utf-8 -*-
'''mid
upsea下有两类文件夹
1.策略类
	每个文件价代表一个策略的不同配置，其中策略的固定部分在文件夹下，
	配置部分单独作为一个文件
	Ea和EaController本来该是一个类且单独设置在一个文件中，为了配置更加清晰，
	将可配置部分作为EaController类，不可配置部分作为Ea类
2.公共类
	公共类，包括由pyalgotrade专用的money
	可扩展
'''