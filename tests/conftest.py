# Dash registers `dash.testing.plugin` via setuptools entry points, so `dash_duo`
# is available without `pytest_plugins` here (duplicating it raises ValueError).


def pytest_configure(config):
    """Put a matching chromedriver on PATH for Selenium (used by dash_duo)."""
    import chromedriver_autoinstaller

    chromedriver_autoinstaller.install()
