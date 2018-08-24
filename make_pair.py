import numpy as np
import cv2 as cv
from Human import Human

# 取得周圍最高分
def find_round_highest_obj(x, y, input_matrix):
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
            if(None == input_matrix[i][j]): continue #這個位置沒人
            else: input_matrix[x][y].wanted_x_y = -1, -1

            # 跳過自己、跳過同性
            if(i==x and j==y):continue
            if(input_matrix[x][y].sex == input_matrix[i][j].sex): continue
            
            # 如果口袋是空的
            if(None == highest_object):
                # 如果分數大於等於自己，放進口袋
                if(input_matrix[i][j].real_score > input_matrix[x][y].real_score):
                    highest_object = input_matrix[i][j]
                    input_matrix[x][y].wanted_x_y = i,j
            # 如果口袋不是空的
            else:
                # 如果分數大於等於口袋，放進口袋
                if(input_matrix[i][j].real_score > highest_object.real_score):
                    highest_object = input_matrix[i][j]
                    input_matrix[x][y].wanted_x_y = i,j

# 展示分布
def display_plane(input_matrix):
    col_size, row_size = len(input_matrix), len(input_matrix[0])
    plane = np.zeros((col_size, row_size, 3), np.uint8)
    for i in range(col_size):
        for j in range(row_size):
            if(None == input_matrix[i][j]):
                plane[i,j] = [0xFF, 0xFF, 0xFF]
            else:
                real_score_scale_to_255 = 2.55*input_matrix[i][j].real_score
                plane[i,j] = {
                    'M':  [255-real_score_scale_to_255, 255-real_score_scale_to_255, 255],
                    'F':  [255, 255-real_score_scale_to_255, 255-real_score_scale_to_255],
                }[input_matrix[i][j].sex]
            
    cv.imshow("Plane", cv.resize(plane, None, None, 5, 5, cv.INTER_NEAREST))


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

display_plane(list_2D_plane)
cv.waitKey(0)

# 打分數
for i in range(len(list_2D_plane)):
    for j in range(len(list_2D_plane[i])):
        if(None == list_2D_plane[i][j]): continue #這個位置沒人
        find_round_highest_obj(i, j, list_2D_plane)

# 配對
for i in range(len(list_2D_plane)):
    for j in range(len(list_2D_plane[i])):
        if(None == list_2D_plane[i][j]): continue #這個位置沒人
        wanted_x, wanted_y = list_2D_plane[i][j].wanted_x_y 
        if(i, j == list_2D_plane[wanted_x][wanted_y].wanted_x_y):
            print("配對成功!")
            list_2D_plane[i][j] = None # 把人趕走
            display_plane(list_2D_plane)
            cv.waitKey(1)

display_plane(list_2D_plane)
cv.waitKey(0)

