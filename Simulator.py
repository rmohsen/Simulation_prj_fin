import random


class Processor:
    def __init__(self, name, queue_capacity, timing_type, mu, next_processor):
        self.mu = mu
        self.name = name
        self.queue = []
        self.queue_capacity = queue_capacity
        self.timing = timing_type
        # for timing_type 1 -> SRJF , 2 -> random , 3 -> PS , 4 -> FCFS
        self.number_of_failures = 0
        self.next_processor = next_processor
        self.processed_count = 0
        self.sum_latency = 0

    def reset_data(self):
        self.number_of_failures = 0
        self.processed_count = 0
        self.sum_latency = 0

    def serve_next(self, process):
        if len(self.queue) < self.queue_capacity:
            self.queue.append(process)
        else:
            self.number_of_failures += 1

    def get_power(self):
        return random.expovariate(lambd=self.mu)

    def process(self, time):
        p = None
        p_list = None
        if self.timing == 1:
            p = srjf_resource_allocating(processes_list=self.queue, working_speed=self.get_power())
        elif self.timing == 2:
            p = random_resource_allocating(processes_list=self.queue, working_speed=self.get_power())
        elif self.timing == 3:
            p_list = ps_resource_allocating(processes_list=self.queue, working_speed=self.get_power())
        elif self.timing == 4:
            p = fcfs_resource_allocating(processes_list=self.queue, working_speed=self.get_power())
        if p:
            if self.timing < 3:
                p.reset_work_length()
                self.next_processor.serve_next(p)
            self.sum_latency += p.calculate_latency(time)
            self.processed_count += 1
        if p_list:
            self.processed_count += len(p_list)
            for p in p_list:
                self.sum_latency += p.calculate_latency(time)


class Process:
    def __init__(self, work_length, creation_time):
        self.orig_work_length = work_length
        self.work_length = work_length
        self.creation_time = creation_time

    def reset_work_length(self):
        self.work_length = self.orig_work_length

    def calculate_latency(self, time):
        return time - self.creation_time


class ProcessGenerator:
    def __init__(self, lambd):
        self.lambd = lambd

    def generate_next(self, time):
        return Process(random.expovariate(self.lambd), time)


def srjf_resource_allocating(processes_list, working_speed):
    if not processes_list:
        return
    work_length_list = list()
    for p in processes_list:
        work_length_list.append(p.work_length)
    min1 = min(work_length_list)
    for p in processes_list:
        if p.work_length == min1:
            p.work_length -= working_speed
            if p.work_length <= 0:
                processes_list.remove(p)
                return p
            break


def random_resource_allocating(processes_list, working_speed):
    if len(processes_list) == 0:
        return
    p = processes_list[random.randint(0, len(processes_list) - 1)]
    p.work_length -= working_speed
    if p.work_length <= 0:
        processes_list.remove(p)
        return p


def ps_resource_allocating(processes_list, working_speed):
    if len(processes_list) == 0:
        return 0
    shared_working_speed = working_speed / len(processes_list)
    out_list = []
    for i in range(len(processes_list) - 1, -1, -1):
        processes_list[i].work_length -= shared_working_speed
        if processes_list[i].work_length <= 0:
            out_list.append(processes_list[i])
            processes_list.remove(processes_list[i])
    return out_list


def fcfs_resource_allocating(processes_list, working_speed):
    if len(processes_list) == 0:
        return
    p = processes_list[0]
    p.work_length -= working_speed
    if p.work_length <= 0:
        processes_list.remove(p)
        return p
    return
