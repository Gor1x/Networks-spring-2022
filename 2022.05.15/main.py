import json
from threading import Thread, Event

file_name = 'data.json'


class RipController:
    MAX_DISTANCE = 16
    _HEADER_LINE = '[Source IP]       ' \
                   '[Destination IP]  ' \
                   '[Next Hop]     ' \
                   '[Metric]'

    def _get_edges(self):
        for (v, xs) in self.metric.items():
            for (u, w) in xs.items():
                yield v, u, w

    def _get_neighbour_edges(self):
        for (v, u, w) in self._get_edges():
            if w != 1:
                continue
            yield v, u, w

    def __init__(self, json_data):
        self.is_algorithm_stopped = Event()
        self.metric = dict()
        self.next_hop = dict()
        self.step_number = 1
        for line in json_data:
            self.add_edge(line['a'], line['b'])

    def try_to_relax_edge(self, v_from, v_to, v_inner):
        if self._distance(v_inner, v_to) + 1 < self._distance(v_from, v_to):
            self.metric[v_from][v_to] = self.metric[v_inner][v_to] + 1
            self.next_hop[v_from][v_to] = v_inner
            return True
        return False

    def relax_distances(self):
        print(f'Step {self.step_number} simulation')

        graph_changed = False

        for (v, u, w) in self._get_neighbour_edges():
            for k in self._routers():
                if self.try_to_relax_edge(u, k, v):
                    graph_changed = True

        self.print_graph_state(isFinal=not graph_changed)
        self.step_number += 1
        if not graph_changed:
            self.is_algorithm_stopped.set()

    def _routers(self):
        return self.metric.keys()

    def run_rip(self):
        RipThread(self.is_algorithm_stopped, self.relax_distances).start()

    def _add_edge(self, v, u, w):
        if v not in self.metric:
            self.metric[v] = dict()
            self.next_hop[v] = dict()
        self.metric[v][u] = w
        self.next_hop[v][u] = u

    def add_edge(self, a, b):
        self._add_edge(a, b, 1)
        self._add_edge(b, a, 1)
        self._add_edge(a, a, 0)
        self._add_edge(b, b, 0)

    def _distance(self, a, b):
        if a in self.metric:
            if b in self.metric[a]:
                return self.metric[a][b]
        return self.MAX_DISTANCE

    @staticmethod
    def _formatted_ip(v):
        return str(v).ljust(18)

    def print_graph_state(self, isFinal=False):
        for v in self._routers():
            if isFinal:
                print(f'Final state of router {v}')
            else:
                print(f'Simulation step {self.step_number} of router {v}')
            print(self._HEADER_LINE)
            for (u, w) in self.metric[v].items():
                if w != 0:
                    print(self._str_by_path_data(v, u, w))

    def _str_by_path_data(self, v, u, w):
        return f'{self._formatted_ip(v)}' \
               f'{self._formatted_ip(u)}' \
               f'{self._formatted_ip(self.next_hop[v][u])}' \
               f'{str(w).rjust(5)}'


class RipThread(Thread):
    SHARE_TIME_SECONDS = 3

    def __init__(self, event, f):
        Thread.__init__(self)
        self.stopped = event
        self.function = f

    def run(self):
        while not self.stopped.wait(self.SHARE_TIME_SECONDS):
            self.function()


def main():
    with open(file_name) as json_data:
        data = json.load(json_data)
        RipController(data).run_rip()


if __name__ == '__main__':
    main()
