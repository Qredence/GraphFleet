RateLimiter
===========

|PyPI Version| |Build Status| |Python Version| |License|

Simple Python module providing rate limiting.

Overview
--------

This package provides the ``ratelimiter`` module, which ensures that an
operation will not be executed more than a given number of times on a
given period. This can prove useful when working with third parties APIs
which require for example a maximum of 10 requests per second.

Usage
-----

Decorator
~~~~~~~~~

.. code:: python

    from ratelimiter import RateLimiter

    @RateLimiter(max_calls=10, period=1)
    def do_something():
        pass

Context Manager
~~~~~~~~~~~~~~~

.. code:: python

    from ratelimiter import RateLimiter

    rate_limiter = RateLimiter(max_calls=10, period=1)

    for i in range(100):
        with rate_limiter:
            do_something()

Callback
~~~~~~~~

The callback is called in its own thread, so your callback may use
``sleep`` without delaying the rate limiter.

.. code:: python

    import time

    from ratelimiter import RateLimiter

    def limited(until):
        duration = int(round(until - time.time()))
        print('Rate limited, sleeping for {:d} seconds'.format(duration))

    rate_limiter = RateLimiter(max_calls=2, period=3, callback=limited)

    for i in range(3):
        with rate_limiter:
            print('Iteration', i)

Output:

::

    Iteration 0
    Iteration 1
    Rate limited, sleeping for 3 seconds
    Iteration 2

asyncio
~~~~~~~

The ``RateLimiter`` object can be used in an ``async with`` statement on
Python 3.5+. Note that the callback must be a coroutine in this context.
The coroutine callback is not called in a separate thread.

.. code:: python

    import asyncio
    import time

    from ratelimiter import RateLimiter

    async def limited(until):
        duration = int(round(until - time.time()))
        print('Rate limited, sleeping for {:d} seconds'.format(duration))

    async def coro():
        rate_limiter = RateLimiter(max_calls=2, period=3, callback=limited)
        for i in range(3):
            async with rate_limiter:
                print('Iteration', i)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(coro())

License
-------

| Original work Copyright 2013 Arnaud Porterie
| Modified work Copyright 2016 Frazer McLean

Licensed under the Apache License, Version 2.0 (the “License”); you may
not use this file except in compliance with the License. You may obtain
a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an “AS IS” BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

.. |PyPI Version| image:: http://img.shields.io/pypi/v/ratelimiter.svg?style=flat-square
   :target: https://pypi.python.org/pypi/ratelimiter
.. |Build Status| image:: http://img.shields.io/travis/RazerM/ratelimiter/master.svg?style=flat-square
   :target: https://travis-ci.org/RazerM/ratelimiter
.. |Python Version| image:: https://img.shields.io/badge/python-2.7%2C%203-brightgreen.svg?style=flat-square
   :target: https://www.python.org/downloads/
.. |License| image:: http://img.shields.io/badge/license-Apache-blue.svg?style=flat-square
   :target: https://github.com/RazerM/ratelimiter/blob/master/LICENSE


