import numpy as np
import cv2 as cv
from Human import Human

# 取得周圍最高分
def get_round_highest_obj(x, y, input_matrix):
    # 處裡邊界條件
    if(0==x):                        x_range = [x, x+1]
    elif(x+1==len(input_matrix)):    x_range = [x-1, x]
    else:                            x_range = [x-1, x, x+1]
    if(0==y):                        y_range = [y, y+1]
    elif(y+1==len(input_matrix[0])): y_range = [y-1, y]
    else:                            y_range = [y-1, y, y+1]

    highest_object = None
    for i in x_range:
        for j in y_range:
            # 跳過自己、跳過同性
            if(i==x and j==y):continue
            if(input_matrix[x][y].sex == input_matrix[i][j].sex): continue
            
            # 如果口袋是空的
            if(None == highest_object):
                # 如果分數大於等於自己，放進口袋
                if(input_matrix[i][j].real_score > input_matrix[x][y].real_score):
                    highest_object = input_matrix[i][j]
                    highest_object.x_y = i,j
            # 如果口袋不是空的
            else:
                # 如果分數大於等於口袋，放進口袋
                if(input_matrix[i][j].real_score > highest_object.real_score):
                    highest_object = input_matrix[i][j]
                    highest_object.x_y = i,j
    return highest_object


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
for i in range(len(list_2D_plane)):
    for j in range(len(list_2D_plane[i])):
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

# 配對

