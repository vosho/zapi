from concurrent.futures import ThreadPoolExecutor


class ThreadPool(object):
    def __init__(self, worker_count=10):
        self.executor = ThreadPoolExecutor(max_workers=worker_count)

    def submit(self, func, *args, **kwargs):
        return self.executor.submit(func, *args, **kwargs)
