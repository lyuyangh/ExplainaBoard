from typing import Any, Dict, List
from eaas import Client
from threading import Thread
import uuid


class AsyncEaaSClient(Client):
    """
    A wrapper class to support async requests for EaaS. It uses threads so there is a limit to the maximum number of parallel requests it can make.
    Example usage:
      1. `request_id = client.score([])` to start a new thread and make a request
      2. `client.wait_and_get_result(request_id)` to join the thread and get the result, this method can be called only once for each request_id
    """

    def __init__(self):
        super().__init__()
        self._threads: Dict[int, Thread] = {}
        self._results: Dict[int, Any] = {}

    def _run_thread(self, original_fn) -> str:
        request_id = str(uuid.uuid1())

        def fn():
            self._results[request_id] = original_fn()

        self._threads[request_id] = Thread(target=fn)
        self._threads[request_id].start()
        return request_id

    def async_score(
        self,
        inputs: List[Dict],
        task="sum",
        metrics=None,
        lang="en",
        cal_attributes=False,
    ):
        return self._run_thread(
            lambda: super(AsyncEaaSClient, self).score(
                inputs, task, metrics, lang, cal_attributes
            )
        )

    def wait_and_get_result(self, request_id: str):
        if request_id not in self._threads:
            raise Exception(f"thread_id {request_id} doesn't exist")
        self._threads[request_id].join()
        result = self._results[request_id]
        self._results.pop(request_id)
        self._threads.pop(request_id)
        return result
