# circuit-breaker-impl

implementation of  circuit breaker design pattern in python, described in "Release It!"

```
File ~\OneDrive\Documents\circuit-breaker-impl\circuit_breaker.py:62, in CircuitBreaker.handle_open_state(self, *args, **kwargs)
     59 current_time = datetime.utcnow().timestamp()
     61 if self.last_attempt_tstamp + self.delay >= current_time:
---> 62     raise RemoteCallFailureException(f"Retry after waiting for {self.last_attempt_tstamp + self.delay - current_time} seconds")
     63 self.set_circuit_state(CircuitStates.HALF_OPEN)
     64 allowed_exceptions = self.exceptions_to_catch

RemoteCallFailureException: Retry after waiting for 2.4061169624328613 seconds

In [43]:

In [43]: inst.make_remote_call(success_endpoint)
00:50:45,918 INFO: changed state from open to half_open
00:50:45,918 INFO: changed state from open to half_open
inside make_request
Call to http://127.0.0.1:5000/positive succeed with status code = 200
00:50:45,926 INFO: changed state from half_open to closed
00:50:45,926 INFO: changed state from half_open to closed
Out[43]: <Response [200]>

```
