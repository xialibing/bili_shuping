#高斯双边滤波，锐化
import cv2
import numpy as np
import os
import subprocess


path = "/home/bili/"  #路径
filename = "aoyi.mp4"  #需要转换视频文件名
outfilename = "aoyi4full.mp4"

vc = cv2.VideoCapture(path+filename) #读取视频文件

w = vc.get(cv2.CAP_PROP_FRAME_WIDTH) #视频宽
w = int(w/3)

h = vc.get(cv2.CAP_PROP_FRAME_HEIGHT) #视频高

fps = vc.get(cv2.CAP_PROP_FPS) #视频帧率

#写视频文件
fourcc = cv2.VideoWriter_fourcc(*"mp4v")
outname = "aoyi4out.mp4" #此视频文件无声，完成后可以删除
vw4 = cv2.VideoWriter(path+outname, fourcc, int(fps*2), (int(w*2.4), int(h*2.4)), isColor=True)

while vc.isOpened():
  retval, image = vc.read()
  if not retval:
    break
  img = np.zeros((int(h), int(w), 3))
  img = image[:, w:w+w, :]
  img4 = cv2.resize(img, dsize=(int(w*2.4), int(h*2.4)), interpolation=cv2.INTER_CUBIC)
  print(image.shape, img.shape, img4.shape)
  
  #几个卷积核可以不同效果
  kernel = np.reshape(np.array([0, -1, 0, -1, 5, -1, 0, -1, 0]), (3, 3))
  #kernel = np.reshape(np.array([-1, -2, -1, -2, 13, -2, -1, -2, -1]), (3, 3))
  #kernel = np.reshape(np.array([-1, -1, -1, -1, 9, -1, -1, -1, -1]), (3, 3))
  #kernel = np.reshape(np.array([0, 0, -1, 0, 0, 0, -1, -2, -1, 0, -1, -2, 17, -2, -1, 0, -1, -2, -1, 0, 0, 0, -1, 0, 0]), (5, 5))
  img4 = cv2.filter2D(img4, -1, kernel)
  
  vw4.write(img4)
  vw4.write(img4)
  
  #cv2.imshow("xiao", img)
  key = cv2.waitKey(0)
  if key == ord("q"):
    break

vc.release()
vw4.release()
cv2.destroyAllWindows()

#音频文件名
m4aname = "aoyiout.m4a"
#提取视频文件的音频
subprocess.run(["ffmpeg", "-i", path+filename, "-vn", "-codec", "copy", path+m4aname])  
#把提取音频文件和新视频文件合并
subprocess.run(["ffmpeg", "-i", path+outname, "-i", path+m4aname, "-c:v", "copy", "-c:a", "aac", "-strict", "experimental", path+outfilename])
exit()

