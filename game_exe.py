import win32gui
import client_utils

def start_game():
  handle=win32gui.FindWindow(None,"PURPLE")
  client_utils.getWindow(handle) #윈도우 얻음
  result=client_utils.searchImg('lineage_symbol.png',beforeDelay=0, afterDelay=0, _region=(0,0,1920,1080), accuracy=0.75)
  result=client_utils.searchImg('game_start_1.png',beforeDelay=2, afterDelay=0, _region=(0,0,1920,1080))
  result=client_utils.searchImg('purple_list_btn.png',beforeDelay=0, afterDelay=0, _region=(0,0,1920,1080))
  for i in range(5):
    result=client_utils.searchImg('game_start_2.png',beforeDelay=5, afterDelay=0, _region=(0,0,1920,1080))
    if result==0:
        break