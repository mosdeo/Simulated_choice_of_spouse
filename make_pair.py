import numpy as np
import cv2 as cv
from Human import Human

# 取得周圍最高分
def find_round_highest_xy(x, y, input_matrix):
    # 處裡邊界條件
    __input_matrix = input_matrix
    if(0==x):                          x_range = [x, x+1]
    elif(x+1==len(__input_matrix)):    x_range = [x-1, x]
    else:                              x_range = [x-1, x, x+1]
    if(0==y):                          y_range = [y, y+1]
    elif(y+1==len(__input_matrix[0])): y_range = [y-1, y]
    else:                              y_range = [y-1, y, y+1]

    highest_object = None
    for i in x_range:
        for j in y_range:
            if(None == __input_matrix[i][j]): continue #這個位置沒人
            else: __input_matrix[x][y].wanted_x_y = -1, -1

            # 跳過自己、跳過同性
            if(i==x and j==y):continue
            if(__input_matrix[x][y].sex == __input_matrix[i][j].sex): continue
            
            # 如果口袋是空的
            if(None == highest_object):
                # 如果分數大於等於自己自覺分數，放進口袋
                if(__input_matrix[i][j].real_score > __input_matrix[x][y].real_score):
                    highest_object = __input_matrix[i][j]
                    __input_matrix[x][y].wanted_x_y = i,j
            # 如果口袋不是空的
            else:
                # 如果分數大於等於口袋，放進口袋
                if(__input_matrix[i][j].real_score > highest_object.real_score):
                    highest_object = __input_matrix[i][j]
                    __input_matrix[x][y].wanted_x_y = i,j


# 計算自覺分數
def find_self_feel_score(x, y, input_matrix):
    # 處裡邊界條件
    __input_matrix = input_matrix
    if(0==x):                          x_range = [x, x+1]
    elif(x+1==len(__input_matrix)):    x_range = [x-1, x]
    else:                              x_range = [x-1, x, x+1]
    if(0==y):                          y_range = [y, y+1]
    elif(y+1==len(__input_matrix[0])): y_range = [y-1, y]
    else:                              y_range = [y-1, y, y+1]

    # 對四周進行探訪
    for i in x_range:
        for j in y_range:
            if(None == __input_matrix[i][j]): continue #這個位置沒人
            if(__input_matrix[x][y].sex == __input_matrix[i][j].sex): continue # 跳過同性
            if((-1,-1) == list_2D_plane[i][j].wanted_x_y): continue #這個位置沒找目標
            if(i==x and j==y):continue # 跳過自己

            # 取得此人心儀對象的位置
            wanted_x, wanted_y = list_2D_plane[i][j].wanted_x_y

            # 沒被選中，重新評估自覺分數
            if(x, y != wanted_x, wanted_y):
                print("沒被選中，重新評估自覺分數")
                __input_matrix[x][y].estimator_self_feel_score(False, __input_matrix[i][j].real_score)
            # 被選中，重新評估自覺分數
            else:
                print("被選中，重新評估自覺分數")
                __input_matrix[x][y].estimator_self_feel_score(True, __input_matrix[i][j].real_score)

# 漫步移動
def random_walk(x, y, input_matrix):
    # 處裡邊界條件
    __input_matrix = input_matrix
    if(0==x):                          x_range = [x, x+1]
    elif(x+1==len(__input_matrix)):    x_range = [x-1, x]
    else:                              x_range = [x-1, x, x+1]
    if(0==y):                          y_range = [y, y+1]
    elif(y+1==len(__input_matrix[0])): y_range = [y-1, y]
    else:                              y_range = [y-1, y, y+1]

    # 對四周進行探訪
    list_free_space = []
    for i in x_range:
        for j in y_range:
            #這個位置沒人
            if(None == __input_matrix[i][j]):
                list_free_space.append((i,j))

    if(0 != len(list_free_space)):
        next_x, next_y = list_free_space[np.random.randint(len(list_free_space))]
        __input_matrix[next_x][next_y] = __input_matrix[x][y]
        __input_matrix[x][y] = None

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

display_plane(list_2D_plane)
print("初始值")
cv.waitKey(0)

for T in range(1000):
    print("T={}".format(T))

    # 找到周圍最高分位置
    for i in range(len(list_2D_plane)):
        for j in range(len(list_2D_plane[i])):
            if(None == list_2D_plane[i][j]): continue #這個位置沒人
            find_round_highest_xy(i, j, list_2D_plane)

    # 計算自覺分數
    for i in range(len(list_2D_plane)):
        for j in range(len(list_2D_plane[i])):
            if(None == list_2D_plane[i][j]): continue #這個位置沒人
            find_self_feel_score(i, j, list_2D_plane)

    # 配對
    for i in range(len(list_2D_plane)):
        for j in range(len(list_2D_plane[i])):
            if(None == list_2D_plane[i][j]): continue #這個位置沒人
            if((-1,-1) == list_2D_plane[i][j].wanted_x_y): continue #這個位置沒找目標
            wanted_x, wanted_y = list_2D_plane[i][j].wanted_x_y
            if(i, j == list_2D_plane[wanted_x][wanted_y].wanted_x_y):
                print("配對成功!")
                list_2D_plane[i][j] = None # 把人趕走
                display_plane(list_2D_plane)
                cv.waitKey(1)

    # 漫步移動
    for i in range(len(list_2D_plane)):
        for j in range(len(list_2D_plane[i])):
            if(None == list_2D_plane[i][j]): continue #這個位置沒人
            random_walk(i, j, list_2D_plane)


    display_plane(list_2D_plane)
    cv.waitKey(30)