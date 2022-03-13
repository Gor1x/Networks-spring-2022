from queue import Queue, Empty
from threading import Thread


class BadStartException(Exception):
    pass


class BadEndException(Exception):
    pass


class ThreadPool:
    def __init__(self, max_threads, function_to_run):
        self._max_threads = max_threads
        self._tasks = Queue()
        self._function = function_to_run
        self._threads = [Thread(target=self._task_runner) for _ in range(max_threads)]
        self._is_running = False
        self._is_started = False
        self._is_ended = False

    def start(self):
        if self._is_started:
            raise BadStartException
        self._is_started = True
        self._is_running = True
        for t in self._threads:
            t.start()
        return self

    def add_task(self, *task):
        if self._is_ended:
            raise RuntimeError("Can't add tasks when ended")
        self._tasks.put(task)

    def stop(self):
        if self._is_ended:
            raise BadEndException
        self._is_ended = True
        self._tasks.join()
        self._is_running = False
        for t in self._threads:
            t.join()

    def _task_runner(self):
        while self._is_running:
            try:
                task = self._tasks.get(timeout=0.1)
                self._function(*task)
                self._tasks.task_done()
            except Empty:
                pass
