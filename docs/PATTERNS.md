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

---

## 3. Factory Method ✅

**Emplacement** : `src/domain/factories/colis_factory.py`

Creation de colis differenciee selon leur type (Standard, Fragile, Express).
Chaque factory encapsule les regles metier specifiques a son type :
- `StandardColisFactory` : aucune contrainte supplementaire
- `FragileColisFactory` : poids <= 20 kg, volume <= 50 000 cm3
- `ExpressColisFactory` : poids <= 10 kg, dimensions <= 50 cm

### Avantages
- **OCP** : ajouter un nouveau type = nouvelle factory, 0 modification
- **SRP** : chaque factory = 1 type = 1 ensemble de regles
- Template method : `creer()` est commun, `valider_contraintes()` est specifique

---

## 4. Strategy (A venir - M2.2)
## 5. Adapter (A venir - M2.3)
## 6. Proxy (A venir - M2.3)
## 7. Unit of Work (A venir - J4)
## 8. Facade (A venir - J4)
## 9. Decorator (A venir - J4)
## 10. Observer (A venir - J4)
