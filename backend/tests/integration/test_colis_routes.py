"""Tests d'integration des routes API des colis."""
from uuid import uuid4


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


class TestCreerColisEndpoint:

    def test_post_cree_colis_retourne_201(self, client):
        response = client.post("/api/colis", json=_payload_valide())
        assert response.status_code == 201
        data = response.json()
        assert data["statut"] == "CREE"
        assert data["tracking_number"].startswith("CLS-")

    def test_post_sans_poids_retourne_422(self, client):
        payload = _payload_valide()
        del payload["poids_kg"]
        response = client.post("/api/colis", json=payload)
        assert response.status_code == 422

    def test_post_poids_negatif_retourne_422(self, client):
        payload = _payload_valide()
        payload["poids_kg"] = -5
        response = client.post("/api/colis", json=payload)
        assert response.status_code == 422

    def test_post_type_invalide_retourne_422(self, client):
        payload = _payload_valide()
        payload["type_colis"] = "INCONNU"
        response = client.post("/api/colis", json=payload)
        assert response.status_code == 422


class TestListerColisEndpoint:

    def test_get_liste_vide(self, client):
        response = client.get("/api/colis")
        assert response.status_code == 200
        assert response.json() == []

    def test_get_liste_apres_creation(self, client):
        client.post("/api/colis", json=_payload_valide())
        client.post("/api/colis", json=_payload_valide())
        response = client.get("/api/colis")
        assert response.status_code == 200
        assert len(response.json()) == 2


class TestObtenirColisEndpoint:

    def test_get_colis_existant(self, client):
        create_resp = client.post("/api/colis", json=_payload_valide())
        colis_id = create_resp.json()["id"]

        response = client.get(f"/api/colis/{colis_id}")
        assert response.status_code == 200
        assert response.json()["id"] == colis_id

    def test_get_colis_inexistant_retourne_404(self, client):
        response = client.get(f"/api/colis/{uuid4()}")
        assert response.status_code == 404

    def test_get_id_invalide_retourne_422(self, client):
        response = client.get("/api/colis/not-a-uuid")
        assert response.status_code == 422


class TestSupprimerColisEndpoint:

    def test_delete_colis_existant(self, client):
        create_resp = client.post("/api/colis", json=_payload_valide())
        colis_id = create_resp.json()["id"]

        response = client.delete(f"/api/colis/{colis_id}")
        assert response.status_code == 204

        # Verifier qu'il est bien supprime
        get_resp = client.get(f"/api/colis/{colis_id}")
        assert get_resp.status_code == 404

    def test_delete_colis_inexistant_retourne_404(self, client):
        response = client.delete(f"/api/colis/{uuid4()}")
        assert response.status_code == 404
