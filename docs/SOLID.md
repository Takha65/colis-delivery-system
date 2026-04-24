# Principes SOLID appliques

## S - Single Responsibility Principle ✅
- Chaque use case = 1 responsabilite
- Chaque etat (State) = 1 role
- Chaque factory = 1 type de colis
- Adapter = traduction, Proxy = cache (responsabilites separees)

## O - Open/Closed Principle ✅
- State Pattern : ajouter un etat = nouvelle classe, 0 modification
- Factory Method : ajouter un type = nouvelle factory
- Strategy : ajouter un algorithme = nouvelle strategie

## L - Liskov Substitution Principle ✅
- Etats substituables via ColisState
- Factories substituables via ColisFactory
- Strategies substituables via IStrategieRoutage
- Proxy et Adapter substituables via IGeocodingService
Tests parametres dans les fichiers test_*.py demontrent ce comportement.

## I - Interface Segregation Principle ✅
- IColisRepository separe de IGeocodingService separe de IStrategieRoutage
- Chaque client ne depend que des methodes qu'il utilise

## D - Dependency Inversion Principle ✅
- Use cases dependent d'interfaces (IColisRepository, IGeocodingService)
- Les implementations concretes (SQLAlchemy, Nominatim) sont injectees
- Fakes utilises en tests pour decouplage total
