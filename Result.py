import Simulator as s


def calculate_first_question_answer():
    mu3 = 1
    k3 = 8  # todo =? 16
    core_pros = s.Processor(name=3, queue_capacity=k3, timing_type=3, mu=mu3, next_processor=None)

    mu1 = 5
    k1 = 100
    pre_pros_1 = s.Processor(name=1, queue_capacity=k1, timing_type=1, mu=mu1, next_processor=core_pros)

    mu2 = 3
    k2 = 12
    pre_pros_2 = s.Processor(name=2, queue_capacity=k2, timing_type=2, mu=mu2, next_processor=core_pros)

    lambda1 = 7
    p_gen1 = s.ProcessGenerator(lambd=lambda1)

    lambda2 = 2
    p_gen2 = s.ProcessGenerator(lambd=lambda2)

    sum_1 = 0
    warm_up = True
    while core_pros.processed_count < 50000:
        print(len(pre_pros_1.queue), pre_pros_1.processed_count)
        print(len(pre_pros_2.queue), pre_pros_2.processed_count)
        print(len(core_pros.queue), core_pros.processed_count)
        if core_pros.processed_count >= 50 and warm_up:
            pre_pros_1.reset_data()
            pre_pros_2.reset_data()
            core_pros.reset_data()
            sum_1 = 0
            warm_up = False

        core_pros.process()
        pre_pros_1.process()
        sum_1 += len(pre_pros_1.queue)
        pre_pros_2.process()
        notify_process_gen(p_gen1, pre_pros_1)
        notify_process_gen(p_gen2, pre_pros_2)
    print("1.1: " + str(pre_pros_1.number_of_failures / (pre_pros_1.number_of_failures + pre_pros_1.processed_count + k1)))
    print("1.2: " + str(sum_1 / (50000 - 50)))


import seaborn


def notify_process_gen(process_gen, processor):
    p = process_gen.generate_next()
    if p:
        processor.serve_next(p)


def calculate_second_question_answer():
    pass


calculate_first_question_answer()
