from content.app import create_app

import pytest


@pytest.fixture
def app():
    return create_app()
