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

## 7. Unit of Work ✅
`backend/src/application/ports/unit_of_work.py`
Centralise la gestion transactionnelle des opérations repositories.
Permet de confirmer ou annuler un ensemble d’actions avec commit/rollback.
Garantit la cohérence des données lors de la création ou mise à jour des colis.

## 10. Observer ✅
`backend/src/application/services/event_bus.py`
Permet de publier des événements métier et de notifier plusieurs handlers.
Découple les actions principales des traitements secondaires.
Utilisé pour réagir à des événements comme la création ou le changement d’état d’un colis.

