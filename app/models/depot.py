"""Dépôt SQLite des résultats du scraping."""
import sqlite3
from pathlib import Path
from typing import Iterable

from app.models.produit import Produit


class DepotProduits:
    """Enregistre ou actualise les produits avec référence et image."""

    def enregistrer_sqlite(self, produits: Iterable[Produit], chemin: str | Path) -> Path:
        destination = Path(chemin)
        destination.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(destination) as connexion:
            connexion.execute(
                """
                CREATE TABLE IF NOT EXISTS produits (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    titre TEXT NOT NULL,
                    prix TEXT,
                    note TEXT,
                    nombre_avis TEXT,
                    reference TEXT UNIQUE,
                    image TEXT,
                    date_collecte TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            for produit in produits:
                valeurs = (produit.titre, produit.prix, produit.note, produit.nombre_avis, produit.url, produit.image_url)
                if produit.url:
                    existant = connexion.execute(
                        "SELECT id FROM produits WHERE reference = ? OR (reference IS NULL AND titre = ?) LIMIT 1",
                        (produit.url, produit.titre),
                    ).fetchone()
                else:
                    existant = connexion.execute(
                        "SELECT id FROM produits WHERE reference IS NULL AND titre = ? LIMIT 1",
                        (produit.titre,),
                    ).fetchone()

                if existant:
                    connexion.execute(
                        """
                        UPDATE produits
                        SET titre = ?, prix = ?, note = ?, nombre_avis = ?, reference = ?, image = ?,
                            date_collecte = CURRENT_TIMESTAMP
                        WHERE id = ?
                        """,
                        (*valeurs, existant[0]),
                    )
                else:
                    connexion.execute(
                        """
                        INSERT INTO produits (titre, prix, note, nombre_avis, reference, image)
                        VALUES (?, ?, ?, ?, ?, ?)
                        """,
                        valeurs,
                    )
        return destination
