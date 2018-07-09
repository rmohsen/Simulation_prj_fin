import Simulator as s


def calculate_first_question_answer(self):
    mu1 = 5
    k1 = 100
    pre_pros_1 = s.Processor(name=1, queue_capacity=k1, timing_type=1, working_speed=1, mu=mu1)

    mu2 = 3
    k2 = 12
    pre_pros_2 = s.Processor(name=2, queue_capacity=k2, timing_type=2, working_speed=1, mu=mu2)

    mu3 = 1
    k3 = 8  # todo =? 16
    core_pros = s.Processor(name=3, queue_capacity=k3, timing_type=3, working_speed=1, mu=mu3)

    lambda1 = 7
    s.ProcessGenerator(lambd=lambda1)

    lambda2 = 2
    s.ProcessGenerator(lambd=lambda2)
    pass

import seaborn


def calculate_second_question_answer(self):
    pass
