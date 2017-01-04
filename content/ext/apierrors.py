from functools import partial

from flask import jsonify


class APIErrors(object):
    def __init__(self, app=None, errors=None):
        self.app = app
        if app is not None:
            self.init_app(app, errors)

    def init_app(self, app, errors=None):
        if not errors:
            errors = set((400, 404, 405, 500))
        for code in errors:
            app.register_error_handler(code, partial(_create_error_response, code))


def _create_error_response(code, error):
    """ Create a JSON error response based on the error. """
    data = {}
    try:
        data['error'] = error.name
    except AttributeError:
        if code == 500:
            data['error'] = 'Internal Server Error'
        else:
            data['error'] = '{} error'.format(code)
    try:
        data['message'] = error.description
    except AttributeError:
        pass
    return jsonify(data), code
