curl -X 'POST' \
  'http://127.0.0.1:8000/pessoas' \
  -H 'Content-Type: application/json' \
  -d '{
    "apelido" : "Arthur",
    "nome" : "Rosso",
    "nascimento" : "2000-11-06",
    "stack" : ["Python", "FastAPI", "PostgreSQL"]
}'
