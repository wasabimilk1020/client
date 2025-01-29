import pyautogui
import sys
import utils
import time
import check_hunting

value=check_hunting.checkHunting()  #value=성공 시="자동 사냥 중" or "스케줄 자동 진행 중", 실패 시=0
if value!=0:
    print("value: ",value)
else:
    print("멈춰있음")