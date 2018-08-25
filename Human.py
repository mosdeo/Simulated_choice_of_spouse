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

