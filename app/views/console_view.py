"""Affichage console des produits collectés."""


class ConsoleView:
    def afficher_produits(self, produits):
        print(f"\n{len(produits)} casque(s) Bluetooth sans fil trouvé(s)\n")
        for index, produit in enumerate(produits, start=1):
            print(f"{index}. {produit.titre}")
            print(f"   Prix : {produit.prix or 'Non indiqué'}")
            print(f"   Note : {produit.note or 'Non indiquée'} | Avis : {produit.nombre_avis or 'Non indiqué'}")
            if produit.url:
                print(f"   Référence : {produit.url}")
            if produit.image_url:
                print(f"   Image : {produit.image_url}")
            print()
