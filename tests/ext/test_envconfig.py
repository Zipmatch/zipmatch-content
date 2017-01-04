import pytest

from content.ext.envconfig import EnvConfig


@pytest.mark.parametrize('use_init_app', [True, False])
def test_ext_init(app, mocker, use_init_app):
    mock_init_app = mocker.patch.object(EnvConfig, 'init_app')
    if use_init_app:
        ext = EnvConfig()
        ext.init_app(app)
    else:
        EnvConfig(app)
    assert mock_init_app.called_with(app)


@pytest.mark.parametrize('value, expected', [
    (1, 1),
    ('x', 'x'),
    ('[1, "x"]', [1, 'x']),
    ('123abc', '123abc')
])
def test_envconfig(app, monkeypatch, value, expected):
    monkeypatch.setenv('APP_TEST_VALUE', value)
    env = EnvConfig()
    env.init_app(app)
    assert app.config['TEST_VALUE'] == expected
