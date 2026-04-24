"""Tests unitaires du GeocodingCacheProxy."""
import pytest

from src.domain.value_objects import Adresse, Coordonnees
from src.infrastructure.external import GeocodingCacheProxy
from tests.fakes.fake_geocoding_service import FakeGeocodingService


@pytest.fixture
def adresse_sherbrooke() -> Adresse:
    return Adresse(
        rue="2500 Boul Universite",
        ville="Sherbrooke",
        code_postal="J1K 2R1",
    )


@pytest.fixture
def adresse_montreal() -> Adresse:
    return Adresse(
        rue="1 rue Saint-Laurent",
        ville="Montreal",
        code_postal="H2W 1Y3",
    )


class TestGeocodingCacheProxy:

    def test_premier_appel_delegue_au_service(self, adresse_sherbrooke) -> None:
        fake = FakeGeocodingService()
        proxy = GeocodingCacheProxy(fake)

        resultat = proxy.geocoder(adresse_sherbrooke)

        assert resultat is not None
        assert fake.compteur_appels == 1

    def test_appel_repete_utilise_cache(self, adresse_sherbrooke) -> None:
        fake = FakeGeocodingService()
        proxy = GeocodingCacheProxy(fake)

        proxy.geocoder(adresse_sherbrooke)
        proxy.geocoder(adresse_sherbrooke)
        proxy.geocoder(adresse_sherbrooke)

        # 1 seul appel reel malgre 3 requetes
        assert fake.compteur_appels == 1
        assert proxy.taille_cache() == 1

    def test_adresses_differentes_appellent_service(
        self, adresse_sherbrooke, adresse_montreal
    ) -> None:
        fake = FakeGeocodingService()
        proxy = GeocodingCacheProxy(fake)

        proxy.geocoder(adresse_sherbrooke)
        proxy.geocoder(adresse_montreal)

        assert fake.compteur_appels == 2
        assert proxy.taille_cache() == 2

    def test_retourne_meme_resultat_que_service_interne(
        self, adresse_sherbrooke
    ) -> None:
        coord_attendue = Coordonnees(latitude=45.5, longitude=-72.5)
        fake = FakeGeocodingService(coordonnees_par_defaut=coord_attendue)
        proxy = GeocodingCacheProxy(fake)

        resultat = proxy.geocoder(adresse_sherbrooke)

        assert resultat == coord_attendue

    def test_echec_du_service_pas_mis_en_cache_comme_valeur(
        self, adresse_sherbrooke
    ) -> None:
        """Si le service retourne None, on cache aussi None (evite re-essayer)."""
        fake = FakeGeocodingService(doit_echouer=True)
        proxy = GeocodingCacheProxy(fake)

        resultat1 = proxy.geocoder(adresse_sherbrooke)
        resultat2 = proxy.geocoder(adresse_sherbrooke)

        assert resultat1 is None
        assert resultat2 is None
        assert fake.compteur_appels == 1  # Pas de nouvel appel

    def test_vider_cache(self, adresse_sherbrooke) -> None:
        fake = FakeGeocodingService()
        proxy = GeocodingCacheProxy(fake)

        proxy.geocoder(adresse_sherbrooke)
        proxy.vider_cache()
        proxy.geocoder(adresse_sherbrooke)

        assert fake.compteur_appels == 2
        assert proxy.taille_cache() == 1

    def test_cle_cache_insensible_a_la_casse(self) -> None:
        fake = FakeGeocodingService()
        proxy = GeocodingCacheProxy(fake)

        adr1 = Adresse(rue="100 rue A", ville="Sherbrooke", code_postal="J1K 1A1")
        adr2 = Adresse(rue="100 RUE A", ville="SHERBROOKE", code_postal="J1K 1A1")

        proxy.geocoder(adr1)
        proxy.geocoder(adr2)

        # Normalisation -> 1 seule cle
        assert fake.compteur_appels == 1


class TestProxySubstitutable:
    """Le Proxy respecte l'interface (LSP)."""

    def test_meme_interface_que_service_interne(self, adresse_sherbrooke) -> None:
        """Un Proxy doit pouvoir remplacer n'importe quel IGeocodingService."""
        fake = FakeGeocodingService()
        proxy = GeocodingCacheProxy(fake)

        # Les deux doivent etre utilisables via IGeocodingService
        from src.application.ports import IGeocodingService
        assert isinstance(fake, IGeocodingService)
        assert isinstance(proxy, IGeocodingService)

        # Et retourner le meme type de resultat
        res_direct = fake.geocoder(adresse_sherbrooke)
        proxy2 = GeocodingCacheProxy(FakeGeocodingService())
        res_proxy = proxy2.geocoder(adresse_sherbrooke)
        assert type(res_direct) is type(res_proxy)
