
def make_extruder_env():
    import os
    try:
        os.mkdir('assets/data')
        os.mkdir('assets/data/screens')
        os.mkdir('assets/data/npc_extruded_by_char_color')
        os.mkdir('assets/data/npc_template_matched')
    except FileExistsError:
        print('Environment already exist')