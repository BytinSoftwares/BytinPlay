import pafy
import vlc
import re
from urllib.request import urlopen
from lxml.html import parse
import requests
import urllib.request

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import ctypes
from ctypes.wintypes import HWND, LPWSTR, UINT

_user32 = ctypes.WinDLL('user32', use_last_error=True)

_MessageBoxW = _user32.MessageBoxW
_MessageBoxW.restype = UINT  # default return type is c_int, this is not required
_MessageBoxW.argtypes = (HWND, LPWSTR, LPWSTR, UINT)

MB_OK = 0
MB_OKCANCEL = 1
MB_YESNOCANCEL = 3
MB_YESNO = 4

IDOK = 1
IDCANCEL = 2
IDABORT = 3
IDYES = 6
IDNO = 7


def MessageBoxW(hwnd, text, caption, utype):
    result = _MessageBoxW(hwnd, text, caption, utype)
    if not result:
        raise ctypes.WinError(ctypes.get_last_error())
    return result

def urlValidate(x):
    return bool(re.match(
        r"(https?|ftp)://" # protocol
        r"(\w+(\-\w+)*\.)?" # host (optional)
        r"((\w+(\-\w+)*)\.(\w+))" # domain
        r"(\.\w+)*" # top-level domain (optional, can have > 1)
        r"([\w\-\._\~/]*)*(?<!\.)" # path, params, anchors, etc. (optional)
    , x))

def playVid(url, pause=False):
    if urlValidate(url) is True:
        video = pafy.new(url)
        best = video.getbestaudio()
        playurl = best.url
        Instance = vlc.Instance()
        global player
        player = Instance.media_player_new()
        Media = Instance.media_new(playurl)
        Media.get_mrl()
        player.set_media(Media)
        player.play()

def PauseVid():
    global player
    player.pause()

def unPause():
    global player
    player.play()

def StopVid():
    global player
    player.stop()

def title(url):
    page = urlopen(url)
    p = parse(page)
    return(p.find(".//title").text)

def check():
    if int(requests.get('https://raw.githubusercontent.com/BytinSoftwares/BytinPlay/updater/ver.txt').text) > 101:
        try:
            result = MessageBoxW(None, "An update is available, do you want to download it?", "BytinPlay Updater", MB_YESNO)
            if result == IDYES:
                urllib.request.urlretrieve('https://github.com/BytinSoftwares/bytinPlay/raw/updater/setup.exe', 'setup.exe')
                import os
                os.startfile("updater.exe")
                exit()
            elif result == IDNO:
                return
            else:
                return
        except WindowsError as win_err:
            print("An error occurred:\n{}".format(win_err))
    else:
        return False
