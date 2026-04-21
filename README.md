
# Systeme de gestion de livraison de colis

Projet IFT785 - Approches Orientees Objets - Hiver 2026
Universite de Sherbrooke

Systeme complet de suivi et d'optimisation de livraisons de colis gerant le cycle
de vie complet (cree -> en transit -> livre -> confirme) et l'optimisation de
routes pour les livreurs.

## Modules implementes

- **M1 - Gestion des colis (Socle)** : CRUD complet, cycle de vie, historique
- **M2 - Optimisation des routes** : Plusieurs algorithmes (Dijkstra, Greedy, Plus proche voisin)
  avec selection intelligente selon criteres (distance, temps, charge)

## Stack technique

- **Backend** : Python 3.11, FastAPI, SQLAlchemy, PostgreSQL
- **Frontend** : Vue 3, TypeScript, Pinia, Tailwind CSS
- **API externe** : Nominatim (OpenStreetMap) pour geocodage
- **Tests** : pytest (couverture >= 80%)
- **Qualite** : pylint, black, radon, mypy

## Architecture

Architecture hexagonale (Ports & Adapters) avec separation stricte :
domain/         -> Logique metier pure (entites, value objects)
application/    -> Use cases et ports (interfaces)
infrastructure/ -> Implementations techniques (DB, API externes)
interfaces/     -> API REST FastAPI


Voir [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) pour le detail.

## Demarrage rapide

### Avec Docker (recommande)

```bash
git clone <url-du-repo>
cd colis-delivery-system
docker-compose up --build
```

- Backend : http://localhost:8000
- Documentation API : http://localhost:8000/docs
- Health check : http://localhost:8000/health

### Developpement local backend

```bash
cd backend
pip install poetry
poetry install
cp .env.example .env
poetry run uvicorn main:app --reload
```

### Tests

```bash
cd backend
poetry run pytest
```

## Documentation

- [PATTERNS.md](docs/PATTERNS.md) - Design patterns utilises
- [SOLID.md](docs/SOLID.md) - Principes SOLID demontres
- [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Architecture detaillee

## Auteur

Projet realise dans le cadre du cours IFT785 - Hiver 2026.
