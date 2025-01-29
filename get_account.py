import time
import win32gui
import win32com.client
shell = win32com.client.Dispatch("WScript.Shell")
from serial_comm import *
import utils

# 현재 실행중인 윈도우 핸들 목록 가져오기
def get_lin2m_hwnd_list():
  lin2m_handle_list=[]  #린2m 핸들 리스트

  def callback(_hwnd, _result: list):
    title = win32gui.GetWindowText(_hwnd)
    if win32gui.IsWindowEnabled(_hwnd) and win32gui.IsWindowVisible(_hwnd) and title is not None and len(title) > 0:
      _result.append(_hwnd)
    return True
  hwnd_list = []  #윈도우 핸들 리스트트
  win32gui.EnumWindows(callback, hwnd_list)
  
  for hwnd in hwnd_list:
    title = win32gui.GetWindowText(hwnd)
    result = title.split(' ')[0].strip()
    if result == "리니지2M":
      lin2m_handle_list.append(hwnd)
  return lin2m_handle_list

def get_account_list(sio):
  account_dict={} #{"아이디":handle value}
  lin2m_handle_list=get_lin2m_hwnd_list()

  for lin2m_hwnd in lin2m_handle_list:
    # print("핸들 값",lin2m_hwnd)
    # startClick(0,0,0,0,0)
    # time.sleep(0.1)
    # shell.SendKeys('%')
    # try:
    #   win32gui.SetForegroundWindow(lin2m_hwnd)
    # except Exception as e:
    #   print(f"Error bringing window to foreground: {e}")
    utils.getWindow(lin2m_hwnd)
       
    dragValues={'fromStartX':900, 'toStartX':1015,'fromStartY':590,'toStartY':620,'fromEndX':860, 'toEndX':1000,'fromEndY':325,'toEndY':345}
    mouseDrag(dragValues)
    time.sleep(2)   #실제로는 열렸는지 확인하는 코드 넣어야됨

    keyboard('x')
    time.sleep(1)
    result=utils.searchImg('information.png',beforeDelay=1, afterDelay=1, _region=(1330, 225, 200, 100))
    if(result==0):
      print("정보 클릭 실패")
      return
    
    x, y, width, height = 1205, 330, 130, 45
    config="--psm 7 -c preserve_interword_spaces=1"
    # 문자 추출 실행
    for i in range(5):
      extracted_text = utils.capture_text_from_region(x, y, width, height, config)
      if extracted_text != "":
        print("extracted text: ",extracted_text)
        break
      else:
        print("실패!!@@!")
      time.sleep(1)
          
    name=extracted_text.split(' ')[0].strip()
    account_dict[name]=lin2m_hwnd
    print("name: ",name)    
    escKey() 
    #절전모드
    keyboard('g')
    randClick(960,535,20,20,1)
    sio.emit("logEvent",["어카운트 완료", name, 1])

  return account_dict
