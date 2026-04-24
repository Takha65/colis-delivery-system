"""Chargement du graphe routier depuis un fichier JSON."""
import json
from pathlib import Path

from src.domain.entities import Arete, Graphe, Noeud
from src.domain.exceptions import GrapheInvalideError
from src.domain.value_objects import Coordonnees


def charger_graphe_depuis_json(chemin: str | Path) -> Graphe:
    """Charge un graphe depuis un fichier JSON.

    Format attendu :
    {
      "noeuds": [{"id": "...", "nom": "...", "latitude": ..., "longitude": ...}],
      "aretes": [{"source": "...", "cible": "...", "distance_km": ...,
                  "temps_minutes": ..., "charge_trafic": ...}]
    }
    """
    path = Path(chemin)
    if not path.exists():
        raise GrapheInvalideError(f"Fichier graphe introuvable : {chemin}")

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as exc:
        raise GrapheInvalideError(f"JSON invalide : {exc}") from exc

    graphe = Graphe()

    # Ajouter les noeuds
    for noeud_data in data.get("noeuds", []):
        noeud = Noeud(
            id=noeud_data["id"],
            nom=noeud_data["nom"],
            coordonnees=Coordonnees(
                latitude=noeud_data["latitude"],
                longitude=noeud_data["longitude"],
            ),
        )
        graphe.ajouter_noeud(noeud)

    # Ajouter les aretes (bidirectionnelles par defaut)
    for arete_data in data.get("aretes", []):
        arete = Arete(
            noeud_source=arete_data["source"],
            noeud_cible=arete_data["cible"],
            distance_km=arete_data["distance_km"],
            temps_minutes=arete_data["temps_minutes"],
            charge_trafic=arete_data.get("charge_trafic", 0.0),
        )
        graphe.ajouter_arete(arete, bidirectionnel=True)

    return graphe
