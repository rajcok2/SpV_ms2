from tkinter import *
from Constants import *
from PIL import ImageTk, Image
from copy import copy
import random
from time import sleep


class CommandItem:
    def __init__(self, canvas, position):
        self.canvas = canvas
        self.box_coords = ()
        self.command_id = None
        self.command_tag = None
        self.command_type = None
        self.command_coords = None
        self.position_in_sequence = position

    def set_command(self, _id, _tag, _type):
        self.command_id = _id
        self.command_tag = _tag
        self.command_type = _type
        # self.command_coords = item.command_coords

    def remove_command(self):
        self.command_id = None
        self.command_tag = None
        self.command_type = None
        # self.command_coords = None

    def draw(self, x0, y0, x1, y1):
        self.box_coords = (x0, y0, x1, y1)
        self.id = self.canvas.create_rectangle(self.box_coords, fill='ghost white', outline='#696969', width=3)

    def change_state(self, state):
        if state == 1:
            self.canvas.itemconfig(self.id, fill='red')
        else:
            self.canvas.itemconfig(self.id, fill='ghost white')


class Playground(Tk):

    def __init__(self):
        super().__init__()
        self.configure_main_window()
        parent = Frame(self, bg='red')
        parent.pack(side=BOTTOM, fill=BOTH, expand=TRUE)
        self.playground = Canvas(parent, width=SCREEN_WIDTH, height=SCREEN_HEIGHT, highlightthickness=0)
        self.playground.pack()
        self.update()

        self.background_image_id = None
        self.commands_list = list()
        self.playground.bind("<ButtonPress-1>", self.click)
        self.playground.bind("<B1-Motion>", self.drag)
        self.playground.bind("<ButtonPress-3>", self.remove)
        self.playground.bind("<ButtonRelease-1>", self.drop)

        self.isDragged = False
        self.obj_id = None
        self.obj_tag = None

        self.hills_array = []
        self.level = 1

        # nacitanie obrazkov
        self.background_image_source = Image.open(BACKGROUND)
        self.background_image = ImageTk.PhotoImage(self.background_image_source)

        self.collect_command_image_source = Image.open(COLLECT_COMMAND).resize(COLLECT_SIZE, Image.ANTIALIAS)
        self.collect_command_image = ImageTk.PhotoImage(self.collect_command_image_source)

        self.vehicle_image_source = Image.open(VEHICLE).resize(VEHICLE_SIZE, Image.ANTIALIAS)
        self.vehicle_image = ImageTk.PhotoImage(self.vehicle_image_source)

        self.forward_command_image_source = Image.open(FORWARD_COMMAND).resize(FORWARD_SIZE, Image.ANTIALIAS)
        self.forward_command_image = ImageTk.PhotoImage(self.forward_command_image_source)

        self.hill_image_source = Image.open(HILL).resize(HILL_SIZE, Image.ANTIALIAS)
        self.hill_image = ImageTk.PhotoImage(self.hill_image_source)

        self.collectible_carrot_source = Image.open(CARROT).resize(CARROT_SIZE, Image.ANTIALIAS)
        self.collectible_carrot_image = ImageTk.PhotoImage(self.collectible_carrot_source)

        # pozicie panelov
        self.command_panel_coord_x0 = 0
        self.command_panel_coord_y0 = 0
        self.command_panel_coord_x1 = self.background_image.width()
        self.command_panel_coord_y1 = SCREEN_HEIGHT - self.background_image.height()

        self.main_panel_coord_x0 = self.command_panel_coord_x1
        self.main_panel_coord_y0 = 0
        self.main_panel_coord_x1 = self.playground.winfo_width()
        self.main_panel_coord_y1 = self.playground.winfo_height()

        self.scene_panel_coord_x0 = 0
        self.scene_panel_coord_y0 = self.command_panel_coord_y1
        self.scene_panel_coord_x1 = self.command_panel_coord_x1
        self.scene_panel_coord_y1 = self.playground.winfo_height()

        # pozicia pre obrazok pozadia
        self.scene_panel_coord_x_center = self.background_image.width() / 2
        self.scene_panel_coord_y_center = self.background_image.height() / 2 + self.command_panel_coord_y1

        self.set_graphical_elements()
        self.define_level()

    def define_level(self):
        # print(LEVELS[self.level])
        item = LEVELS[self.level]
        carrot_count = item[1]
        for i in range(item[0]):
            self.hills_array.append(None)

        while carrot_count > 0:
            r = random.randrange(1, item[0])
            if self.hills_array[r] is None:
                self.hills_array[r] = True
                carrot_count -= 1
        self.set_hills_and_tractor()


    def configure_main_window(self):
        self.title(APP_NAME)
        self.iconbitmap(default=HEAD_ICON)
        self.minsize(width=SCREEN_WIDTH, height=SCREEN_HEIGHT)
        self.geometry(INITIAL_SIZE_AND_POSITION)
        # self.state(Constants.INITIAL_STATE)

    def set_graphical_elements(self):
        self.playground.create_rectangle(self.command_panel_coord_x0, self.command_panel_coord_y0,
                                         self.command_panel_coord_x1, self.command_panel_coord_y1,
                                         fill=BACKGROUND_COLOR, outline='')
        self.crete_command_box()

        self.playground.create_rectangle(self.main_panel_coord_x0, self.main_panel_coord_y0,
                                         self.main_panel_coord_x1, self.main_panel_coord_y1,
                                         fill=BACKGROUND_COLOR, outline='')

        self.playground.create_text(TEXT_POSITION_1, text='ZBIERANIE', font=FONT_TYPE_3)
        self.playground.create_text(TEXT_POSITION_2, text='MRKVY', font=FONT_TYPE_3)

        self.playground.create_text(TEXT_POSITION_3, text=LEVEL.format('1'), font=FONT_TYPE_1)
        self.playground.create_text(TEXT_POSITION_2, text='MRKVY', font=FONT_TYPE_3)

        self.background_image_id = self.playground.create_image((self.scene_panel_coord_x_center,
                                                                 self.scene_panel_coord_y_center),
                                                                image=self.background_image)


        self.playground.create_rectangle(START_BUTTON_POSITION, fill='#35A0A4', outline='#3C3C3C', width = 3)
        self.playground.create_rectangle(RESTART_BUTTON_POSITION, fill='#35A0A4', outline='#3C3C3C', width = 3)

        self.playground.create_text((850, 275), text=START, font=FONT_TYPE_4)
        self.playground.create_text((945, 275), text=RESTART, font=FONT_TYPE_4)

        self.create_collect_button()
        self.create_forward_button()
        self.create_collect_button()
        self.create_forward_button()

        self.playground.create_text((900, 510), text=CARROTS_COUNT + ':', font=FONT_TYPE_2)
        self.playground.create_text((900, 550), text='0/3', font=FONT_TYPE_2)


    def set_hills_and_tractor(self):
        # spravit pocitanie kde sa ma zacat vykreslovat
        # o to x sa bude posuvat aj traktor
        # x, y = daco, daco
        x = 800 // len(self.hills_array)
        # print(len(self.hills_array))
        print('x kde idem vykreslit traktor', x)
        self.tractor_image_id = self.playground.create_image((x, 410), image=self.vehicle_image, tag='tractor')
        # self.rec = self.playground.create_rectangle(0, 450, 800, 470, fill='red')
        for i in range(len(self.hills_array)):
            # print(i)
            if self.hills_array[i] == True:
                print('x kde idem vykreslit mrkvu', x)
                self.collectible_carrot_image_id = self.playground.create_image((x, 450),
                                                                                image=self.collectible_carrot_image,
                                                                                tag='carrot')
            print('x kde idem vykreslit kopec', x)
            self.hill_image_id = self.playground.create_image((x, 520), image=self.hill_image)
            x += 150

    def create_image(self, center_x, center_y, _tag=None):
        image_id = self.playground.create_image((center_x, center_y))
        img = None
        if _tag == 'collect':
            _tag = _tag + str(image_id)
            img = self.collect_command_image
        if _tag == 'forward':
            _tag = _tag + str(image_id)
            img = self.forward_command_image
        self.playground.itemconfig(image_id, tag=_tag, image=img)

        return image_id

    def create_collect_button(self):
        return self.create_image(850, 400, 'collect')

    def create_forward_button(self):
        return self.create_image(950, 400, 'forward')

    def crete_command_box(self, count=4):
        size = COMMAND_BOX_SIZE
        x0, y0 = COMMAND_BOX_START_POSITION
        x1, y1 = x0 + size, y0 + size
        for index in range(count):
            command_item = CommandItem(self.playground, index)
            command_item.draw(x0, y0, x1, y1)
            self.commands_list.append(command_item)
            x0 += size
            x1 += size

    def print_commands_list(self):
        array = list()
        for item in self.commands_list:
            array.append([item.command_id, item.command_type])
        print(array)

    def sort_commands_in_box(self, event):
        is_shift_needed = False
        new_pos = None
        old_pos = None
        print("pred", self.obj_id)
        self.print_commands_list()
        print("................................")
        for index in range(len(self.commands_list)):
            item = self.commands_list[index]
            if item.box_coords[0] <= event.x <= item.box_coords[2] and \
                                    item.box_coords[1] <= event.y <= item.box_coords[3]:
                new_pos = index
                print("is shift neede? ", item.command_id, self.obj_id)
                if item.command_id and item.command_id != self.obj_id:
                    is_shift_needed = True

            elif item.command_tag == self.obj_tag:
                old_pos = index

        if old_pos is not None:
            dragged_item = copy(self.commands_list[old_pos])
            self.commands_list[old_pos].remove_command()
            print("dragged: " + dragged_item.command_type)

            print((old_pos != new_pos), is_shift_needed)
            is_shift_needed = True
            if (old_pos != new_pos) and is_shift_needed:
                print("eeeeeeeeeeeeeeeeeeeeeeeee", new_pos+1)
                for index in range(len(self.commands_list)-1, new_pos+1, -1):
                    item = self.commands_list[index]
                    item.command_id = self.commands_list[index - 1].command_id
                    item.command_tag = self.commands_list[index-1].command_tag
                    item.command_type = self.commands_list[index-1].command_type
                    self.playground.update()
                    if item.command_id:
                        self.playground.move(item.command_id, -COMMAND_BOX_SIZE, 0)
                        self.playground.update()

            self.commands_list[new_pos].command_tag = dragged_item.command_tag
            self.commands_list[new_pos].command_type = dragged_item.command_type

        # if old_pos and (old_pos != new_pos):
        #     self.commands_list[new_pos].command_tag, self.commands_list[old_pos].command_tag = \
        #         self.commands_list[old_pos].command_tag, self.commands_list[new_pos].command_tag
        #
        #     self.commands_list[new_pos].command_type, self.commands_list[old_pos].command_type = \
        #         self.commands_list[old_pos].command_type, self.commands_list[new_pos].command_type


        # for item in self.commands_list:
        #     if item.position_in_sequence == new_pos:

            # if pos:
            #     command_item.position_in_sequence += 1
            #     self.playground.move(self.obj_tag, COMMAND_BOX_SIZE, 0)

        print("po")
        self.print_commands_list()
        print(old_pos, new_pos)
        self.playground.update()

    def remove_item_from_commands(self):
        for item in self.commands_list:
            if item.command_tag == self.obj_tag:
                self.playground.delete(self.obj_id)
                item.remove_command()

    def remove(self, event):
        self.obj_id = event.widget.find_closest(event.x, event.y)[0]
        self.obj_tag = self.playground.gettags(event.widget.find_closest(event.x, event.y))[0]
        self.remove_item_from_commands()

    def check_buttons(self, event):
        if START_BUTTON_POSITION[0] <= event.x <= START_BUTTON_POSITION[2] and \
                                START_BUTTON_POSITION[1] <= event.y <= START_BUTTON_POSITION[3]:
                self.start_tractor_move()

        elif RESTART_BUTTON_POSITION[0] <= event.x <= RESTART_BUTTON_POSITION[2] and \
                                RESTART_BUTTON_POSITION[1] <= event.y <= RESTART_BUTTON_POSITION[3]:
                # self.restart()
            print('restart clilck')

    def click(self, event):
        self.will_drag = False
        self.check_buttons(event)
        self.obj_id = event.widget.find_closest(event.x, event.y)[0]
        if self.obj_id:
            self.obj_tag = self.playground.gettags(event.widget.find_closest(event.x, event.y))[0]
        if 'collect' in self.obj_tag or 'forward' in self.obj_tag:
            self.playground.lift(self.obj_id)
        self.initial_coords = self.playground.coords(self.obj_id)
        self.ex, self.ey = event.x, event.y

    def drag(self, event):
        self.will_drag = True
        if self.obj_tag == ('collect' + str(self.obj_id)) or self.obj_tag == ('forward'+ str(self.obj_id)):
            self.playground.move(self.obj_tag, event.x - self.ex, event.y - self.ey)
            self.ex, self.ey = event.x, event.y

    def check_command_in_list(self, pos):
        first_empty_position = None
        for item in self.commands_list:
            if self.obj_id == item.command_id:
                item.remove_command()
            if item.command_id is None and (first_empty_position is None or item.position_in_sequence < pos):
                first_empty_position = item.position_in_sequence

        return first_empty_position


    def drop(self, event):
        if self.will_drag is True:
            if self.obj_tag is not "current":
                for i in range(len(self.commands_list)):
                    command_item = self.commands_list[i]

                    if command_item.box_coords[0] <= event.x <= command_item.box_coords[2] and \
                                            command_item.box_coords[1] <= event.y <= command_item.box_coords[3]:

                        first_empty_position = self.check_command_in_list(i)

                        x, y = command_item.box_coords[0] + COMMAND_BOX_SIZE / 2,\
                               command_item.box_coords[1] + COMMAND_BOX_SIZE / 2

                        if first_empty_position is None:
                            print(first_empty_position)
                            return

                        elif first_empty_position < i:
                            condition = (0,i,1)
                            step = [1, 0, 1]
                            print("eeeeeee")
                            if command_item.command_id:
                                for j in range(first_empty_position, i):
                                    print("eoooooo")
                                    item = self.commands_list[j]
                                    item.command_id = self.commands_list[j+1].command_id
                                    item.command_tag = self.commands_list[j+1].command_tag
                                    item.command_type = self.commands_list[j+1].command_type
                                    if item.command_id:
                                        self.playground.move(item.command_id, -COMMAND_BOX_SIZE, 0)
                                    self.commands_list[j+1].remove_command()
                                    self.playground.update()

                        elif first_empty_position > i:
                            condition = (len(self.commands_list) - 1, i, -1)
                            step = [0, -1, -1]

                            if command_item.command_id:
                                for j in range(first_empty_position, i, -1):
                                    print(i-1, len(self.commands_list)-1)
                                    item = self.commands_list[j]
                                    item.command_id = self.commands_list[j-1].command_id
                                    item.command_tag = self.commands_list[j-1].command_tag
                                    item.command_type = self.commands_list[j-1].command_type
                                    if item.command_id:
                                        self.playground.move(item.command_id, COMMAND_BOX_SIZE, 0)
                                    self.commands_list[j-1].remove_command()
                                    self.playground.update()

                        self.playground.coords(self.obj_id, x, y)
                        self.print_commands_list()

                        command_item.command_tag = self.obj_tag
                        command_item.command_coords = (x, y)
                        command_item.command_id = self.obj_id

                        if self.obj_tag == ('collect' + str(self.obj_id)):
                            command_item.command_type = 'collect'
                            self.create_collect_button()
                        if self.obj_tag == ('forward'+ str(self.obj_id)):
                            command_item.command_type = 'forward'
                            self.create_forward_button()
                        self.print_commands_list()
                        break
                    else:
                        if not self.obj_tag == "current":
                            self.playground.coords(self.obj_id, self.initial_coords[0],
                                                   self.initial_coords[1])

    def image_scale(self):
        return
        # skaluj !!!!!
        # responzivita - kontroluj, ci sa obe velkosti zmenili, ak len jedna neskaluj, ak obe, skaluj
        # self.scene_image_source = self.scene_image_source.resize((250, 250), Image.ANTIALIAS)
        # self.scene_image = ImageTk.PhotoImage(self.scene_image_source)
        # self.playground.itemconfig(self.scene_image_id, image=self.scene_image)

    def start_tractor_move(self):
        print('toto je commands list', self.commands_list)
        for i in range(len(self.commands_list)):
            if self.commands_list[i].command_type == 'forward':
                self.tractor_start_x = self.playground.coords('tractor')[0]
                # self.playground.move('tractor', 150, 0)
                # for j in range(150):
                #     self.playground.move('tractor', 1, 0)
                self.commands_list[i].change_state(1)
                self.tractor_move()
                self.commands_list[i].change_state(2)
                print('pohol sa o forward')
            elif self.commands_list[i].command_type == 'collect':
                self.commands_list[i].change_state(1)
                print('skusil som zobrat mrkvu')
                self.try_pickup_carrot()
                self.commands_list[i].change_state(2)

    def tractor_move(self):
        while self.playground.coords('tractor')[0] < self.tractor_start_x + 150:
            # namiesto 150 bude self.step ktory sa bude generovat podla poctu kopcov
            self.playground.move('tractor', 1, 0)
            # self.playground.after(30, self.tractor_move)
            self.playground.update()
            sleep(0.01)

    def try_pickup_carrot(self):
        if self.playground.coords('tractor')[0] == self.playground.coords('carrot')[0]:
            print('zdvihol si mrkvu')
            self.playground.delete('carrot')
            self.playground.update()
            sleep(0.5)
        else:
            print('nezdvihol si mrkvu')


if __name__ == '__main__':
    mw = Playground()
    mw.mainloop()
