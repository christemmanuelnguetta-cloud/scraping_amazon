"""Confirmation de l'enregistrement SQLite."""


class ExportView:
    def confirmer_export(self, chemin, nombre):
        print(f"Base SQLite mise à jour : {nombre} produit(s) -> {chemin}")
