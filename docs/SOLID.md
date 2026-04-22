# Principes SOLID appliques

## S - Single Responsibility Principle ✅

Chaque use case a **une seule responsabilite** :
- `CreerColisUseCase`, `ObtenirColisUseCase`, `ListerColisUseCase`,
  `SupprimerColisUseCase`, `TransiterColisUseCase`, `ObtenirHistoriqueUseCase`

Chaque **etat** (State Pattern) a **une seule responsabilite** : representer
son comportement (transitions, modifiabilite, etc.).

**Fichiers** : `src/application/use_cases/`, `src/domain/states/`

---

## O - Open/Closed Principle ✅

Le **State Pattern** permet d'ajouter de nouveaux etats sans modifier le code
existant. Il suffit de :
1. Creer une nouvelle classe heritant de `ColisState`
2. L'ajouter au registre `_ETATS`

Aucune autre ligne de code n'a besoin d'etre modifiee.

**Fichiers** : `src/domain/states/colis_state.py`

---

## L - Liskov Substitution Principle ✅

Les 4 classes d'etat (`ColisCree`, `ColisEnTransit`, `ColisLivre`,
`ColisConfirme`) sont **substituables** via `ColisState`. L'entite `Colis`
manipule uniquement `ColisState`, sans connaitre le type concret.

**Test de verification** : `tests/unit/domain/test_states.py` utilise
`@pytest.mark.parametrize` pour faire tourner les memes tests sur tous les
etats.

**Fichiers** : `src/domain/states/colis_state.py`, `src/domain/entities/colis.py`

---

## I - Interface Segregation Principle (A venir)

---

## D - Dependency Inversion Principle ✅

Les use cases dependent de l'abstraction `IColisRepository`, pas de
l'implementation concrete `SQLAlchemyColisRepository`.

```python
class CreerColisUseCase:
    def __init__(self, repository: IColisRepository) -> None:
        self._repository = repository
```

**Fichiers** : `src/application/use_cases/`, `src/application/ports/colis_repository.py`
