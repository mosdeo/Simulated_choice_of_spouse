import numpy as np

class Human(object):
    pass

    def __init__(self, sex, real_score):
        self.sex = sex
        self.real_score = real_score
        self.__feel_score = np.NaN
        self.__feel_score_max = 99
        self.__feel_score_min = 0
        self.wanted_x_y = None
        self.experience = 0

    def estimator_self_feel_score(self, isSelected, other_real_score):
        self.experience += 1
        if(isSelected):
            self.__feel_score_min = max(self.__feel_score_min, other_real_score) # 被選中，提高自信
        else:
            self.__feel_score_max = min(self.__feel_score_max, other_real_score) # 沒被選中，降低自信
            self.__feel_score = self.__feel_score_max # 從最高分給自己打分數

    def get_feel_score(self):
        if(np.NaN is self.__feel_score):
            return 99
        else:
            return self.__feel_score

    # 漫步移動
    def random_walk(self, x, y, input_matrix):
        # 處裡邊界條件
        if(0==x):                          x_range = [x, x+1]
        elif(x+1==len(input_matrix)):    x_range = [x-1, x]
        else:                              x_range = [x-1, x, x+1]
        if(0==y):                          y_range = [y, y+1]
        elif(y+1==len(input_matrix[0])): y_range = [y-1, y]
        else:                              y_range = [y-1, y, y+1]

        # 對四周進行探訪
        list_free_space = []
        for i in x_range:
            for j in y_range:
                #這個位置沒人，放入候選
                if(None == input_matrix[i][j]):
                    list_free_space.append((i,j))

        # 如果有找到空位
        if(0 != len(list_free_space)):
            next_x, next_y = list_free_space[np.random.randint(len(list_free_space))] #隨機選取沒人的位置
            input_matrix[next_x][next_y] = input_matrix[x][y] #把自己放到新位置
            input_matrix[next_x][next_y].wanted_x_y = None #經過移動之後要清除心儀對象
            input_matrix[x][y] = None #舊位置空出來

