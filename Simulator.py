import random


class Processor:
    def __init__(self, name, queue_capacity, timing_type, working_speed, mu):
        self.mu = mu
        self.name = name
        self.queue = []
        self.queue_capacity = queue_capacity
        self.timing = timing_type
        # for timing_type 1 -> SRJF , 2 -> random , 3 -> PS , 4 -> FCFS
        self.queue_length = 0
        self.number_of_failures = 0
        self.time = 0
        self.working_speed = working_speed

    def serve_next(self, process):
        if self.queue_length < self.queue_capacity:
            self.serve_process(process)
        else:
            self.number_of_failures += 1

    def serve_process(self, process):
        # todo:complete
        l = random.expovariate(lambd=self.mu)
        process.set_work_length(l)
        # process.interval_time
        if self.timing == 1:
            srjf_resource_allocating(self.queue, self.working_speed)
        elif self.timing == 2:
            pass
        elif self.timing == 3:
            pass
        elif self.timing == 4:
            pass

        self.queue.append(process)
        self.time = process.creation_time


class Process:
    def __init__(self, creation_time, interval_time):
        self.creation_time = creation_time
        self.interval_time = 0
        self.work_length = 10000  # todo:check

    def set_work_length(self, work_length):
        self.work_length = work_length


class ProcessGenerator:
    def __init__(self, lambd):
        self.lambd = lambd
        self.now = 0

    def generate_next(self):
        interval_time = random.expovariate(self.lambd)
        self.now += interval_time
        p = Process(creation_time=self.now, interval_time=interval_time)
        return p


def srjf_resource_allocating(processes_list, working_speed):
    work_length_list = list()
    for p in processes_list:
        work_length_list.append(p.work_length)
    for p in processes_list:
        if p.work_length == min(work_length_list):
            p.work_length -= working_speed
            break


def random_resource_allocating(processes_list, working_speed):
    processes_list[random.randint(0, len(processes_list) - 1)].work_length -= working_speed


def ps_resource_allocating(processes_list, working_speed):
    shared_working_speed = working_speed / len(processes_list)
    for p in processes_list:
        p.work_length -= shared_working_speed


def fcfs_resource_allocating(processes_list, working_speed):
    # processes_list must be in order of entrance
    processes_list[0].work_length -= working_speed


def precise_calculation():
    pass
