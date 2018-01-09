import variables as var

def buffs(clicks, delays):
	result = list()
	multiply = 37
	if type(clicks) is int:
		return _build_buff(clicks * multiply + 81, delays)

	for e in range(len(clicks)):
		delay = delays[e]
		result.append(_build_buff(clicks[e] * multiply + 81, delay))

	return result

def _build_buff(x, delay):
	return {
		'x': x,
		'y': 745,
		'delay': delay,
		'process': 'click'
	}

def getBufferCommand(id):
	zero_pos = 150
	multiplier = 205 - 150
	return {
		var.process: 'click',
		var.x: 850,
		var.y: zero_pos + multiplier * id,
		var.delay: 1
	}


char_selector_cond = {
			var.process : 'recognize',
			var.region : (740, 130, 20, 20),
			var.img : var.IMG_PREFIX + 'load_marker.png',
			var.freq : 3
		}


def await_(delay):
	return {
		var.process: 'wait',
		var.delay: delay
	}

go_to_select_menu_v2 = [
	{
		var.process: 'center_on',
		var.region: (940, 740, 120, 120),
		var.img: var.IMG_PREFIX + 'menu_btn.png',
		var.freq: 1
	},
	{
		var.process: 'center_on',
		var.region: (955, 710,170, 20),
		var.img: var.IMG_PREFIX + 'system_menu.png',
		var.freq: 1
	},
	{
		var.process: 'center_on',
		var.region: (500, 400, 200, 30),
		var.img: var.IMG_PREFIX + 'to_char_select.png',
		var.freq: 1
	},
		{
		var.process: 'center_on',
		var.region: (580, 230, 100, 30),
		var.img: var.IMG_PREFIX + 'ok_btn.png',
		var.freq: 1
	},
]




load_char = {
	var.process : 'click',
	var.x : 930,
	var.y : 570,
	var.delay : 1
}


def make_single_buff(id, positions, delays):
	source =  [
		char_selector_cond,
		getBufferCommand(id),
		load_char,
		await_(8),
	 ] + buffs(positions, delays) + go_to_select_menu_v2

	return source


def make_reload_instruction(id):
	return [
		char_selector_cond,
		getBufferCommand(id),
		load_char,
		await_(13)
	] + go_to_select_menu_v2

buff_squence = [
	[4, [0], [2]],
	[5, [0], [2]],
	[6, [0], [2]],
	[3, [0], [2]],
	[0, [0,1,2,3,4], [2 ] * 5],
	[1, [0,1,2,3,4], [2] * 5],
	[2, [0], [2]],
	[7, [1,2,0], [2,2,5]]
]

def instruction(sequence):
	istr = []
	for e in sequence:
		istr += make_single_buff(e[0], e[1],e[2])
	for e in sequence:
		istr += make_reload_instruction(e[0])
	return istr


def getBuffInstruction():
	return instruction(buff_squence)


to_select_char_menu = [
		{
			var.process: 'click',
			var.x: 1005,
			var.y: 773,
			var.delay: 1
		},
		{
			var.process: 'click',
			var.x: 1005,
			var.y: 723,
			var.delay: 1
		},
		{
			var.process: 'click',
			var.x: 600,
			var.y: 413,
			var.delay: 1
		},
		{
			var.process: 'click',
			var.x: 635,
			var.y: 234,
			var.delay: 1
		}
	]
