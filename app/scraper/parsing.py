"""Extraction robuste des champs produit depuis les résultats Amazon."""
import re
from urllib.parse import urljoin

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

from app.models.produit import Produit


def _valeur(element, selecteurs):
    """Lit aussi le contenu textuel des éléments Amazon masqués à l'écran."""
    for selecteur in selecteurs:
        try:
            champ = element.find_element(By.CSS_SELECTOR, selecteur)
        except NoSuchElementException:
            continue
        for attribut in ("aria-label", "title", "textContent"):
            valeur = champ.get_attribute(attribut)
            if valeur and valeur.strip():
                return " ".join(valeur.split())
        valeur = champ.text.strip()
        if valeur:
            return " ".join(valeur.split())
    return None


def _nombre_avis(carte):
    """N'accepte que le texte d'un compteur numérique, jamais un lien publicitaire."""
    selecteurs = (
        "a[href*='customerReviews'] span",
        "a.s-underline-text span",
        "span.s-underline-text",
    )
    for selecteur in selecteurs:
        for champ in carte.find_elements(By.CSS_SELECTOR, selecteur):
            valeur = champ.get_attribute("textContent") or champ.text
            valeur = " ".join(valeur.split()) if valeur else ""
            if valeur and any(caractere.isdigit() for caractere in valeur):
                if "publicit" not in valeur.lower():
                    return valeur
    return None


def _href_produit(carte, base_url):
    """Utilise l'ASIN pour bâtir une référence stable, puis cherche les liens directs."""
    asin = carte.get_attribute("data-asin")
    if asin:
        return urljoin(base_url, f"/dp/{asin}")
    for selecteur in (
        "h2 a[href]",
        "a.a-link-normal[href*='/dp/']",
        "a[href*='/dp/']",
        "a[href*='/gp/aw/d/']",
    ):
        try:
            href = carte.find_element(By.CSS_SELECTOR, selecteur).get_attribute("href")
        except NoSuchElementException:
            continue
        if href:
            return urljoin(base_url, href)
    return None


def analyser_cartes(driver, limite: int, base_url: str) -> list[Produit]:
    produits = []
    cartes = driver.find_elements(By.CSS_SELECTOR, "div[data-component-type='s-search-result']")
    for carte in cartes:
        if len(produits) >= limite:
            break
        titre = _valeur(carte, ["h2 a span", "h2 span", "h2"])
        if not titre:
            continue

        reference = _href_produit(carte, base_url)
        try:
            image_element = carte.find_element(By.CSS_SELECTOR, "img.s-image")
            image = image_element.get_attribute("src") or image_element.get_attribute("data-src")
        except NoSuchElementException:
            image = None

        prix = _valeur(carte, [".a-price .a-offscreen", "span.a-price"])
        note = _valeur(carte, [".a-icon-star-small .a-icon-alt", ".a-icon-alt", "[aria-label*='étoile']"])
        avis = _nombre_avis(carte)
        produits.append(Produit(
            titre=titre,
            prix=prix,
            note=note,
            nombre_avis=avis,
            url=reference,
            image_url=image,
        ))
    return produits
