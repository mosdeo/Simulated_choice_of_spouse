import numpy as np

class Human(object):
    pass

    def __init__(self, sex, real_score):
        self.sex = sex
        self.real_score = real_score
        self.__feel_score = np.NaN
        self.__feel_score_max = 0
        self.__feel_score_min = 100

    def estimator_self_feel_score(self, isSelected, level_score):
        if(isSelected):
            self.__feel_score_min = max(self.__feel_score_min, level_score)
        else:
            self.__feel_score_max = min(self.__feel_score_max, level_score)

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
