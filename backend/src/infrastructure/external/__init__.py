"""Services externes (APIs tierces)."""
from src.infrastructure.external.geocoding_cache_proxy import GeocodingCacheProxy
from src.infrastructure.external.nominatim_adapter import NominatimGeocodingAdapter

__all__ = ["GeocodingCacheProxy", "NominatimGeocodingAdapter"]
