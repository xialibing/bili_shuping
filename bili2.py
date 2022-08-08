import os
from pathlib import Path 
import cv2
import numpy as np
import subprocess
import time
import multiprocessing as mp
from multiprocessing import Manager
import _thread

manager = Manager()

diclock = manager.Lock()

def shu(path):
  diclock.acquire()
  for key in dic.keys():
    if dic[key] == 0:
      dic[key] = 1
      filename = key
      print(filename)
      break
  else:
    diclock.release()
    return 0
  diclock.release()
  outfilename = filename.split(".")[0]+"4full.mp4"

  vc = cv2.VideoCapture(path+filename) #读取视频文件

  w = vc.get(cv2.CAP_PROP_FRAME_WIDTH) #视频宽
  w = int(w/3)

  h = vc.get(cv2.CAP_PROP_FRAME_HEIGHT) #视频高

  fps = vc.get(cv2.CAP_PROP_FPS) #视频帧率

  #写视频文件
  fourcc = cv2.VideoWriter_fourcc(*"mp4v")
  outname = filename.split(".")[0]+"4out.mp4" #此视频文件无声，完成后可以删除
  vw4 = cv2.VideoWriter(path+outname, fourcc, int(fps*2), (int(w*2.4), int(h*2.4)), isColor=True)

  while vc.isOpened():
    retval, image = vc.read()
    if not retval:
      break
    img = np.zeros((int(h), int(w), 3))
    img = image[:, w:w+w, :]
    img4 = cv2.resize(img, dsize=(int(w*2.4), int(h*2.4)), interpolation=cv2.INTER_CUBIC)
    print(filename, image.shape, img.shape, img4.shape)
  
    #几个卷积核可以不同效果
    kernel = np.reshape(np.array([0, -1, 0, -1, 5, -1, 0, -1, 0]), (3, 3))
    #kernel = np.reshape(np.array([-1, -2, -1, -2, 13, -2, -1, -2, -1]), (3, 3))
    #kernel = np.reshape(np.array([-1, -1, -1, -1, 9, -1, -1, -1, -1]), (3, 3))
    #kernel = np.reshape(np.array([0, 0, -1, 0, 0, 0, -1, -2, -1, 0, -1, -2, 17, -2, -1, 0, -1, -2, -1, 0, 0, 0, -1, 0, 0]), (5, 5))
    img4 = cv2.filter2D(img4, -1, kernel)
  
    vw4.write(img4)
    vw4.write(img4)
  
    #cv2.imshow("xiao", img)
    #key = cv2.waitKey(0)
    #if key == ord("q"):
      #break

  vc.release()
  vw4.release()
  cv2.destroyAllWindows()

  #音频文件名
  m4aname = filename.split(".")[0]+"out.m4a"
  #提取视频文件的音频
  subprocess.run(["ffmpeg", "-i", path+filename, "-vn", "-codec", "copy", path+m4aname])  
  #把提取音频文件和新视频文件合并
  subprocess.run(["ffmpeg", "-i", path+outname, "-i", path+m4aname, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", path+outfilename])
  subprocess.run(["rm", "-rf", path+m4aname]) 
  subprocess.run(["rm", "-rf", path+outname]) 
  subprocess.run(["mv", path+outfilename, path+"out/"])
  time.sleep(5)
  return 1


def jin(ti):
  time.sleep(ti)
  while True:
    if shu(path)==0:
      break

dic = manager.dict()
def t_dri(name):
  while True:
    fn = os.listdir(path)
    mp4lst = [i for i in fn if i.endswith(".mp4") and (i.split(".")[0]).find("out")==-1]
    for ifn in mp4lst:
      diclock.acquire()
      if dic.get(ifn, 100) == 100:
        dic[ifn] = 0
      diclock.release()
    time.sleep(60)

path = "/home/bili/jiaoben/"
def quan():
  _thread.start_new_thread(t_dri, ("thread",))
  time.sleep(30)
  arglst = [1, 1]
  for _ in mp.Pool().imap(jin, arglst):
    print("xxxx")

quan()


