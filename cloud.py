from system_parameters import parameter
from task import get_fixed_task
import numpy as np


class Cloud:
    def __init__(self, uplink_rate, execution_cap):
        self.tr_power = parameter['tr_power']
        self.tail_latency_energy = parameter['tail_energy']
        self.tail_duration = parameter["tail_duration"]
        self.uplink_rate = uplink_rate
        self.execution_cap = parameter['cloud_com_cap'] * execution_cap
        self.price = parameter["cph_cloud"]
        self.distance = 500000.0  # in m
        self.propagation_speed = 2e8  # in m/s

    def cal_propagation_delay(self):
        # delay = self.distance / self.propagation_speed
        # delay = 0.25 # amazon us-east-1 average latency for a day.
        while True:
            delay = np.random.normal(250, 189)
            if delay < 0:
                continue
            else:
                delay = delay / 1000.0
                break
        return delay

    def cal_transmit_time(self, task):
        tr_time = task['data'] / self.uplink_rate
        tr_time += self.cal_propagation_delay()
        return tr_time

    def cal_transmit_energy(self, task, tr_time):
        tr_energy = self.tr_power * tr_time + self.tail_latency_energy * self.tail_duration
        return tr_energy

    def cal_processing_time(self, task):
        proc_time = task["cpu_cycle"] / self.execution_cap
        return proc_time

    def cal_price(self, proc_time):
        expense = proc_time * self.price
        return expense

    def cal_total_cost(self, task, weight, energy_factor):
        tr_time = self.cal_transmit_time(task)
        proc_time = self.cal_processing_time(task)
        energy = self.cal_transmit_energy(task, tr_time)
        money = self.cal_price(proc_time)
        time = tr_time + proc_time
        energy_impact = energy + energy * energy_factor
        total = (1 - weight) * time + weight * energy_impact + money
        return total, time, energy


if __name__ == '__main__':
    cloud = Cloud(15000000, 0.6)
    task = get_fixed_task()
    # print(cloud.cal_transmit_energy(task))
    print(cloud.cal_transmit_time(task))
    # print(cloud.cal_transmit_time(task) + cloud.cal_processing_time(task))
    print(cloud.cal_total_cost(task, 0.5, 0))
