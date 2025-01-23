ERR_MSG = 0
STATUS_MSG = 1

def mainLoop(sio, btn_func, func_data, id_handle, btn_name):
  for id, handle in id_handle.items():
    character_name=id
    result=btn_func(sio, func_data)
    if result==1:
      sio.emit("logEvent",[f"{btn_name} 실행", character_name, STATUS_MSG])
    elif result==0:
      sio.emit("logEvent",[f"{btn_name} 실패", character_name, ERR_MSG])

    