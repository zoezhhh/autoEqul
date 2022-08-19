import pyautogui as pg
import time
from config import *
from utils import *


def secure_enters(n=ENTERS):
    pg.press('enter', presses=n, interval=KEYBOARD_INTERVAL)
    time.sleep(STEP_INTERVAL)


def save():
    pg.hotkey("ctrl", "s")
    time.sleep(STEP_INTERVAL)
    secure_enters()


def quit():
    pg.hotkey("alt", "f4")
    time.sleep(STEP_INTERVAL)
    secure_enters()


def wait_for_excel():
    time.sleep(3)
    excel = []
    while not excel:
        excel = pg.getWindowsWithTitle("Excel")
        time.sleep(RETRY_INTERVAL)



class EqulGUI:

    def __init__(self, title=WINDOW_TITLE):
        self.title = title
        self.window = pg.getWindowsWithTitle(self.title)[0]
        self.cur_tag = 0
        self.cur_tab = 0
        self.section = 0
        self.checkbox_status = dict()

    def reload_window(self):
        self.window = pg.getWindowsWithTitle(self.title)[0]

    def focus_window(self):
        region = self.window.box
        pg.click(region.left + region.width // 2, region.top + 10)

    def locate_image(self, image, max_retries=MAX_RETRIES):
        for i in range(max_retries):
            located = pg.locateCenterOnScreen(image, confidence=IMAGE_CONFIDENCE, grayscale=GRAYSCALE)
            if located:
                return located
            time.sleep(RETRY_INTERVAL)

        return

    def switch_field(self, n):
        if n > 0:
            pg.press('tab', presses=n, interval=KEYBOARD_INTERVAL)
        elif n < 0:
            with pg.hold('shift'):
                pg.press('tab', presses=abs(n), interval=KEYBOARD_INTERVAL)
        self.cur_tab += n
        time.sleep(STEP_INTERVAL)

    def switch_tag(self, n):
        if n > 0:
            pg.press('right', presses=n, interval=KEYBOARD_INTERVAL)
        elif n < 0:
            pg.press('left', presses=abs(n), interval=KEYBOARD_INTERVAL)
        self.cur_tag += n
        self.cur_tab = 0
        time.sleep(STEP_INTERVAL)

    def goto_tagbar(self):
        self.switch_field(3)
        self.switch_field(-self.cur_tab - NTAB_TAGBAR - NTAB_SECURE)
        time.sleep(STEP_INTERVAL)
        self.switch_field(NTAB_TAGBAR)
        self.cur_tab = 0
        time.sleep(STEP_INTERVAL)

    def reset_tag(self):
        self.goto_tagbar()
        time.sleep(STEP_INTERVAL)
        self.switch_tag(-self.cur_tag)
        time.sleep(STEP_INTERVAL)

    def set_checkbox(self, name, target):
        print(f"Setting Checkbox {name} to {target}")
        if name in self.checkbox_status:
            is_checked = self.checkbox_status[name]
        else:
            img_path = IMG_PATH[name]
            is_checked = bool(self.locate_image(img_path))
        print(f"{name} is currently {is_checked}")
        if target != is_checked:
            print("Press Space")
            pg.press(" ")
        self.checkbox_status[name] = target
        time.sleep(STEP_INTERVAL)

    def fill_field(self, field, row_data):
        ntag = Tags[field["Novinsoft Field"]["tag"]]
        ntab = field["Novinsoft Field"]["#tab"]

        if ntag == self.cur_tag:
            self.switch_field(ntab - self.cur_tab)
        else:
            self.goto_tagbar()
            self.switch_tag(ntag - self.cur_tag)
            self.switch_field(ntab)

        self.cur_tag = ntag
        self.cur_tab = ntab
        time.sleep(STEP_INTERVAL)

        name = field["Novinsoft Field"]["field"]
        ftype = field["Novinsoft Field"]["type"]
        value = row_data[field["Excel colname"]]
        print(f"Setting {name} to {value}...")
        converted = convert(name, ftype, value)

        if ftype == INPUT_FIELD:
            pg.write(converted, interval=KEYBOARD_INTERVAL)

        if ftype == DROPDOWN_LIST:
            pg.press(converted)

        if ftype == CHECKBOX:
            self.set_checkbox(name, converted)
            if converted and "Folded Fields" in field:
                for folded in field["Folded Fields"]:
                    self.fill_field(folded, row_data)
                    time.sleep(STEP_INTERVAL)

        secure_enters()

    def auto_complete(self, row_data):
        self.reset_tag()
        for field in InputMapping:
            self.fill_field(field, row_data)
            time.sleep(STEP_INTERVAL)
        self.reset_tag()
        time.sleep(STEP_INTERVAL)


    def spreadsheet(self):
        if self.section == 0:
            pg.press("f10")
            time.sleep(STEP_INTERVAL)
            secure_enters()
        self.section = 1

    def previous_section(self):
        if self.section == 1:
            pg.hotkey("alt", "left")
            time.sleep(STEP_INTERVAL)
            secure_enters()
        self.section = 0

    def export_to_excel(self, icon=IMG_PATH["export to Excel"]):
        self.spreadsheet()
        located = self.locate_image(icon)
        time.sleep(STEP_INTERVAL)
        pg.click(located)
        time.sleep(STEP_INTERVAL)
        wait_for_excel()
        time.sleep(STEP_INTERVAL)
        save()
        time.sleep(STEP_INTERVAL)
        quit()
        time.sleep(STEP_INTERVAL)
        self.previous_section()

