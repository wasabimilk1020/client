import win32gui
import utils
import serial_comm
import time

ERR_MSG = 0
STATUS_MSG = 1

def mainLoop(sio, btn_func, func_data, id_handle, btn_name):
  dict_length=len(id_handle)-1
  for idx, (id, handle) in enumerate(id_handle.items()):
    character_name=id
    if win32gui.IsWindow(handle):
      sio.emit("logEvent",[f"{btn_name} 시작", character_name, STATUS_MSG])

      utils.getWindow(handle) #윈도우 얻음
      #절전모드 해제 
      if btn_name != "status_check_button":
        dragValues={'fromStartX':900, 'toStartX':1015,'fromStartY':590,'toStartY':620,'fromEndX':860, 'toEndX':1000,'fromEndY':325,'toEndY':345}
        serial_comm.mouseDrag(dragValues)
        time.sleep(2)   #실제로는 열렸는지 확인하는 코드 넣어야됨
      result=btn_func(sio, func_data, btn_name, character_name) #result[0]=성공여부, result[1]=메세지
      message=result[1]

      if result[0]==0:
        sio.emit("logEvent",[message, character_name, ERR_MSG])
      elif result[0]==1:  #일반루틴 완료메세지
        sio.emit("logEvent",[f"{btn_name} 완료", character_name, STATUS_MSG])
        #절전모드
        serial_comm.keyboard('g')
        serial_comm.randClick(960,535,20,20,1)
      elif result[0]==2:  #statusChk 완료메세지
        sio.emit("logEvent",[f"{message} 완료", character_name, STATUS_MSG])
      elif result[0]==3:  #diamond 완료메세지
        diamond=message
        data=[]
        data.append(diamond)
        data.append(character_name)
        sio.emit("get_diamond",data)
        sio.emit("logEvent",["다이아몬드 완료", character_name, STATUS_MSG])
        #절전모드
        serial_comm.keyboard('g')
        serial_comm.randClick(960,535,20,20,1)
      if idx==dict_length:
        sio.emit("stop_animation",btn_name)
    else:
      print("핸들 없음",handle)
      sio.emit("logEvent",["윈도우 없음", character_name, ERR_MSG])
      continue

      
      
      


    