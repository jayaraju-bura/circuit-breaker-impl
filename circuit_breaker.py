import functools
import logging 
from datetime import datetime


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s,%(msecs)d %(levelname)s: %(message)s",
    datefmt="%H:%M:%S",
)

class CircuitStates:
    OPEN = "open"
    CLOSED = "closed"
    HALF_OPEN = "half_open"

class RemoteCallFailureException(Exception):
    pass

class CircuitBreaker:
    def __init__(self, func, exceptions, threshold, delay):
        self.func = func
        self.exceptions_to_catch = exceptions
        self.threshold = threshold
        self.delay = delay
        self.state = CircuitStates.CLOSED

        self.last_attempt_tstamp = None
        self.failed_attempt_count = 0

    def set_circuit_state(self, state):
        previous_state = self.state
        self.state = state
        logging.info(f"changed state from {previous_state} to {self.state}")

    def update_last_attempt_timestamp(self):
        self.last_attempt_tstamp = datetime.utcnow().timestamp()

    def handle_closed_state(self, *args, **kwargs):
        allowed_exceptions = self.exceptions_to_catch
        try:
            api_call_status = self.func(*args, **kwargs)
            logging.info("Success : Remote call")
            self.update_last_attempt_timestamp()
            return api_call_status
        except allowed_exceptions as ex:
            logging.info("Failure : remote call")

            self.failed_attempt_count += 1
            self.update_last_attempt_timestamp()

            if self.failed_attempt_count >= self.threshold:
                self.set_circuit_state(CircuitStates.OPEN)

            raise RemoteCallFailureException from ex
    
    def handle_open_state(self, *args, **kwargs):
        current_time = datetime.utcnow().timestamp()

        if self.last_attempt_tstamp + self.delay >= current_time:
            raise RemoteCallFailureException(f"Retry after waiting for {self.last_attempt_tstamp + self.delay - current_time} seconds")
        self.set_circuit_state(CircuitStates.HALF_OPEN)
        allowed_exceptions = self.exceptions_to_catch
        try:
            api_call_status = self.func(*args, **kwargs)
            self.set_circuit_state(CircuitStates.CLOSED)
            self.failed_attempt_count = 0
            self.update_last_attempt_timestamp()
            return api_call_status

        except allowed_exceptions as ex:
            self.failed_attempt_count += 1
            self.update_last_attempt_timestamp()
            self.set_circuit_state(CircuitStates.OPEN)
            raise RemoteCallFailureException from ex

    def make_remote_call(self, *args, **kwargs):
        if self.state == CircuitStates.OPEN:
            return self.handle_open_state(*args, **kwargs)
        if self.state == CircuitStates.CLOSED:
            return self.handle_closed_state(*args, **kwargs)
        


class APICircuitBreaker:
    def __init__(self, exceptions=(Exception,), threshold=5, delay=60):
        self.obj = functools.partial(
            CircuitBreaker,
            exceptions=exceptions,
            threshold=threshold,
            delay=delay
        )

    def __call__(self, func):
        self.obj = self.obj(func=func)

        def decorator(*args, **kwargs):
            ret_val = self.obj.make_remote_call(*args, **kwargs)
            return ret_val

        return decorator

    def __getattr__(self, item):
        return getattr(self.obj, item)


circuit_breaker = APICircuitBreaker
