# circuit-breaker-impl

``
File ~\OneDrive\Documents\circuit-breaker-impl\circuit_breaker.py:80, in CircuitBreaker.make_remote_call(self, *args, **kwargs)
     78 def make_remote_call(self, *args, **kwargs):
     79     if self.state == CircuitStates.OPEN:
---> 80         return self.handle_open_state(*args, **kwargs)
     81     if self.state == CircuitStates.CLOSED:
     82         return self.handle_closed_state(*args, **kwargs)

File ~\OneDrive\Documents\circuit-breaker-impl\circuit_breaker.py:62, in CircuitBreaker.handle_open_state(self, *args, **kwargs)
     59 current_time = datetime.utcnow().timestamp()
     61 if self.last_attempt_tstamp + self.delay >= current_time:
---> 62     raise RemoteCallFailureException(f"Retry after waiting for {self.last_attempt_tstamp + self.delay - current_time} seconds")
     63 self.set_circuit_state(CircuitStates.HALF_OPEN)
     64 allowed_exceptions = self.exceptions_to_catch

RemoteCallFailureException: Retry after waiting for 6.256181001663208 seconds

In [13]: inst.make_remote_call(success_endpoint)
00:45:50,603 INFO: changed state from open to half_open
00:45:50,603 INFO: changed state from open to half_open
inside make_request
Call to http://127.0.0.1:5000/success succeed with status code = 200
00:45:50,610 INFO: changed state from half_open to closed
00:45:50,610 INFO: changed state from half_open to closed
Out[13]: <Response [200]>
``
