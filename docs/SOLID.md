# Principes SOLID appliques

## S - Single Responsibility Principle ✅

Chaque use case a **une seule responsabilite** (CreerColisUseCase, etc.).
Chaque **etat** (State Pattern) a une seule responsabilite.
Chaque **factory** (Factory Method) encapsule les regles d'un seul type.

**Fichiers** : `src/application/use_cases/`, `src/domain/states/`, `src/domain/factories/`

---

## O - Open/Closed Principle ✅

Demontre par deux patterns :
1. **State Pattern** : ajouter un etat = nouvelle classe, 0 modification.
2. **Factory Method** : ajouter un type de colis = nouvelle factory, 0 modification.

**Fichiers** : `src/domain/states/colis_state.py`, `src/domain/factories/colis_factory.py`

---

## L - Liskov Substitution Principle ✅

Les 4 classes d'etat et les 3 factories sont **substituables** via leurs
classes abstraites (`ColisState`, `ColisFactory`). Les tests utilisent
`@pytest.mark.parametrize` pour valider ce comportement uniforme.

**Fichiers** : `src/domain/states/`, `src/domain/factories/`

---

## I - Interface Segregation Principle (A venir en M2.3)

---

## D - Dependency Inversion Principle ✅

Les use cases dependent de l'abstraction `IColisRepository`, pas de
l'implementation concrete `SQLAlchemyColisRepository`.

**Fichiers** : `src/application/use_cases/`, `src/application/ports/`
