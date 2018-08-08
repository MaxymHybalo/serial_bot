from utils.configurator import Configurator
from processes.click import Click
from processes.wait import Wait



# Abstract things:
# 1. Move some features to global scope (window detection, splits, etc)
# features for buff 2.0:
# 0. Add in Arduiono sketch keyboard support                                +
# 1. Autodetect window
# 2. Split window to usefull zones
# 3. Start from 'in game mode'
# 4. Try to use 'splinter' icon to detect that character loaded
# 5. Use keywords for buffing
# In game enhacement
# 1. Add cast and run speed
# 
# Base points, and demensions
# Game window start position dy=5, dx=3, marker='window_marker'

CONFIG = 'buff_utils.json'

full_buff_sequence = [
    [4, [0], [2]],
    [5, [0], [2]],
    [6, [0], [2]],
    [3, [0], [2]],
    [0, [0, 1, 2, 3, 4], [2] * 5],
    [1, [0, 1, 2, 3, 4], [2] * 5],
    [2, [0], [2]],
    [7, [1, 2, 0], [2, 2, 5]]
]

farm_buff_sequence = [
    [1, [0, 1, 2, 3, 4], [2] * 5],
    [2, [0], [1]],
    [6, [0], [1]]
]


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
    return Click(x, 745, delay=delay)


def get_buff_command(index):
    zero_pos = 150
    multiplier = 205 - 150
    return Click(
        850,
        zero_pos + multiplier * index,
        delay=1
    )


def make_single_buff(index, positions, delays, cfg=None):
    source = [
                 cfg['is_char_select'],
                 get_buff_command(index),
                 cfg['load_char'],
                 Wait(10),
             ] + buffs(positions, delays) + cfg['select_char_menu']

    return source


def make_reload_instruction(index, cfg=None):
    return [
               cfg['is_char_select'],
               get_buff_command(index),
               cfg['load_char'],
               Wait(13)
           ] + cfg['select_char_menu']


def instruction(sequence, reload):
    cfg = _config()
    order = []
    for e in sequence:
        order += make_single_buff(e[0], e[1], e[2], cfg=cfg)
    if reload:
        for e in sequence:
            order += make_reload_instruction(e[0], cfg=cfg)
    return order


def to_reload(is_return=False):
    cfg = _config()
    print(cfg)
    if is_return:
        from processes.recognizer import Recognizer
        from shapes.rect import Rect
        click = Recognizer('assets/return_scroll.png', region=None).recognize()
        click = Rect(click).click()
        return [click, Wait(11)] + cfg['select_char_menu']
    return cfg['select_char_menu']


def get_buff_instruction(sequence=full_buff_sequence, reload=False):
    return instruction(sequence, reload)


def _config():
    cfg = Configurator(CONFIG)
    return cfg.generate_objects()
