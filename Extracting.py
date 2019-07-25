import cv2
import numpy as np
import math
from matplotlib import pyplot as plt

class Point2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y
  
img = cv2.imread('C:\\Users\\Yejin Kim\\Desktop\\bird.png',0)
edges = cv2.Canny(img,100,255)

#plt.subplot()
#plt.imshow(edges,cmap = 'gray')
#plt.show()

indices = np.where(edges != [0])
coordinates = zip(indices[0], indices[1])
count= len(indices[0])
print("count=",count)

x_cent=0
y_cent=0
x_axis=[]
y_axis=[]
for xp, yp in zip(indices[0], indices[1]):
    x_cent+=xp
    y_cent+=yp
    x_axis.append(xp)
    y_axis.append(yp)
    
x_cent/=count
y_cent/=count

c=[]
for xp, yp in zip(x_axis, y_axis):
    p1 = Point2D(x=x_cent, y=y_cent)    # 점1
    p2 = Point2D(x=xp, y=yp)    # 점2
    a = p2.x - p1.x    # 선 a의 길이
    b = p2.y - p1.y    # 선 b의 길이
    c.append(math.sqrt((a**2) + (b**2)))    # (a * a) + (b * b)의 제곱근을 구함

plt.plot(x_axis,c)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
