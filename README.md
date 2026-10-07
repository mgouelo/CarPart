# CarPart

Deux APIs FastAPI conteneurisées pour l'entreprise CarPart :

- **stock-api** : gestion du stock de produits (MongoDB), port `8000`
- **clients-api** : gestion des clients (MySQL), port `8001`

Projet réalisé dans le cadre de la ressource R5.A.09.

## Où trouver le projet

| Ressource | URL |
|---|---|
| Dépôt (public) | https://github.com/mgouelo/CarPart |
| Docker Hub : stock-api (public) | https://hub.docker.com/r/matthgouelo/carpart-stock-api |
| Docker Hub : clients-api (public) | https://hub.docker.com/r/matthgouelo/carpart-clients-api |
| GHCR : stock-api | https://github.com/mgouelo/CarPart/pkgs/container/carpart-stock-api |
| GHCR : clients-api | https://github.com/mgouelo/CarPart/pkgs/container/carpart-clients-api |

> **Note :** le dépôt est hébergé sur **GitHub**.
> GitHub Actions remplace GitLab CI, et GHCR (GitHub Container Registry) remplace le GitLab Registry.

## Lancer le projet

```bash
cp .env.example .env     # adapter les valeurs si besoisn
docker compose up --build
```

- Stock API : http://localhost:8000/docs
- Clients API : http://localhost:8001/docs

Pour utiliser les images publiées plutôt que de les construire :

```bash
docker pull matthgouelo/carpart-stock-api
docker pull matthgouelo/carpart-clients-api
```

## Pipeline CI

Le workflow [.github/workflows/ci.yml](.github/workflows/ci.yml) se déclenche à chaque push sur `main` :

1. **test** : installation des dépendances, compilation et import des modules, pour chaque API.
2. **build-buildah-ghcr** : build avec Buildah, push vers GHCR (`ghcr.io/mgouelo/carpart-*`).
3. **build-docker-hub** : build avec Docker, push vers Docker Hub (`matthgouelo/carpart-*`).

Chaque image est publiée avec les tags `latest` et le SHA du commit. Les identifiants Docker Hub sont
stockés dans les secrets GitHub (`DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`).

## Endpoints

**Stock API** : `POST/GET /products`, `GET/PATCH/DELETE /products/{id}`,
`POST /products/{id}/add-stock`, `POST /products/{id}/remove-stock`

**Clients API** : `POST/GET /clients`, `GET/PATCH/DELETE /clients/{id}`, `POST /clients/{id}/orders`

Des exemples de requêtes sont dans [tests/](tests/).
