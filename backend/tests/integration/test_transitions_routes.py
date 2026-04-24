"""Tests d'integration des routes de transition et d'historique."""


def _payload_valide() -> dict:
    return {
        "poids_kg": 2.5,
        "longueur_cm": 30,
        "largeur_cm": 20,
        "hauteur_cm": 10,
        "rue_origine": "100 rue A",
        "ville_origine": "Sherbrooke",
        "code_postal_origine": "J1K 1A1",
        "rue_destination": "200 rue B",
        "ville_destination": "Montreal",
        "code_postal_destination": "H3Z 2Y7",
        "type_colis": "STANDARD",
    }


class TestTransiterColis:

    def test_transition_valide_retourne_200(self, client):
        colis = client.post("/api/colis", json=_payload_valide()).json()

        response = client.post(
            f"/api/colis/{colis['id']}/transiter",
            json={"nouvel_etat": "EN_TRANSIT"},
        )

        assert response.status_code == 200
        assert response.json()["statut"] == "EN_TRANSIT"

    def test_transition_invalide_retourne_409(self, client):
        """Impossible de passer de CREE a LIVRE directement."""
        colis = client.post("/api/colis", json=_payload_valide()).json()

        response = client.post(
            f"/api/colis/{colis['id']}/transiter",
            json={"nouvel_etat": "LIVRE"},
        )

        assert response.status_code == 409

    def test_transition_colis_inexistant_retourne_404(self, client):
        response = client.post(
            "/api/colis/00000000-0000-0000-0000-000000000000/transiter",
            json={"nouvel_etat": "EN_TRANSIT"},
        )
        assert response.status_code == 404

    def test_transition_etat_invalide_retourne_422(self, client):
        colis = client.post("/api/colis", json=_payload_valide()).json()
        response = client.post(
            f"/api/colis/{colis['id']}/transiter",
            json={"nouvel_etat": "INCONNU"},
        )
        assert response.status_code == 422

    def test_cycle_complet(self, client):
        colis = client.post("/api/colis", json=_payload_valide()).json()
        colis_id = colis["id"]

        for etat in ["EN_TRANSIT", "LIVRE", "CONFIRME"]:
            r = client.post(f"/api/colis/{colis_id}/transiter", json={"nouvel_etat": etat})
            assert r.status_code == 200

        final = client.get(f"/api/colis/{colis_id}").json()
        assert final["statut"] == "CONFIRME"


class TestHistorique:

    def test_historique_vide_a_la_creation(self, client):
        colis = client.post("/api/colis", json=_payload_valide()).json()
        response = client.get(f"/api/colis/{colis['id']}/historique")
        assert response.status_code == 200
        assert response.json() == []

    def test_historique_apres_transitions(self, client):
        colis = client.post("/api/colis", json=_payload_valide()).json()
        colis_id = colis["id"]

        client.post(
            f"/api/colis/{colis_id}/transiter",
            json={"nouvel_etat": "EN_TRANSIT", "commentaire": "Pris en charge"},
        )
        client.post(f"/api/colis/{colis_id}/transiter", json={"nouvel_etat": "LIVRE"})

        response = client.get(f"/api/colis/{colis_id}/historique")
        assert response.status_code == 200
        historique = response.json()
        assert len(historique) == 2
        assert historique[0]["statut_nouveau"] == "EN_TRANSIT"
        assert historique[0]["commentaire"] == "Pris en charge"
        assert historique[1]["statut_nouveau"] == "LIVRE"
