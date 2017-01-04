import logging

import pytest

from content.ext.applogging import AppLogging


@pytest.mark.parametrize('use_init_app', [True, False])
def test_ext_init(app, mocker, use_init_app):
    mock_init_app = mocker.patch.object(AppLogging, 'init_app')
    if use_init_app:
        ext = AppLogging()
        ext.init_app(app)
    else:
        AppLogging(app)
    assert mock_init_app.called_with(app)


def test_applogging(app):
    app.testing = False
    applog = AppLogging()
    applog.init_app(app)
    app.logger.isEnabledFor(logging.INFO)
    assert app.logger.getEffectiveLevel() == logging.INFO
    assert app.logger.hasHandlers()
