import numpy as np
import cv2 as cv
from Human import Human

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


# 給大約各 100 位男女，隨機分配真實分數
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
    # print("T={}".format(T))

    # 找到周圍最高分位置
    for i in range(len(list_2D_plane)):
        for j in range(len(list_2D_plane[i])):
            if(None == list_2D_plane[i][j]): continue #這個位置沒人
            list_2D_plane[i][j].set_find_round_highest_xy(i, j, list_2D_plane)

    # 計算自覺分數
    for i in range(len(list_2D_plane)):
        for j in range(len(list_2D_plane[i])):
            if(None == list_2D_plane[i][j]): continue #這個位置沒人
            list_2D_plane[i][j].set_self_feel_score(i, j, list_2D_plane)

    # 對場上所有人配對
    for i in range(len(list_2D_plane)):
        for j in range(len(list_2D_plane[i])):
            if(None == list_2D_plane[i][j]): continue # 這個位置沒人
            if(None == list_2D_plane[i][j].wanted_x_y): continue # 這個位置沒找目標
            wanted_x, wanted_y = list_2D_plane[i][j].wanted_x_y # 找出此人心儀對象座標
            if(None == list_2D_plane[wanted_x][wanted_y]): continue # 心儀對象已經先配對到，走了!
            if(None == list_2D_plane[wanted_x][wanted_y].wanted_x_y): continue # 心儀對象還沒找到心儀對象
            if((i,j) == list_2D_plane[wanted_x][wanted_y].wanted_x_y): # 心儀對象的心儀對象座標，跟自己一樣嗎?
                print("T={}, 配對成功!, M={}, exp={}, F={}, exp={}"
                        .format(T, 
                                list_2D_plane[i][j].real_score, list_2D_plane[i][j].experience,
                                list_2D_plane[wanted_x][wanted_y].real_score, list_2D_plane[wanted_x][wanted_y].experience
                                ))
                list_2D_plane[i][j] = None # 把人趕走
                list_2D_plane[wanted_x][wanted_y] = None # 把人趕走
    display_plane(list_2D_plane)
    cv.waitKey(1)

    # if(T<30):continue
    # 漫步移動
    for i in range(len(list_2D_plane)):
        for j in range(len(list_2D_plane[i])):
            if(None == list_2D_plane[i][j]): continue #這個位置沒人
            list_2D_plane[i][j].random_walk(i, j, list_2D_plane)
    display_plane(list_2D_plane)
    cv.waitKey(1)

    display_plane(list_2D_plane)
    cv.waitKey(30)

cv.waitKey(0)