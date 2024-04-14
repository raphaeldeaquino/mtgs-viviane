echo "Salvando building:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @volga.json

echo -e "\n\nSalvando rooms:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @room-01.json
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @room-02.json
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @room-03.json

echo -e "\n\nSalvando aplicações:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @temperature-control-app.json
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @energy-monitoring-app.json

echo -e "\n\nSalvando fluxos de informação:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @info-flow-01.json
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @info-flow-02.json

echo -e "\n\nSalvando fluxos de infraestrutura:"
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @ifr-flow-01.json
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @ifr-flow-02.json
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @ifr-flow-03.json
curl -X POST http://localhost:8000/entities \
   -H "Content-Type: application/json" \
   --data @ifr-flow-04.json