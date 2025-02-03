# docker start
```sh
cd docker
sudo docker compose -f docker-compose.middleware.yaml --profile weaviate -p dify up
```

# background
```sh
poetry run python -m celery -A app.celery worker -P gevent -c 1 --loglevel INFO -Q dataset,generation,mail,ops_trace,app_deletion
```
#  

# run web server
```sh
cd web
npm run dev
```

# run llama cpp server
```sh
cd web
npm run dev
```

# run llama cpp server
cd llm
and follow the readme.md