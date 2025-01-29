import utils
import time
import re

x, y, width, height = 810, 660, 295, 65 #자동 사냥 범위
config="--psm 7 -c preserve_interword_spaces=1"

def checkHunting():
  for i in range(5):
    text=utils.capture_text_from_region(x, y, width, height, config)
    clean_text=re.sub(r"^\s+|\s+$", "", text)  # 정규식으로 앞뒤 공백 제거
    if clean_text == "스케줄 자동 진행 중" or clean_text == "자동 사냥 중" or clean_text=="스케줄 자동 정비 진행 중":
      return clean_text
    time.sleep(0.3)
  return 0