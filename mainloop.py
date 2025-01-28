import win32gui
ERR_MSG = 0
STATUS_MSG = 1

def mainLoop(sio, btn_func, func_data, id_handle, btn_name):
  dict_length=len(id_handle)-1
  for idx, (id, handle) in enumerate(id_handle.items()):
    character_name=id
    if win32gui.IsWindow(handle):
      print("핸들 없음")
      sio.emit("logEvent",["윈도우 없음", character_name, ERR_MSG])
      break
    else:
      # get_window(handle)
      sio.emit("logEvent",[f"{btn_name} 시작", character_name, STATUS_MSG])

      #절전모드 해제 여기에
      result=btn_func(sio, func_data, btn_name, character_name) #result[0]=성공여부, result[1]=메세지
      message=result[1]

      if result[0]==0:
        sio.emit("logEvent",[message, character_name, ERR_MSG])
      elif result[0]==1:
        sio.emit("logEvent",[f"{btn_name} 완료", character_name, STATUS_MSG])
        #절전모드 여기에
      elif result[0]==2:
        sio.emit("logEvent",[f"{message} 완료", character_name, STATUS_MSG])
      if idx==dict_length:
        sio.emit("stop_animation",btn_name)
      
      


    