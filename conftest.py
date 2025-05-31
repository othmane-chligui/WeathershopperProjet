import pytest
import allure
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from utils.config import Config
from utils.logger import logger


@pytest.fixture(scope="function")
def browser(request):
    # Configuration du navigateur
    edge_options = Options()
    if Config.browser_headless:
        edge_options.add_argument("--headless")
        edge_options.add_argument("--disable-gpu")

    driver = webdriver.Edge(options=edge_options)
    driver.maximize_window()
    driver.implicitly_wait(Config.WAIT_TIMEOUT)
    logger.info("Initialisation du navigateur")

    # Ajouter le driver à l'objet request pour accès dans les tests
    request.cls.driver = driver if hasattr(request, 'cls') else driver
    yield driver

    logger.info("Fermeture du navigateur")
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()

    # Capturer les screenshots sur échec
    if rep.when in ("call", "setup", "teardown") and rep.failed:
        driver = getattr(item.cls, 'driver', None) if hasattr(item, 'cls') else item.funcargs.get('browser')
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"screenshot_{rep.when}",
                attachment_type=allure.attachment_type.PNG
            )