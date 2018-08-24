import numpy as np
import cv2 as cv
from Human import Human

# 給各 100 位男女，隨機分配真實分數
list___men, list_women = [], []
list_2D_plane = [i for i in range(70)] #= np.ndarray(shape=(70, 70))
for i in range(len(list_2D_plane)):
    list_2D_plane[i] = [i for i in range(70)]
    for j in range(len(list_2D_plane[i])):
        rand_case = np.random.randint(0, 3)

        # python style switch-case
        list_2D_plane[i][j] = {
            0: None,
            1: Human('M', np.random.randint(0, 100)),
            2: Human('F', np.random.randint(0, 100))
        }[rand_case]
        # list___men.append(Human('M', np.random.randint(0, 100)))
        # list_women.append(Human('F', np.random.randint(0, 100)))

# 展示分布
plane = np.zeros((70, 70, 3), np.uint8)
for i in range(len(plane)):
    for j in range(len(plane[i])):
        if(None == list_2D_plane[i][j]):
            plane[i,j] = [0xFF, 0xFF, 0xFF]
        else:
            real_score_scale_to_255 = 2.55*list_2D_plane[i][j].real_score
            plane[i,j] = {
                'M':  [255-real_score_scale_to_255, 255-real_score_scale_to_255, 255],
                'F':  [255, 255-real_score_scale_to_255, 255-real_score_scale_to_255],
            }[list_2D_plane[i][j].sex]
        
cv.imshow("Plane", cv.resize(plane, None, None, 5, 5, cv.INTER_NEAREST))
cv.waitKey(0)

