# Principes SOLID appliques

## S - Single Responsibility Principle ✅

**Illustration** : Chaque use case a **une seule responsabilite**.
- `CreerColisUseCase` : creation uniquement
- `ObtenirColisUseCase` : recuperation uniquement
- `ListerColisUseCase` : liste uniquement
- `SupprimerColisUseCase` : suppression uniquement

**Fichiers** : `backend/src/application/use_cases/`

---

## D - Dependency Inversion Principle ✅

**Illustration** : Les use cases dependent de l'abstraction `IColisRepository`,
pas de l'implementation concrete `SQLAlchemyColisRepository`.

```python
class CreerColisUseCase:
    def __init__(self, repository: IColisRepository) -> None:  # <-- Abstraction
        self._repository = repository
```

On peut injecter `SQLAlchemyColisRepository` en production ou `FakeColisRepository`
en test, sans modifier le use case.

**Fichiers** : tous les use cases + `application/ports/colis_repository.py`

---

## O - Open/Closed Principle (A venir)
## L - Liskov Substitution Principle (A venir)
## I - Interface Segregation Principle (A venir)
