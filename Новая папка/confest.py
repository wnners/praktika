import pytest
import os
from helium import kill_browser

@pytest.fixture(scope='function')
def browser_context():
    if not os.path.exists('report'):
        os.makedirs('report')
    yield
    kill_browser()