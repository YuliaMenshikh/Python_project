from .services import make_connection


def with_connection(name='db'):
    def decorator(func):
        def wrapper(*args, **kwargs):
            with make_connection(name) as conn:
                return func(conn, *args, **kwargs)
        return wrapper
    return decorator
