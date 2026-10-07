# Tests CRUD — Clients API (MySQL)

API accessible sur `http://localhost:8001`. Tests exécutés sur la stack lancée via `docker compose up -d`.

## Test ajouter un client

> curl -s -X POST http://localhost:8001/clients -H "Content-Type: application/json" -d '{"first_name":"Matthieu","last_name":"Gouélo","email":"matthieugouelo@gmail.com"}'

Output :
```json
{"id":2,"first_name":"Matthieu","last_name":"Gouélo","email":"matthieugouelo@gmail.com","order_count":0}
```
----------------------------

## Test lister les clients

> curl -s http://localhost:8001/clients

Output :
```json
[{"id":2,"first_name":"Matthieu","last_name":"Gouélo","email":"matthieugouelo@gmail.com","order_count":0}]
```
----------------------------

## Test accéder à une fiche client

> curl -s http://localhost:8001/clients/2

Output :
```json
{"id":2,"first_name":"Matthieu","last_name":"Gouélo","email":"matthieugouelo@example.com","order_count":0}
```
----------------------------

## Test modifier une fiche client (nom, prénom, email)

> curl -s -X PATCH http://localhost:8001/clients/2 -H "Content-Type: application/json" -d '{"first_name":"Matthieu","last_name":"Le lain","email":"matthieulelain@gmail.com"}'

Output :
```json
{"id":2,"first_name":"Matthieu","last_name":"Le lain","email":"matthieulelain@gmail.com","order_count":0}
```
----------------------------

## Test mettre à jour le nombre de commandes (+4)

> curl -s -X POST http://localhost:8001/clients/2/orders -H "Content-Type: application/json" -d '{"quantity":4}'

Output :
```json
{"id":2,"first_name":"Matthieu","last_name":"Le lain","email":"matthieulelain@gmail.com","order_count":4}
```
----------------------------

## Test accéder à un client inexistant (404 attendu)

> curl -s -w "\nHTTP %{http_code}\n" http://localhost:8001/clients/999

Output :
```json
{"detail":"Client not found"}
HTTP 404
```
----------------------------

## Test supprimer un client

> curl -s -o /dev/null -w "HTTP %{http_code}\n" -X DELETE http://localhost:8001/clients/2

Output :
```
HTTP 204
```
----------------------------

## Test vérifier la suppression (404 attendu)

> curl -s -w "\nHTTP %{http_code}\n" http://localhost:8001/clients/2

Output :
```json
{"detail":"Client not found"}
HTTP 404
```
----------------------------
