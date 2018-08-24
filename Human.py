import numpy as np

class Human(object):
    pass

    def __init__(self, sex, real_score):
        self.sex = sex
        self.real_score = real_score
        self.__feeL_score = np.NaN

    # 在清單中剃除同性
    def __kick_same_sex(self, list_around_human):
        return [human for human in list_around_human if human.sex != self.sex]

    # 在清單中挑選真實最高的對象，而且必須不低於自覺分數
    def select(self, list_around_human):
        highest_score_human = None
        list_around_human = self.__kick_same_sex(list_around_human)
    
        for human in list_around_human:
            if(human.real_score > highest_score_human.real_score):
                highest_score_human = human

        return (False, True)[highest_score_human.real_score >= self.__feeL_score]
