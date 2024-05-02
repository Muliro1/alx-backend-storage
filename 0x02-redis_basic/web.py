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
    def wrapper(url: str) -> str:
        """ Wrapper that:
            - check whether a url's data is cached
        """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cache_page = client.get(f'{url}')
        if cache_page:
            return cache_page.decode('utf-8')
        response = fn(url)
        client.set(f'{url}', response, 10)
        return response
    return wrapper


@track_get_page
def get_page(url: str) -> str:
    """ Makes a http request to a given endpoint
    """
    response = requests.get(url)
    print(response.text)
if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
