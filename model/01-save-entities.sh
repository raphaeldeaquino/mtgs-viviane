echo "Salvando building:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @building.json

echo -e "\n\nSalvando rooms:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @room.json

echo -e "\n\nSalvando aplicação:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @temperature-control-app.json

echo -e "\n\nSalvando fluxo de informação:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @info-flow-01.json

echo -e "\n\nSalvando primeiro fluxo de infraestrutura:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @ifr-flow-01.json

echo -e "\n\nSalvando segundo fluxo de infraestrutura:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @ifr-flow-02.json