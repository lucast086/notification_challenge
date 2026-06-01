#!/bin/bash
set -e

echo "🚀 Iniciando configuración del entorno FastAPI PostgreSQL..."

git config --global --add safe.directory /workspace

if ! command -v psql &> /dev/null; then
  echo "📦 Instalando cliente PostgreSQL..."
  sudo apt-get update
  sudo apt-get install -y postgresql-client
else
  echo "✓ Cliente PostgreSQL ya está instalado."
fi

echo "📦 Instalando dependencias de Python con Poetry..."
poetry install
echo "✓ Dependencias de Python instaladas."

echo "⏳ Esperando a que PostgreSQL esté disponible..."
timeout=60
elapsed=0
while ! PGPASSWORD=postgres psql -h db -U postgres -c '\q' 2>/dev/null; do
  if [ $elapsed -ge $timeout ]; then
    echo "❌ Tiempo de espera agotado para PostgreSQL."
    break
  fi
  echo "PostgreSQL no disponible, esperando... ($elapsed/$timeout s)"
  sleep 2
  elapsed=$((elapsed+2))
done

if [ $elapsed -lt $timeout ]; then
  echo "✅ PostgreSQL disponible."
  PGPASSWORD=postgres psql -h db -U postgres -c "CREATE DATABASE fullstackapp;" 2>/dev/null || echo "✓ Base de datos ya existe."
fi

echo "🔍 Verificando instalaciones..."
echo "FastAPI: $(poetry run python -c 'import fastapi; print(fastapi.__version__)' 2>/dev/null || echo 'No instalado')"
echo "SQLModel: $(poetry run python -c 'import sqlmodel; print(sqlmodel.__version__)' 2>/dev/null || echo 'No instalado')"
echo "Alembic: $(poetry run alembic --version 2>/dev/null || echo 'No instalado')"

echo "✨ Entorno FastAPI configurado correctamente."
echo "🚀 Listo para desarrollar con FastAPI, PostgreSQL!"
