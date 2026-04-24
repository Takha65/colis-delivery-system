"""Adapter pour l'API Nominatim (OpenStreetMap).

Pattern Adapter : convertit l'interface de l'API Nominatim vers notre
interface IGeocodingService. Le domaine ne connait rien de Nominatim.
"""

import logging
import time
from typing import Optional

import httpx

from src.application.ports import IGeocodingService
from src.domain.value_objects import Adresse, Coordonnees
from src.shared.config import settings

logger = logging.getLogger(__name__)


class NominatimGeocodingAdapter(IGeocodingService):
    """Adapte l'API HTTP Nominatim a l'interface IGeocodingService.

    Respecte la politique d'utilisation Nominatim :
    - User-Agent identifiable (avec email)
    - Maximum 1 requete par seconde
    - Timeout raisonnable
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        user_agent: Optional[str] = None,
        timeout_seconds: Optional[int] = None,
    ) -> None:
        self._base_url = (base_url or settings.nominatim_base_url).rstrip("/")
        self._user_agent = user_agent or settings.nominatim_user_agent
        self._timeout = timeout_seconds or settings.nominatim_timeout_seconds
        self._dernier_appel: float = 0.0

    def geocoder(self, adresse: Adresse) -> Optional[Coordonnees]:
        """Convertit une adresse en coordonnees GPS via Nominatim."""
        self._respecter_rate_limit()

        url = f"{self._base_url}/search"
        params = {
            "q": adresse.ligne_complete(),
            "format": "json",
            "limit": 1,
        }
        headers = {"User-Agent": self._user_agent}

        try:
            response = httpx.get(url, params=params, headers=headers, timeout=self._timeout)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPError as exc:
            logger.warning("Erreur Nominatim pour '%s': %s", adresse, exc)
            return None

        if not data:
            logger.info("Adresse '%s' non trouvee par Nominatim", adresse)
            return None

        try:
            premier_resultat = data[0]
            return Coordonnees(
                latitude=float(premier_resultat["lat"]),
                longitude=float(premier_resultat["lon"]),
            )
        except (KeyError, ValueError, TypeError) as exc:
            logger.warning("Reponse Nominatim mal formee pour '%s': %s", adresse, exc)
            return None

    def _respecter_rate_limit(self) -> None:
        """Assure 1 seconde minimum entre 2 appels (politique Nominatim)."""
        maintenant = time.time()
        ecart = maintenant - self._dernier_appel
        if ecart < 1.0:
            time.sleep(1.0 - ecart)
        self._dernier_appel = time.time()
