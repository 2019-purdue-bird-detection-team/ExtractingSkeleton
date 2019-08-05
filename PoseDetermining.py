import math

def read_vectors():
     file = open("vectors.txt").read().split()
     c_x, c_y= (float)(file[0]), (float)(file[1])
     h_x, h_y= (float)(file[2]), (float)(file[3]) #머리
     t_x, t_y= (float)(file[4]), (float)(file[5]) #꼬리
     w1_x, w1_y= (float)(file[6]), (float)(file[7])
     w2_x, w2_y= (float)(file[8]), (float)(file[9])

     vec= (h_x-c_x, h_y-c_y) #기준벡터: 머리-중심
     vec1= (w1_x-c_x, w1_y-c_y) #날개벡터 1
     vec2= (w2_x-c_x, w2_y-c_y) #날개벡터 2

     if (vec==(0,0)): #for front-rear frame
          read_front_vectors(vec1, vec2)
          return
     
     isClockWise = 1 #시계방향
     if (h_x > t_x): isClockWise= 0 #반시계방향
     
     theta1= CalAngleBetweenTwoPoints(vec, vec1, isClockWise)
     theta2= CalAngleBetweenTwoPoints(vec, vec2, isClockWise)
     print(theta1, theta2)

     if (theta1<180 and theta2<180):
          pose=0
     elif (theta1>180 and theta2>180):
          pose=1
     elif (theta1==0 and theta2==0):
          pose=3
     else:
          pose=2
          
def read_front_vectors(vec1, vec2):
     if (vec1[1]>0):
          pose=0
     else:
          pose=1

def CalAngleBetweenTwoPoints(h, w, isClockWise):
     rotated= [0,0] #h vector will be rotated 90 degree

     if (isClockWise): #h벡터로부터 시계방향 회전 (머리-중심-꼬리 사진)
          rotated[0]= h[1]
          rotated[1]= -h[0]
     else: #h벡터로부터 반시계방향회전 (꼬리-중심-머리 사진)
          rotated[0]= -h[1]
          rotated[1]= h[0]

     hVecsize= math.sqrt(h[0]**2 + h[1]**2)
     wVecsize= math.sqrt(w[0]**2 + w[1]**2)
     
     fAng= math.degrees(math.acos((rotated[0]*w[0] + rotated[1]*w[1]) / (hVecsize * wVecsize)))

     if (fAng>90): #if True, it means the angle between vector h and w is bigger than 180 
          return 360- math.degrees(math.acos((h[0]*w[0] + h[1]*w[1]) / (hVecsize * wVecsize)))
     else:
          return math.degrees(math.acos((h[0]*w[0] + h[1]*w[1]) / (hVecsize * wVecsize)))
     
read_vectors()
