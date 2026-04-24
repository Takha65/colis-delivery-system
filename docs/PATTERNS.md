# Design Patterns utilises

## 1. Repository Pattern ✅
`src/application/ports/colis_repository.py` + `src/infrastructure/persistence/`
Separation metier/persistance. Demontrer DIP.

## 2. State Pattern ✅
`src/domain/states/colis_state.py`
4 classes polymorphes pour le cycle de vie du colis.
Demontrer OCP + LSP + SRP.

## 3. Factory Method ✅
`src/domain/factories/colis_factory.py`
3 factories (Standard/Fragile/Express) avec regles metier dediees.
Demontrer OCP + SRP.

## 4. Strategy Pattern ✅
`src/infrastructure/routage/` + `src/application/ports/strategie_routage.py`
3 algorithmes interchangeables (Dijkstra, Plus proche voisin, Greedy)
avec selecteur intelligent.
Demontrer OCP + LSP.

## 5. Adapter ✅
`src/infrastructure/external/nominatim_adapter.py`
Adapte l'API HTTP Nominatim a notre interface IGeocodingService.
Le domaine ne connait rien de Nominatim.

## 6. Proxy ✅
`src/infrastructure/external/geocoding_cache_proxy.py`
Enveloppe le NominatimAdapter pour ajouter un cache in-memory,
sans changer l'interface. Respecte le rate limit Nominatim.

## 7. Unit of Work (A venir - J4)
## 8. Facade (A venir - J4)
## 9. Decorator (A venir - J4)
## 10. Observer (A venir - J4)
