#!/usr/bin/env python3
"""
Caching request module
"""
import redis
import requests
from functools import wraps
from typing import Callable


def track_get_page(fn: Callable) -> Callable:
    """ Decorator for get_page
    """
    @wraps(fn)
    def wrapper(url: str = "http://slowwly.robertomurray.co.uk") -> str:
        """ Wrapper that:
            - check whether a url's data is cached
            - tracks how many times get_page is called
        """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        r = fn(url)
        client.set(f'{url}', r, 10)
        return r
    return wrapper


@track_get_page
def get_page(url: str = "http://slowwly.robertomurray.co.uk") -> str:
    """ Makes a http request to a given endpoint
    """
    r = requests.get(url)
    return r.text
