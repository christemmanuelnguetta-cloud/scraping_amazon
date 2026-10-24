"""Coordonne le scraping, l'affichage et l'enregistrement."""
from app.models.depot import DepotProduits
from app.scraper.amazon_scraper import AmazonScraper


class ScrapingController:
    def __init__(self, console_view, export_view, scraper=None, depot=None):
        self.console_view = console_view
        self.export_view = export_view
        self.scraper = scraper or AmazonScraper()
        self.depot = depot or DepotProduits()

    def scrape(self, url, limit=10, headless=False):
        return self.scraper.scraper(url, limite=limit, headless=headless)

    def display(self, produits):
        self.console_view.afficher_produits(produits)

    def export(self, produits, chemin):
        destination = self.depot.enregistrer_sqlite(produits, chemin)
        self.export_view.confirmer_export(destination, len(produits))
        return destination
