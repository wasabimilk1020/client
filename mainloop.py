ERR_MSG = 0
STATUS_MSG = 1

def mainLoop(sio, btn_func, func_data, id_handle, btn_name):
  dict_length=len(id_handle)-1
  for idx, (id, handle) in enumerate(id_handle.items()):
    # result_window=get_window(handle)
    # if result_window is not None: #정확히 없을 때 None이 나오는지 모름 확인해보고 넣어주자
      character_name=id
      result=btn_func(sio, func_data, btn_name)
      if result==1:
        sio.emit("logEvent",[f"{btn_name} 실행", character_name, STATUS_MSG])
      elif result==0:
        sio.emit("logEvent",[f"{btn_name} 실패", character_name, ERR_MSG])
      if idx==dict_length:
        sio.emit("stop_animation",btn_name)
    # else:
    #   sio.emit("logEvent",["윈도우 없음", character_name, ERR_MSG])


    