
import cv2
import numpy as np
import json
import src.PoseDetermining as PoseDetermining
from collections import OrderedDict


cap = cv2.VideoCapture("../image/Test2.mp4")

# 옵션 설명 http://layer0.authentise.com/segment-background-using-computer-vision.html
#fgbg = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=100, detectShadows=0)
fgbg = cv2.createBackgroundSubtractorKNN(history=500, dist2Threshold=400, detectShadows=0)

group_data = OrderedDict()
Data_set = OrderedDict()

number = 0
comp = (0, 0)
prior_coor = (1, 0)

while True:
#while (number < 100):
    ret, frame = cap.read()

    width = frame.shape[1]
    height = frame.shape[0]

    frame = cv2.resize(frame, (int(width * 0.5), int(height * 0.5)))

    fgmask = fgbg.apply(frame)

    nlabels, labels, stats, centroids = cv2.connectedComponentsWithStats(fgmask)

    for index, centroid in enumerate(centroids):
        if stats[index][0] == 0 and stats[index][1] == 0:
            continue
        if np.any(np.isnan(centroid)):
            continue

        x, y, width, height, area = stats[index]
        centerX, centerY = int(centroid[0]), int(centroid[1])

        # 날개 조각이나 잔상 등 이상한 부분 처리 - 이전 프레임보다 훨씬 작은 프레임은 무시
        if (width * height < 0.5 * comp[0] * comp[1]):
            continue
        comp = (width, height)

        if area > 10:
            dst1 = fgmask.copy()
            dst1 = fgmask[y - 5:y + height + 5, x - 5:x + width + 5]
            dst2 = frame.copy()
            cv2.circle(dst2, (centerX, centerY), 1, (0, 255, 0), 2)
            cv2.rectangle(frame, (x, y), (x + width, y + height), (0, 0, 255))
            cv2.imwrite('../test/birds%d.png' % number, dst1)

            # theta 구하기
            theta_x = centerX - prior_coor[0]
            theta_y = centerY - prior_coor[1]
            if theta_x == 0:
                continue
            theta = theta_y / theta_x
            prior_coor = (centerX, centerY)  # 현재 점으로 업데이트

#            print(theta)
#            file = '../test/birds%d.png' % number
#            pose = PoseDetermining.read_vectors(file, theta)
#            print("Pose는 ", pose)

            number = number + 1

    #cv2.imshow('mask', fgmask)
    #cv2.imshow('frame', frame)

    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break

print()
print(stats[0][0], stats[0][1], stats[0][2], stats[0][3], stats[0][4])
print(stats[1][0], stats[1][1], stats[1][2], stats[1][3], stats[1][4])

cap.release()
cv2.destroyAllWindows()
