"""Fake service de geocodage pour les tests."""
from typing import Optional

from src.application.ports import IGeocodingService
from src.domain.value_objects import Adresse, Coordonnees


class FakeGeocodingService(IGeocodingService):
    """Service de geocodage factice pour les tests.

    Peut etre configure pour :
    - Retourner des coordonnees fixes
    - Compter les appels (verifier que le cache fonctionne)
    - Simuler des echecs
    """

    def __init__(
        self,
        coordonnees_par_defaut: Optional[Coordonnees] = None,
        doit_echouer: bool = False,
    ) -> None:
        self._coordonnees = coordonnees_par_defaut or Coordonnees(
            latitude=45.4000, longitude=-71.9000  # Sherbrooke par defaut
        )
        self._doit_echouer = doit_echouer
        self.compteur_appels = 0

    def geocoder(self, adresse: Adresse) -> Optional[Coordonnees]:
        self.compteur_appels += 1
        if self._doit_echouer:
            return None
        return self._coordonnees
