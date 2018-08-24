import numpy as np

class Human(object):
    pass

    def __init__(self, sex, real_score):
        self.sex = sex
        self.real_score = real_score
        self.__feel_score = np.NaN
        self.__feel_score_max = 100
        self.__feel_score_min = 0

    def estimator_self_feel_score(self, isSelected, level_score):
        if(isSelected):
            # 被選中，提高自信
            self.__feel_score_min = max(self.__feel_score_min, level_score)
        else:
            # 沒被選中，降低自信
            self.__feel_score_max = min(self.__feel_score_max, level_score)
            # 從最高分給自己打分數
            self.__feel_score = self.__feel_score_max

    def get_feel_score(self):
        if(np.NaN == self.__feel_score):
            return 100
        else:
            return self.__feel_score

    # 在清單中剃除同性
    # def __kick_same_sex(self, list_around_human):
    #     return [human for human in list_around_human if human.sex != self.sex]

    # # 在清單中挑選真實最高的對象，而且必須不低於自覺分數
    # def select(self, list_around_human):
    #     highest_score_human = None
    #     list_around_human = self.__kick_same_sex(list_around_human)
    
    #     for human in list_around_human:
    #         if(human.real_score > highest_score_human.real_score):
    #             highest_score_human = human

    #     return (False, True)[highest_score_human.real_score >= self.__feeL_score]
