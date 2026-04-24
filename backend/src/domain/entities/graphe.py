"""Entites du graphe routier."""

from dataclasses import dataclass, field

from src.domain.exceptions import NoeudIntrouvableError
from src.domain.value_objects import Coordonnees


@dataclass(frozen=True)
class Arete:
    """Arete entre deux noeuds (route entre deux points).

    Caracteristiques :
    - distance_km : longueur en km
    - temps_minutes : duree de parcours en minutes
    - charge_trafic : niveau de trafic (0.0 = libre, 1.0 = bouchon)
    """

    noeud_source: str  # ID du noeud de depart
    noeud_cible: str  # ID du noeud d'arrivee
    distance_km: float
    temps_minutes: float
    charge_trafic: float = 0.0  # Entre 0 et 1


@dataclass
class Noeud:
    """Noeud du graphe (point de livraison)."""

    id: str
    nom: str  # Ex: "Sherbrooke"
    coordonnees: Coordonnees


@dataclass
class Graphe:
    """Graphe routier (nœuds + aretes).

    Les aretes sont indexees par noeud source pour un acces rapide.
    Pour representer un graphe non dirige, chaque arete est stockee
    dans les deux sens.
    """

    noeuds: dict[str, Noeud] = field(default_factory=dict)
    aretes_par_source: dict[str, list[Arete]] = field(default_factory=dict)

    def ajouter_noeud(self, noeud: Noeud) -> None:
        self.noeuds[noeud.id] = noeud
        self.aretes_par_source.setdefault(noeud.id, [])

    def ajouter_arete(self, arete: Arete, bidirectionnel: bool = True) -> None:
        """Ajoute une arete au graphe (bidirectionnelle par defaut)."""
        if arete.noeud_source not in self.noeuds:
            raise NoeudIntrouvableError(arete.noeud_source)
        if arete.noeud_cible not in self.noeuds:
            raise NoeudIntrouvableError(arete.noeud_cible)

        self.aretes_par_source[arete.noeud_source].append(arete)
        if bidirectionnel:
            arete_retour = Arete(
                noeud_source=arete.noeud_cible,
                noeud_cible=arete.noeud_source,
                distance_km=arete.distance_km,
                temps_minutes=arete.temps_minutes,
                charge_trafic=arete.charge_trafic,
            )
            self.aretes_par_source[arete.noeud_cible].append(arete_retour)

    def voisins(self, noeud_id: str) -> list[Arete]:
        """Retourne les aretes sortantes d'un noeud."""
        if noeud_id not in self.noeuds:
            raise NoeudIntrouvableError(noeud_id)
        return self.aretes_par_source.get(noeud_id, [])

    def noeud(self, noeud_id: str) -> Noeud:
        """Retourne un noeud par son id."""
        if noeud_id not in self.noeuds:
            raise NoeudIntrouvableError(noeud_id)
        return self.noeuds[noeud_id]
