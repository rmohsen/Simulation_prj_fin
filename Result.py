import Simulator as sim
import statistics as st
import math
import threading
import time
import numpy as np
import matplotlib.pyplot as plt


def simulate(k3):
    global output

    mu3 = 1
    # for optional part of project run with this line (timing_type=4)
    # core_pros = sim.Processor(name=3, queue_capacity=k3 + 8, timing_type=4, mu=mu3, next_processor=None)
    core_pros = sim.Processor(name=3, queue_capacity=k3 + 8, timing_type=3, mu=mu3, next_processor=None)

    mu1 = 5
    k1 = 100
    pre_pros_1 = sim.Processor(name=1, queue_capacity=k1, timing_type=1, mu=mu1, next_processor=core_pros)

    mu2 = 3
    k2 = 12
    pre_pros_2 = sim.Processor(name=2, queue_capacity=k2, timing_type=2, mu=mu2, next_processor=core_pros)

    lambda1 = 7
    p_gen1 = sim.ProcessGenerator(lambd=lambda1)

    lambda2 = 2
    p_gen2 = sim.ProcessGenerator(lambd=lambda2)

    sum_1 = 0
    sum_2 = 0
    sum_3 = 0
    t = 0
    warm_up = True
    while core_pros.processed_count < processed_count_to_end:
        if core_pros.processed_count >= 5000 and warm_up:
            pre_pros_1.reset_data()
            pre_pros_2.reset_data()
            core_pros.reset_data()
            sum_1 = 0
            sum_2 = 0
            sum_3 = 0
            t = 0
            warm_up = False

        core_pros.process(t)
        sum_3 += len(core_pros.queue)
        pre_pros_1.process(t)
        sum_1 += len(pre_pros_1.queue)
        pre_pros_2.process(t)
        sum_2 += len(pre_pros_2.queue)
        notify_process_gen(p_gen1, pre_pros_1, t)
        notify_process_gen(p_gen2, pre_pros_2, t)
        t += 1

    o11 = pre_pros_1.number_of_failures / (
                pre_pros_1.number_of_failures + pre_pros_1.processed_count + len(pre_pros_1.queue))
    o12 = sum_1 / t
    o13 = pre_pros_1.sum_latency / pre_pros_1.processed_count
    o21 = core_pros.number_of_failures / (
                core_pros.number_of_failures + core_pros.processed_count + len(core_pros.queue))
    o22 = core_pros.sum_latency / core_pros.processed_count
    o23 = sum_3 / (pre_pros_1.processed_count + pre_pros_2.processed_count)

    output[k3].append({1: o11, 2: o12, 3: o13, 4: o21, 5: o22, 6: o23})


def notify_process_gen(process_gen, processor, t):
    p = process_gen.generate_next(t)
    if p:
        processor.serve_next(p)


def show_plot(values, title):
    plt.bar(y_pos, values, align='center', alpha=0.5)
    plt.xticks(y_pos, k3_list)
    plt.ylabel('output')
    plt.xlabel('k3')
    plt.title(title)
    plt.show()


processed_count_to_end = 500000
r = 25

k3_list = [i for i in range(9)]  # minus 8 considered
output = [[] for i in range(9)]

for i in range(r):
    for k in k3_list:
        threading.Thread(target=lambda: simulate(k)).start()

while True:
    end_flag = True
    for k in k3_list:
        if len(output[k]) < r:
            end_flag = False
    if end_flag:
        break
    time.sleep(1)

for i in range(1, 4):
    o_list = []
    for j in range(r):
        o_list.append(output[3][j][i])
    s = math.sqrt(st.variance(o_list))
    y = st.mean(o_list)
    precision = (1.96 * s) / (math.sqrt(r) * y)
    print("1." + str(i) + "(k3=11): " + str(y) + "\t\tprecision: " + str(precision))

y_pos = np.arange(len(k3_list))
for i in range(4, 7):
    outputs = []
    for k in k3_list:
        o_list = []
        sum_values = 0
        for j in range(r):
            o_list.append(output[k][j][i])
            sum_values += output[k][j][i]
        s = math.sqrt(st.variance(o_list))
        y = st.mean(o_list)
        if -0.0000001 < y < 0.0000001:
            precision = 0
        else:
            precision = (1.96 * s) / (math.sqrt(r) * y)
        outputs.append(sum_values / r)
        print("2." + str(i - 3) + "(k3=" + str(k + 8) + "): " + str(y) + "\t\tprecision: " + str(precision))
    show_plot(outputs, '2.' + str(i - 3))
