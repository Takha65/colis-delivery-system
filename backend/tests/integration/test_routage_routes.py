"""Tests d'integration des routes M2 (livreurs, routage, graphe)."""


def _creer_livreur(client, nom="Jean Dupont") -> dict:
    response = client.post(
        "/api/livreurs",
        json={
            "nom": nom,
            "capacite_max_kg": 50.0,
            "position_depart_id": "SHE",
        },
    )
    assert response.status_code == 201
    return response.json()


class TestLivreurs:

    def test_creer_livreur(self, client):
        response = client.post(
            "/api/livreurs",
            json={
                "nom": "Marie Tremblay",
                "capacite_max_kg": 75.0,
                "position_depart_id": "MTL",
            },
        )
        assert response.status_code == 201
        data = response.json()
        assert data["nom"] == "Marie Tremblay"
        assert data["capacite_max_kg"] == 75.0

    def test_creer_livreur_capacite_negative_retourne_422(self, client):
        response = client.post(
            "/api/livreurs",
            json={
                "nom": "Test",
                "capacite_max_kg": -5.0,
                "position_depart_id": "SHE",
            },
        )
        assert response.status_code == 422

    def test_lister_livreurs(self, client):
        _creer_livreur(client, "Livreur 1")
        _creer_livreur(client, "Livreur 2")

        response = client.get("/api/livreurs")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestGraphe:

    def test_obtenir_graphe(self, client):
        response = client.get("/api/graphe")
        assert response.status_code == 200
        data = response.json()
        # Graphe reel : 8 noeuds
        assert len(data["noeuds"]) == 8
        # Verifier un noeud connu
        noms = {n["nom"] for n in data["noeuds"]}
        assert "Sherbrooke" in noms
        assert "Montreal" in noms


class TestStrategies:

    def test_lister_strategies(self, client):
        response = client.get("/api/strategies")
        assert response.status_code == 200
        data = response.json()
        noms = {s["nom"] for s in data}
        assert noms == {"DIJKSTRA", "PLUS_PROCHE_VOISIN", "GREEDY"}


class TestCalculerRoute:

    def test_calculer_route_simple(self, client):
        livreur = _creer_livreur(client)

        response = client.post(
            "/api/routes/calculer",
            json={
                "livreur_id": livreur["id"],
                "noeud_depart": "SHE",
                "noeuds_a_visiter": ["MAG", "MTL"],
                "poids_distance": 0.5,
                "poids_temps": 0.3,
                "poids_charge": 0.2,
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["livreur_id"] == livreur["id"]
        assert data["strategie_utilisee"] == "DIJKSTRA"  # auto pour 2 colis
        assert data["nombre_arrets"] == 3  # depart + 2 arrets
        assert data["distance_totale_km"] > 0

    def test_calculer_route_avec_strategie_explicite(self, client):
        livreur = _creer_livreur(client)

        response = client.post(
            "/api/routes/calculer",
            json={
                "livreur_id": livreur["id"],
                "noeud_depart": "SHE",
                "noeuds_a_visiter": ["MAG", "GRA", "MTL"],
                "poids_distance": 0.5,
                "poids_temps": 0.3,
                "poids_charge": 0.2,
                "strategie": "GREEDY",
            },
        )
        assert response.status_code == 200
        assert response.json()["strategie_utilisee"] == "GREEDY"

    def test_calculer_route_noeud_inconnu_retourne_404(self, client):
        livreur = _creer_livreur(client)

        response = client.post(
            "/api/routes/calculer",
            json={
                "livreur_id": livreur["id"],
                "noeud_depart": "INEXISTANT",
                "noeuds_a_visiter": ["MTL"],
            },
        )
        assert response.status_code == 404

    def test_calculer_route_criteres_invalides_retourne_400(self, client):
        """La somme des poids doit etre 1.0."""
        livreur = _creer_livreur(client)

        response = client.post(
            "/api/routes/calculer",
            json={
                "livreur_id": livreur["id"],
                "noeud_depart": "SHE",
                "noeuds_a_visiter": ["MTL"],
                "poids_distance": 0.5,
                "poids_temps": 0.5,
                "poids_charge": 0.5,  # total = 1.5
            },
        )
        assert response.status_code == 400

    def test_calculer_route_visite_tous_les_noeuds(self, client):
        livreur = _creer_livreur(client)

        response = client.post(
            "/api/routes/calculer",
            json={
                "livreur_id": livreur["id"],
                "noeud_depart": "SHE",
                "noeuds_a_visiter": ["MAG", "GRA", "DRU"],
            },
        )
        data = response.json()
        noeuds_visites = {e["noeud_id"] for e in data["etapes"]}
        assert {"SHE", "MAG", "GRA", "DRU"} == noeuds_visites
