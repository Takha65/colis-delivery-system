"""Proxy de cache pour le service de geocodage.

Pattern Proxy : intercepte les appels pour ajouter du cache en memoire,
sans changer l'interface. Respecte strictement le contrat IGeocodingService.
"""

import logging
from typing import Optional

from src.application.ports import IGeocodingService
from src.domain.value_objects import Adresse, Coordonnees

logger = logging.getLogger(__name__)


class GeocodingCacheProxy(IGeocodingService):
    """Proxy qui cache les resultats de geocodage en memoire.

    Avantages :
    - Evite les appels repetes a l'API externe pour la meme adresse
    - Respect du rate limit Nominatim
    - Transparent pour le client (meme interface)
    """

    def __init__(self, service_interne: IGeocodingService) -> None:
        self._service = service_interne
        self._cache: dict[str, Optional[Coordonnees]] = {}

    def geocoder(self, adresse: Adresse) -> Optional[Coordonnees]:
        """Retourne le cache si present, sinon delegue au service interne."""
        cle = self._cle_cache(adresse)

        if cle in self._cache:
            logger.debug("Cache hit pour '%s'", adresse)
            return self._cache[cle]

        logger.debug("Cache miss pour '%s', appel du service", adresse)
        resultat = self._service.geocoder(adresse)
        self._cache[cle] = resultat
        return resultat

    def vider_cache(self) -> None:
        """Vide le cache (utile pour tests ou refresh manuel)."""
        self._cache.clear()

    def taille_cache(self) -> int:
        """Retourne le nombre d'entrees en cache."""
        return len(self._cache)

    @staticmethod
    def _cle_cache(adresse: Adresse) -> str:
        """Normalise l'adresse en cle de cache."""
        return adresse.ligne_complete().lower().strip()
