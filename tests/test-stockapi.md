# Tests CRUD — Stock API (MongoDB)

API accessible sur `http://localhost:8000`. Tests exécutés sur la stack lancée via `docker compose up -d`.

## Test ajouter un produit

> curl -s -X POST http://localhost:8000/products -H "Content-Type: application/json" -d '{"name":"Plaquette de frein","description":"Jeu de plaquettes avant","quantity":10}'

Output :
```json
{"id":"6ab3977135e5b34653bd9f80","name":"Plaquette de frein","description":"Jeu de plaquettes avant","quantity":10}
```
----------------------------

## Test lister les produits

> curl -s http://localhost:8000/products

Output :
```json
[{"id":"6ab3977135e5b34653bd9f80","name":"Plaquette de frein","description":"Jeu de plaquettes avant","quantity":10}]
```
----------------------------

## Test accéder à une fiche produit

> curl -s http://localhost:8000/products/6ab3977135e5b34653bd9f80

Output :
```json
{"id":"6ab3977135e5b34653bd9f80","name":"Plaquette de frein","description":"Jeu de plaquettes avant","quantity":10}
```
----------------------------

## Test modifier la description d'un produit

> curl -s -X PATCH http://localhost:8000/products/6ab3977135e5b34653bd9f80 -H "Content-Type: application/json" -d '{"description":"Jeu de plaquettes avant, references renforcees"}'

Output :
```json
{"id":"6ab3977135e5b34653bd9f80","name":"Plaquette de frein","description":"Jeu de plaquettes avant, references renforcees","quantity":10}
```
----------------------------

## Test ajouter du stock (+5)

> curl -s -X POST http://localhost:8000/products/6ab3977135e5b34653bd9f80/add-stock -H "Content-Type: application/json" -d '{"quantity":5}'

Output :
```json
{"id":"6ab3977135e5b34653bd9f80","name":"Plaquette de frein","description":"Jeu de plaquettes avant, references renforcees","quantity":15}
```
----------------------------

## Test retirer du stock (-3)

> curl -s -X POST http://localhost:8000/products/6ab3977135e5b34653bd9f80/remove-stock -H "Content-Type: application/json" -d '{"quantity":3}'

Output :
```json
{"id":"6ab3977135e5b34653bd9f80","name":"Plaquette de frein","description":"Jeu de plaquettes avant, references renforcees","quantity":12}
```
----------------------------

## Test accéder à un produit inexistant (404 attendu)

> curl -s -w "\nHTTP %{http_code}\n" http://localhost:8000/products/000000000000000000000000

Output :
```json
{"detail":"Product not found"}
HTTP 404
```
----------------------------

## Test supprimer un produit

> curl -s -o /dev/null -w "HTTP %{http_code}\n" -X DELETE http://localhost:8000/products/6ab3977135e5b34653bd9f80

Output :
```
HTTP 204
```
----------------------------

## Test vérifier la suppression (404 attendu)

> curl -s -w "\nHTTP %{http_code}\n" http://localhost:8000/products/6ab3977135e5b34653bd9f80

Output :
```json
{"detail":"Product not found"}
HTTP 404
```
----------------------------
