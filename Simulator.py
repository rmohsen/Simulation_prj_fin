import random


class Processor:
    def __init__(self, name, queue_capacity, timing_type, working_speed, mu):
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

    def serve_process(self, process):
        # todo:complete
        l = random.expovariate(lambd=self.mu)
        process.set_work_length(l)


class Process:
    def __init__(self, creation_time):
        self.creation_time = creation_time

    work_length = 10000  # todo:check

    def set_work_length(self, work_length):
        self.work_length = work_length


class ProcessGenerator:
    now = 0

    def __init__(self, lambd):
        self.lambd = lambd

    def generate_next(self):
        self.now += random.expovariate(self.lambd)
        p = Process(creation_time=self.now)
        return p


def srjf_resource_allocating(processes_list, working_speed):
    life_time_list = list()
    for p in processes_list:
        life_time_list.append(p.life_time)
    for p in processes_list:
        if p.life_time == min(life_time_list):
            p.life_time -= working_speed
            break


def random_resource_allocating(processes_list, working_speed):
    processes_list[random.randint(0, len(processes_list) - 1)].life_time -= working_speed


def ps_resource_allocating(processes_list, working_speed):
    shared_working_speed = working_speed / len(processes_list)
    for p in processes_list:
        p.life_time -= shared_working_speed


def fcfs_resource_allocating(processes_list, working_speed):
    # processes_list must be in order of entrance
    processes_list[0].life_time -= working_speed


def precise_calculation():
    pass
