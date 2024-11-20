#!/bin/bash

GRAFANA_URL="http://localhost:3000"
ADMIN_PASSWORD="admin"
DATASOURCE_NAME="TimescaleDB"

# Add a new TimescaleDB datasource
curl -X POST -H "Content-Type: application/json" \
     -u admin:$ADMIN_PASSWORD \
     -d '{
          "name": "'"$DATASOURCE_NAME"'",
          "type": "postgres",
          "url": "timescale:5432",
          "access": "proxy",
          "database": "locust",
          "user": "postgres",
          "password": "password",
          "isDefault": true
     }' \
     $GRAFANA_URL/api/datasources
