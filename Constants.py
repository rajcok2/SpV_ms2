############

BACKGROUND_IMAGE_SIZE = (800, 464)
CARROT_SIZE = (int(300/5), int(293/5))
COLLECT_SIZE = (int(102*5/7), int(103*5/7))
FORWARD_SIZE = (int(102*5/7), int(103*5/7))
VEHICLE_SIZE = (int(300 / 2), int(190 / 2))
ARROW_SIZE = (int(297/5), int(194/5))
HILL_SIZE = (300, 109)

############ POSITIONS ##############

TEXT_POSITION_1 = (900, 50)  # ZBIERANIE
TEXT_POSITION_2 = (900, 100)  # MRKVY
TEXT_POSITION_3 = (900, 175)  # UROVEN
TEXT_POSITION_4 = (900, 100)  # MRKVY
TEXT_POSITION_5 = (900, 100)  # 0/3

START_BUTTON_POSITION = (810, 255, 890, 295)
RESTART_BUTTON_POSITION = (900, 255, 990, 295)

ARROW_COMMAND_POSITION = ()
CARROT_COMMAND_POSITION = ()

COMMAND_BOX_SIZE = 75
COMMAND_BOX_START_POSITION = (30, 30)

############ APP PROPERTIES ######

FONT_TYPE_1 = ('Comic Sans MS', 25)
FONT_TYPE_2 = ('Rockwell-ExtraBold', 22)
FONT_TYPE_3 = ('Showcard Gothic', 28)
FONT_TYPE_4 = ('sans-serif', 15)

############ IMAGES PATH ############

BACKGROUND = 'sources/pozadie.png'
CARROT = 'sources/mrkva.png'
ARROW = 'sources/sipka.png'
VEHICLE = 'sources/traktor.png'
HILL = 'sources/kopec.png'
COLLECT_COMMAND = 'sources/zdvihni.png'
FORWARD_COMMAND = 'sources/dopredu.png'

############ APP PROPERTIES ############

APP_NAME = 'Zbieranie mrkvy'
LEVEL = 'Úroveň {}'
START = 'Štart'
RESTART = 'Opakuj'
CARROTS_COUNT = 'Mrkvy'

BACKGROUND_COLOR = "#A8DDE0"
HEAD_ICON = 'sources/carrot.ico'
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
INITIAL_SIZE_AND_POSITION = "1000x600+200+50"
INITIAL_STATE = 'zoomed'

############ APP TOOLS ############

ACTIVE_COMMAND_COLOR = 'red'

############ TASKS TEMPLATE ############

LEVELS = {1: (2, 1),
          2: (3, 1),
          3: (3, 2),
          4: (4, 2),
          5: (5, 2),
          6: (5, 2),
          7: (6, 3),
          8: (8, 4)}
