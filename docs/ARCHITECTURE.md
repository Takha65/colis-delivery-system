# Architecture

## Vue d'ensemble

Le projet suit une **architecture hexagonale** (Ports & Adapters) pour garantir :
- La separation de la logique metier et des details techniques
- La testabilite de la logique metier
- La possibilite de remplacer les couches techniques sans impact metier

## Structure des couches

backend/src/
├── domain/             # Coeur : logique metier pure
│   ├── entities/       # Colis, Route, Livreur, Graphe
│   ├── value_objects/  # Adresse, Coordonnees, Poids
│   └── exceptions/     # Exceptions metier
│
├── application/        # Orchestration : use cases et contrats
│   ├── use_cases/      # Un cas d'utilisation = une classe
│   ├── ports/          # Interfaces (IColisRepository, etc.)
│   └── services/       # Services applicatifs
│
├── infrastructure/     # Details techniques : adapters
│   ├── persistence/    # SQLAlchemy, repositories concrets
│   └── external/       # Nominatim, APIs tierces
│
├── interfaces/         # Points d'entree externes
│   └── api/            # Routes FastAPI, schemas Pydantic
│
└── shared/             # Transversal (config, DI container)

## Regle de dependance

Les dependances vont **toujours** de l'exterieur vers l'interieur :

interfaces -> application -> domain
infrastructure -> application -> domain

Le domaine ne depend de rien. L'application ne depend que du domaine.
