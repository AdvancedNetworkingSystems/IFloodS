import random
import heapq


class EventScheduler(object):
        def __init__(self):
                self.queue = []
                self.time = 0
                self.last = 0

        def schedule_event(self, interval, e):
                t = self.time + interval
                if t > self.last:
                    self.last = t
                heapq.heappush(self.queue, (t, e))

        def pop_event(self):
                e = heapq.heappop(self.queue)
                self.time = e[0]
                return e[1]

        def elapsed_time(self):
                return self.time

        def last_event_time(self):
                return self.last


def simulate_multi_queue(time, feedback_prob=0):
    l = 1  # arrival rate
    customers = {0: 0, 1: 0, 2: 0, 3: 0}
    mean_service_time = {0: 0.5, 1: 0.7, 2: 0.8, 3: 0.95}
    intervals = {q: (mean_service_time[q]/2,  mean_service_time[q]*3/2)
                 for q in mean_service_time}

    sched = EventScheduler()
    sched.schedule_event(random.expovariate(l), 0)

    filename = "queue_length_fprob" + str(feedback_prob) + ".csv"
    fp = open(filename, "w")
    fp.write("time,q0len,q1len,q2len,q3len\n")

    while(sched.elapsed_time() < time):
        queue = sched.pop_event()
        # we have an arrival in queue number "queue"

        # update of queue-1
        if queue - 1 < 0:
            sched.schedule_event(random.expovariate(l), queue)
        else:
            customers[queue-1] -= 1
            if customers[queue-1] > 0:
                sched.schedule_event(random.uniform(intervals[queue-1][0],
                                                    intervals[queue-1][1]),
                                     queue)

        # update of queue
        if queue <= 3:
            customers[queue] += 1
            if customers[queue] == 1:
                sched.schedule_event(random.uniform(intervals[queue][0],
                                                    intervals[queue][1]),
                                     queue+1)
        else:
            if feedback_prob > 0:
                # we feedback to queue 2
                feedback_queue = 2
                if random.uniform(0, 1) < feedback_prob:
                    customers[feedback_queue] += 1
                    if customers[feedback_queue] == 1:
                        sched.schedule_event(random.uniform(
                            intervals[feedback_queue][0],
                            intervals[feedback_queue][1]),
                            feedback_queue+1)

        fp.write(str(sched.elapsed_time()) + "," +
                 ",".join([str(el) for el in customers.values()]) + "\n")

    fp.close()

if __name__ == '__main__':
    simulate_multi_queue(time=10000)
    simulate_multi_queue(time=10000, feedback_prob=0.04)
    simulate_multi_queue(time=10000, feedback_prob=0.06)
