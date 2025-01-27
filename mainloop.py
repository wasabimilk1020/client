ERR_MSG = 0
STATUS_MSG = 1

def mainLoop(sio, btn_func, func_data, id_handle, btn_name):
  dict_length=len(id_handle)-1
  for idx, (id, handle) in enumerate(id_handle.items()):
    # result_window=get_window(handle)
    # if result_window is not None: #정확히 없을 때 None이 나오는지 모름 확인해보고 넣어주자
      character_name=id
      sio.emit("logEvent",[f"{btn_name} 시작", character_name, STATUS_MSG])
      result=btn_func(sio, func_data, btn_name, character_name) #result[0]=성공여부, result[1]=메세지
      if result[0]==1:
        sio.emit("logEvent",[f"{btn_name} 완료", character_name, STATUS_MSG])
      elif result[0]==0:
        sio.emit("logEvent",[f"{result[1]}", character_name, ERR_MSG])
      if idx==dict_length:
        sio.emit("stop_animation",btn_name)
    # else:
    #   sio.emit("logEvent",["윈도우 없음", character_name, ERR_MSG])


    