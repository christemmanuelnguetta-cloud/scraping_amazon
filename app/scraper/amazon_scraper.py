"""Navigation Amazon et collecte Selenium des casques."""
import logging
from urllib.parse import urlparse

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from app.scraper.driver import creer_driver
from app.scraper.parsing import analyser_cartes
from config import MAX_LIMIT, PAGE_LOAD_TIMEOUT_SECONDS

logger = logging.getLogger(__name__)


class AmazonScraper:
    def __init__(self, timeout: int = PAGE_LOAD_TIMEOUT_SECONDS):
        self.timeout = timeout

    def scraper(self, url: str, limite: int = MAX_LIMIT, headless: bool = False):
        limite = max(1, min(int(limite), MAX_LIMIT))
        domaine = urlparse(url).hostname or ""
        if not domaine.endswith("amazon.fr") and not domaine.endswith("amazon.com") and ".amazon." not in domaine:
            raise ValueError("L'URL doit pointer vers un domaine Amazon.")

        driver = creer_driver(headless=headless)
        try:
            driver.set_page_load_timeout(self.timeout)
            logger.info("Ouverture de la recherche Amazon : %s", url)
            driver.get(url)
            try:
                WebDriverWait(driver, self.timeout).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-component-type='s-search-result']"))
                )
            except TimeoutException:
                logger.warning("Délai dépassé en attendant les résultats Amazon.")

            produits = analyser_cartes(driver, limite, url)
            if not produits:
                titre_page = driver.title or "(sans titre)"
                texte_page = ""
                try:
                    texte_page = driver.find_element(By.TAG_NAME, "body").text[:350].replace("\n", " ")
                except WebDriverException:
                    pass
                extrait = f" Contenu affiché : {texte_page}" if texte_page else ""
                raise RuntimeError(
                    f"Aucun produit détecté sur Amazon. Titre de page : {titre_page}.{extrait}"
                )
            return produits
        except WebDriverException as exc:
            raise RuntimeError(f"Erreur du navigateur Selenium : {exc}") from exc
        finally:
            driver.quit()
