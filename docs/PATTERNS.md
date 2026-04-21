# Design Patterns utilises

## 1. Repository Pattern ✅ (Implemente)

**Categorie** : Architectural
**Emplacement** : `backend/src/application/ports/colis_repository.py` + `backend/src/infrastructure/persistence/sqlalchemy_colis_repository.py`

### Probleme resolu
Separer la logique metier de l'acces aux donnees. Les use cases ne doivent pas
savoir si les colis sont stockes en PostgreSQL, MongoDB, ou en memoire.

### Implementation
- **Interface** (port) : `IColisRepository` declare les operations (save, get_by_id, find_all, delete)
- **Implementations** :
  - `SQLAlchemyColisRepository` : production (PostgreSQL)
  - `FakeColisRepository` (dans tests/) : tests unitaires rapides

### Justification
Demontrer le **DIP** (Dependency Inversion Principle) : les use cases dependent
de `IColisRepository`, pas de SQLAlchemy. Changer de techno = remplacer
l'implementation sans toucher au metier.

---

## 2. Factory Method (A venir - M1.5)
## 3. State (A venir - M1.4)
## 4. Strategy (A venir - M2)
## 5. Adapter (A venir - M2)
## 6. Proxy (A venir - M2)
## 7. Facade (A venir - J4)
## 8. Decorator (A venir - J4)
## 9. Unit of Work (A venir - J4)
## 10. Observer (A venir - J4)
