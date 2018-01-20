from variables import *
import json

CONFIG = 'buff_utils.json'

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
		process: 'click',
		x: 850,
		y: zero_pos + multiplier * id,
		delay: 1
	}


char_selector_cond = {
			process : 'recognize',
			region : (740, 130, 20, 20),
			img : IMG_PREFIX + 'load_marker.png',
			freq : 3
		}


def await_(_delay):
	return {
		process: 'wait',
		delay: _delay
	}

go_to_select_menu_v2 = [
	{
		process: 'center_on',
		region: (940, 740, 120, 120),
		img: IMG_PREFIX + 'menu_btn.png',
		freq: 1
	},
	{
		process: 'center_on',
		region: (955, 710,170, 20),
		img: IMG_PREFIX + 'system_menu.png',
		freq: 1
	},
	{
		process: 'center_on',
		region: (500, 400, 200, 30),
		img: IMG_PREFIX + 'to_char_select.png',
		freq: 1
	},
		{
		process: 'center_on',
		region: (580, 230, 100, 30),
		img: IMG_PREFIX + 'ok_btn.png',
		freq: 1
	},
]




load_char = {
	process : 'click',
	x : 930,
	y : 570,
	delay : 1
}


def make_single_buff(id, positions, delays, cfg=None):
	source =  [
		cfg['is_char_select'],
		getBufferCommand(id),
		cfg['load_char'],
		await_(8),
	 ] + buffs(positions, delays) + cfg['select_char_menu']

	return source


def make_reload_instruction(id, cfg=None):
	return [
		cfg['is_char_select'],
		getBufferCommand(id),
		cfg['load_char'],
		await_(13)
	] + cfg['select_char_menu']

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
	cfg = import_config()
	istr = []
	for e in sequence:
		istr += make_single_buff(e[0], e[1],e[2], cfg=cfg)
	for e in sequence:
		istr += make_reload_instruction(e[0], cfg=cfg)
	return istr


def getBuffInstruction():
	return instruction(buff_squence)


to_select_char_menu = [
		{
			process: 'click',
			x: 1005,
			y: 773,
			delay: 1
		},
		{
			process: 'click',
			x: 1005,
			y: 723,
			delay: 1
		},
		{
			process: 'click',
			x: 600,
			y: 413,
			delay: 1
		},
		{
			process: 'click',
			x: 635,
			y: 234,
			delay: 1
		}
	]

def import_config():
	config = open(CONFIG, 'r')
	configuration = config.read()
	config.close()
	return json.loads(configuration)
