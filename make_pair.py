import numpy as np
import cv2 as cv
from Human import Human

# 取得周圍最高分對象位置
def find_round_highest_xy(x, y, input_matrix):
    # 處裡邊界條件
    __input_matrix = input_matrix
    if(0==x):                          x_range = [x, x+1]
    elif(x+1==len(__input_matrix)):    x_range = [x-1, x]
    else:                              x_range = [x-1, x, x+1]
    if(0==y):                          y_range = [y, y+1]
    elif(y+1==len(__input_matrix[0])): y_range = [y-1, y]
    else:                              y_range = [y-1, y, y+1]

    __input_matrix[x][y].wanted_x_y = None # 清除口袋

    for i in x_range:
        for j in y_range:
            if(None == __input_matrix[i][j]): continue #這個位置沒人
            if(__input_matrix[x][y].sex == __input_matrix[i][j].sex): continue # 跳過同性
            if(i==x and j==y):continue # 跳過自己
            
            # 如果口袋是空的
            if(None == __input_matrix[x][y].wanted_x_y):
                # 如果此人真實分數，大於等於自己自覺分數
                if(__input_matrix[i][j].real_score >= __input_matrix[x][y].get_feel_score()):
                    __input_matrix[x][y].wanted_x_y = i,j # 放進口袋
            # 如果口袋不是空的
            else:
                wanted_x, wanted_y = __input_matrix[x][y].wanted_x_y #挖出自己口袋對象座標
                # 如果此人真實分數，大於等於口袋對象真實分數
                if(__input_matrix[i][j].real_score >= __input_matrix[wanted_x][wanted_y].real_score):
                    __input_matrix[x][y].wanted_x_y = i,j # 放進口袋


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
            # if(None == __input_matrix[i][j].wanted_x_y): continue #這個位置沒找到心儀對象
            if(__input_matrix[x][y].sex == __input_matrix[i][j].sex): continue # 跳過同性
            if(i==x and j==y):continue # 跳過自己

            # 沒被選中，重新評估自覺分數
            if(None==__input_matrix[i][j].wanted_x_y or x,y!=__input_matrix[i][j].wanted_x_y):
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
            #這個位置沒人，放入候選
            if(None == __input_matrix[i][j]):
                list_free_space.append((i,j))

    # 如果有找到空位
    if(0 != len(list_free_space)):
        next_x, next_y = list_free_space[np.random.randint(len(list_free_space))] #隨機選取沒人的位置
        __input_matrix[next_x][next_y] = __input_matrix[x][y] #把自己放到新位置
        __input_matrix[next_x][next_y].wanted_x_y = None #經過移動之後要清除心儀對象
        __input_matrix[x][y] = None #舊位置空出來
        

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

    # 對場上所有人配對
    for i in range(len(list_2D_plane)):
        for j in range(len(list_2D_plane[i])):
            if(None == list_2D_plane[i][j]): continue # 這個位置沒人
            if(None == list_2D_plane[i][j].wanted_x_y): continue # 這個位置沒找目標
            wanted_x, wanted_y = list_2D_plane[i][j].wanted_x_y # 找出此人心儀對象座標
            if(None == list_2D_plane[wanted_x][wanted_y]): continue # 心儀對象已經先配對到，走了!
            if(None == list_2D_plane[wanted_x][wanted_y].wanted_x_y): continue # 心儀對象還沒找到心儀對象
            if((i,j) == list_2D_plane[wanted_x][wanted_y].wanted_x_y): # 心儀對象的心儀對象座標，跟自己一樣嗎?
                print("T={}, 配對成功!, M={}, xy={}, F={}, xy={}"
                        .format(T, 
                                list_2D_plane[i][j].real_score, list_2D_plane[i][j].wanted_x_y,
                                list_2D_plane[wanted_x][wanted_y].real_score, list_2D_plane[wanted_x][wanted_y].wanted_x_y
                                ))
                list_2D_plane[i][j] = None # 把人趕走
                list_2D_plane[wanted_x][wanted_y] = None # 把人趕走
    display_plane(list_2D_plane)
    cv.waitKey(1)

    if(T<30):continue
    # 漫步移動
    for i in range(len(list_2D_plane)):
        for j in range(len(list_2D_plane[i])):
            if(None == list_2D_plane[i][j]): continue #這個位置沒人
            random_walk(i, j, list_2D_plane)
    display_plane(list_2D_plane)
    cv.waitKey(1)

    display_plane(list_2D_plane)
    cv.waitKey(30)

cv.waitKey(0)