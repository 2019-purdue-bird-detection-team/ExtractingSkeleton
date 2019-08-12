import math
import src.vector_extractor as v_e


def read_vectors():

     theta = 2.96706
     v = v_e.get_vectors(theta)
     center = v.center
     head = v.head
     tail = v.tail
     wing1 = v.wings[0]
     wing2 = v.wings[1]

     vec= (head.x-center.x, head.y-center.y) #기준벡터: 머리-중심
     vec1= (wing1.x-center.x, wing1.y-center.y) #날개벡터 1
     vec2= (wing2.x-center.x, wing2.y-center.y) #날개벡터 2

     if (vec==(0,0)): #for front-rear frame
          read_front_vectors(vec1, vec2)
          return
     
     isClockWise = 1 #시계방향
     if (head.x > tail.x): isClockWise= 0 #반시계방향
     
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
     elif (vec1[1]<0):
          pose=1
     else:
          pose=2

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
