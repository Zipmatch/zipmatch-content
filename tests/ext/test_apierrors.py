import pytest

from content.ext.apierrors import APIErrors, _create_error_response


@pytest.mark.parametrize('use_init_app', [True, False])
def test_ext_init(app, mocker, use_init_app):
    mock_init_app = mocker.patch.object(APIErrors, 'init_app')
    if use_init_app:
        ext = APIErrors()
        ext.init_app(app)
    else:
        APIErrors(app)
    assert mock_init_app.called_with(app)


def test_api_errors(app):
    apierr = APIErrors()
    apierr.init_app(app)
    assert 400 in app.error_handler_spec[None]
    assert 404 in app.error_handler_spec[None]
    assert 405 in app.error_handler_spec[None]
    assert 500 in app.error_handler_spec[None]


@pytest.mark.parametrize('code, error, message', [
    (500, None, None), (400, None, 'frogs'), (404, 'test', None)
])
def test_create_error_response(app, code, error, message):
    err = type('Error', (object,), {})
    if message:
        err.description = message
    if not code and not message:
        err = None
    rv, rcode = _create_error_response(code, err)
    assert rcode == code
    if message:
        assert rv.json['message'] == message
    else:
        assert 'message' not in rv.json
