curl -X 'POST' \
  'http://127.0.0.1:8000/pessoas' \
  -H 'Content-Type: application/json' \
  -d '{
    "apelido" : "icaro",
    "nome" : "Rosa Roberto",
    "nascimento" : "2000-10-01",
    "stack" : ["C#", "Node", "Oracle"]
}'
