import random


class Processor:
    def __init__(self, name, queue_capacity, timing_type, working_speed,mu):
        self.mu = mu
        self.name = name
        self.queue_capacity = queue_capacity
        self.timing = timing_type
        # for timing_type 1 -> SRJF , 2 -> random , 3 -> PS , 4 -> FCFS

    queue_length = 0

    def serve_next(self, process):
        if self.queue_length < self.queue_capacity:
            self.serve_process(process)
        else:
            pass  # todo

    def serve_process(self,process):
        #todo:complete
        l = random.expovariate(lambd=self.mu)
        process.set_work_length(l)

class Process:
    def __init__(self, life_time, creation_time):
        self.life_time = life_time
        self.creation_time = creation_time

    work_length = 10000  # todo:check

    def set_work_length(self, work_length):
        self.work_length = work_length


class ProcessGenerator:
    def __init__(self, lambd, now, process_life_time):
        self.lambd = lambd
        self.now = now
        self.process_life_time = process_life_time

    def generate_next(self):
        self.now += random.expovariate(self.lambd)
        p = Process(life_time=self.process_life_time, creation_time=self.now)
        return p


def srjf_resource_allocating(self, processes_list, working_speed):
    life_time_list = list()
    for p in processes_list:
        life_time_list.append(p.life_time)
    for p in processes_list:
        if p.life_time == min(life_time_list):
            p.life_time -= working_speed


def random_resource_allocating(self, processes_list):
    pass


def ps_resource_allocating(self):
    pass


def fcfs_resource_allocating(self):
    pass


def precise_calculation(self):
    pass
