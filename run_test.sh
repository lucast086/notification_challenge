docker compose -f docker-compose-test.yml up --build --exit-code-from app

if [ $? -eq 0 ]; then
  echo "Tests passed"
else
  echo "Tests failed"
fi
