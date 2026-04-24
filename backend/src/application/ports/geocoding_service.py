"""Port : interface d'un service de geocodage d'adresses."""
from abc import ABC, abstractmethod
from typing import Optional

from src.domain.value_objects import Adresse, Coordonnees


class IGeocodingService(ABC):
    """Interface d'un service de geocodage.

    Implementations possibles :
    - NominatimGeocodingAdapter (production, API OpenStreetMap)
    - GeocodingCacheProxy (cache par-dessus un autre service)
    - FakeGeocodingService (tests)
    """

    @abstractmethod
    def geocoder(self, adresse: Adresse) -> Optional[Coordonnees]:
        """Convertit une adresse en coordonnees GPS.

        Returns:
            Coordonnees si l'adresse est trouvee, None sinon.
        """
