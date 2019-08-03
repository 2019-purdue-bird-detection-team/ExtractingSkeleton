import math

def read_vectors():
     file = open("vectors.txt").read().split()
     c_x, c_y= (float)(file[0]), (float)(file[1])
     h_x, h_y= (float)(file[4]), (float)(file[5]) #머리
     w1_x, w1_y= (float)(file[6]), (float)(file[7])
     w2_x, w2_y= (float)(file[8]), (float)(file[9])

     vec= (h_x-c_x, h_y-c_y)
     vec1= (w1_x-c_x, w1_y-c_y)
     vec2= (w2_x-c_x, w2_y-c_y)
     
     if (vec==(0,0)): #정면일 경우 처리
          read_front_vectors(vec1, vec2)
          return

     vec_size= math.sqrt(vec[0]**2+ vec[1]**2)
     vec1_size= math.sqrt(vec1[0]**2+ vec1[1]**2)
     vec2_size= math.sqrt(vec2[0]**2+ vec2[1]**2)

     theta1= math.degrees(math.acos((vec[0]*vec1[0]+ vec[1]*vec1[1])/(vec_size*vec1_size)))
     theta2= math.degrees(math.acos((vec[0]*vec2[0]+ vec[1]*vec2[1])/(vec_size*vec2_size)))


     if (theta1<180 and theta2<180):
          print("flying pose 1")
     elif (theta1>180 and theta2>180):
          print("flying pose 2")
     elif (theta1==0 and theta2==0):
          print("flying pose 4")
     else:
          print("flying pose 3")

def read_front_vectors(vec1, vec2):
     if (vec1[1]>0):
          print("flying pose 1")
     else:
          print("flying pose2")

read_vectors()
