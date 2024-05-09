import time

from pynput.keyboard import Controller, Key

keyboard = Controller()

SPECIAL_KEYS = {
    'alt': Key.alt,
    'alt_l': Key.alt_l,
    'alt_r': Key.alt_r,
    'alt_gr': Key.alt_gr,
    'backspace': Key.backspace,
    'caps_lock': Key.caps_lock,
    'cmd': Key.cmd,
    'cmd_l': Key.cmd_l,
    'cmd_r': Key.cmd_r,
    'ctrl': Key.ctrl,
    'ctrl_l': Key.ctrl_l,
    'ctrl_r': Key.ctrl_r,
    'delete': Key.delete,
    'down': Key.down,
    'end': Key.end,
    'enter': Key.enter,
    'esc': Key.esc,
    'f1': Key.f1,
    'f2': Key.f2,
    'f3': Key.f3,
    'f4': Key.f4,
    'f5': Key.f5,
    'f6': Key.f6,
    'f7': Key.f7,
    'f8': Key.f8,
    'f9': Key.f9,
    'f10': Key.f10,
    'f11': Key.f11,
    'f12': Key.f12,
    'f13': Key.f13,
    'f14': Key.f14,
    'f15': Key.f15,
    'f16': Key.f16,
    'f17': Key.f17,
    'f18': Key.f18,
    'f19': Key.f19,
    'f20': Key.f20,
    'home': Key.home,
    'insert': Key.insert,
    'left': Key.left,
    'menu': Key.menu,
    'num_lock': Key.num_lock,
    'page_down': Key.page_down,
    'page_up': Key.page_up,
    'pause': Key.pause,
    'print_screen': Key.print_screen,
    'right': Key.right,
    'scroll_lock': Key.scroll_lock,
    'shift': Key.shift,
    'shift_l': Key.shift_l,
    'shift_r': Key.shift_r,
    'space': Key.space,
    'tab': Key.tab,
    'up': Key.up,
    'media_play_pause': Key.media_play_pause,
    'media_previous': Key.media_previous,
    'media_next': Key.media_next,
}


def send_key(key):
    """input the key in to the user computer"""
    if key in SPECIAL_KEYS:
        keyboard.press(SPECIAL_KEYS[key])
        keyboard.release(SPECIAL_KEYS[key])
    else:
        keyboard.press(key)
        keyboard.release(key)
