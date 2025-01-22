def mainLoop(sio, btn_func, func_data, id_handle, btn_name):
  for id, handle in id_handle.items():
    character_name=id
    btn_func(sio, func_data, character_name)
    