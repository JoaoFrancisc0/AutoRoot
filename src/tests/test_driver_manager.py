from src.common import driver_manager

def test_configure_driver_options():
    options = driver_manager.configure_driver_options()
    
    assert "--headless" in options.arguments
    assert isinstance(options.experimental_options, dict)
    assert "prefs" in options.experimental_options
    assert "safebrowsing.enabled" in options.experimental_options["prefs"]


def test_start_driver_mock(mocker):
    mock_chrome = mocker.patch("src.common.driver_manager.webdriver.Chrome")
    mock_manager = mocker.patch("src.common.driver_manager.ChromeDriverManager")
    
    mock_manager().install.return_value = "fake/path/to/driver"
    
    options = driver_manager.configure_driver_options()
    driver_manager.start_driver(options)
    
    mock_chrome.assert_called_once()
    mock_manager().install.assert_called_once()
