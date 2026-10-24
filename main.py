"""Point d'entrée du scraper Amazon Selenium."""
import argparse
import logging

from app.controllers.scraping_controller import ScrapingController
from app.views.console_view import ConsoleView
from app.views.export_view import ExportView
from config import DEFAULT_DATABASE, DEFAULT_LIMIT, DEFAULT_SEARCH_URL, MAX_LIMIT


def parse_args():
    parser = argparse.ArgumentParser(description="Scraper jusqu'à 10 casques Bluetooth sans fil sur Amazon.")
    parser.add_argument("--url", default=DEFAULT_SEARCH_URL, help="URL Amazon de résultats de recherche")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="Nombre maximal de produits (1 à 10)")
    parser.add_argument("--database", default=str(DEFAULT_DATABASE), help="Chemin de la base SQLite")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--headless", dest="headless", action="store_true", help="Lancer Chrome en arrière-plan")
    mode.add_argument("--visible", dest="headless", action="store_false", help="Afficher Chrome pendant la collecte (défaut)")
    parser.set_defaults(headless=False)
    return parser.parse_args()


def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    args = parse_args()
    if args.limit < 1:
        raise SystemExit("La limite doit être au moins 1.")
    limit = min(args.limit, MAX_LIMIT)
    if args.limit > MAX_LIMIT:
        logging.warning("La limite demandée est plafonnée à %s produits.", MAX_LIMIT)

    controller = ScrapingController(ConsoleView(), ExportView())
    try:
        produits = controller.scrape(args.url, limit=limit, headless=args.headless)
    except Exception as exc:
        logging.error("Le scraping a échoué : %s", exc)
        raise SystemExit(1) from exc
    if not produits:
        logging.warning("Aucun produit n'a été trouvé.")
        return
    database_path = controller.export(produits, args.database)
    controller.display(produits)
    logging.info("%s produit(s) enregistré(s) dans %s", len(produits), database_path)


if __name__ == "__main__":
    main()

