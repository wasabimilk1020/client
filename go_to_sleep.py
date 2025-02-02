import serial_comm
import check_hunting
import utils

ERR_MSG = 0
STATUS_MSG = 1

def go_to_sleep_and_huntingChk(btn_name, character_name, sio):
  for i in range(20):
    serial_comm.keyboard('g')
    result=utils.searchImg('sleepChk.png', beforeDelay=1, afterDelay=0,  chkCnt=2, _region=(850, 455, 200, 200))  
    if result ==1:
      break

  serial_comm.randClick(960,535,20,20,2.5)
  value=check_hunting.checkHunting()  #value=성공 시="자동 사냥 중" or "스케줄 자동 진행 중", 실패 시=0
  print("value: ",value)
  if value!=0:
    sio.emit("logEvent",[f"{btn_name}, {value} 완료", character_name, STATUS_MSG])
  else:
    sio.emit("logEvent",["멈춰있음", character_name, ERR_MSG])