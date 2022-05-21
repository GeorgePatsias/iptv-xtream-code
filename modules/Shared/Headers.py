import functools
from flask import make_response


def headers(view):
    @functools.wraps(view)
    def no_cache_impl(*args, **kwargs):
        response = make_response(view(*args, **kwargs))
        # response.headers['Expires'] = '-1'
        # response.headers['Pragma'] = 'no-cache'
        response.headers['Server'] = 'Microsoft' #Static files not getting the HEADERS
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, max-age=0'
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'

        return response

    return functools.update_wrapper(no_cache_impl, view)
