## Docker

- local containerization
```zsh
docker build -t webmasterdevlin/fastapi:<version> .
```

- local deployment
```zsh
docker run -p 8000:80 webmasterdevlin/fastapi:<version> 
```