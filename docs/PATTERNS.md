# Design Patterns utilises

## 1. Repository Pattern ✅

**Emplacement** : `src/application/ports/colis_repository.py` + `src/infrastructure/persistence/sqlalchemy_colis_repository.py`

Separation entre la logique metier et l'acces aux donnees. Les use cases
dependent de l'interface `IColisRepository`, avec deux implementations :
- `SQLAlchemyColisRepository` (prod)
- `FakeColisRepository` (tests)

Demontrer **DIP**.

---

## 2. State Pattern ✅

**Emplacement** : `src/domain/states/colis_state.py`

Le cycle de vie d'un colis (CREE -> EN_TRANSIT -> LIVRE -> CONFIRME) est
represente par 4 classes polymorphes heritant de `ColisState`. Chaque etat
sait :
- son nom
- quelles transitions il autorise
- s'il est final
- si le colis est encore modifiable

### Avantages
- **OCP** : ajouter un etat = creer une classe, aucune modification
- **LSP** : tous les etats substituables via `ColisState`
- **SRP** : chaque classe = 1 etat = 1 responsabilite

### Avant / Apres
Avant : dict `TRANSITIONS_VALIDES` + `if/else` implicite.
Apres : polymorphisme, chaque etat encapsule sa logique.

---

## 3. Factory Method (A venir - M1.5)
## 4. Strategy (A venir - M2)
## 5. Adapter (A venir - M2)
## 6. Proxy (A venir - M2)
## 7. Facade (A venir - J4)
## 8. Decorator (A venir - J4)
## 9. Unit of Work (A venir - J4)
## 10. Observer (A venir - J4)
