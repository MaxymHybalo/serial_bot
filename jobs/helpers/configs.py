# Support classes
class CharTitleConfig:
    light = 0
    dark = (18, 255, 255)
    template = 'assets/circus_flow/guide_siege_title.png'
    roi=None

class GuildIconConfig:
    light = (50, 0, 0)
    dark = (60, 200, 255)
    template = 'assets/circus_flow/guild_icon.png'
    roi=None

class StartPointConfig:
    light = (0,0,0)
    dark = (80, 100, 40)
    template = 'assets/circus_flow/altar_ground.png'
    roi = (760, 220, 60, 80)

class QuestMenu:
    path = 'assets/circus_flow/quest_menu.png'
    roi = (630, 200, 200, 30)

class AcceptQuest:
    path = 'assets/circus_flow/accept_quest.png'
    roi = (665, 720, 110, 25)
