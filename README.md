# Latam Price Checker
This is a simple app using **Python/Fastapi** for the backend to deliver all price combinations when searching for an airline ticket.

It searches for 21 days from the start date and compiles all the prices into a table.

![This is an image](./screenshot.png)

Backend:
- Python using FastApi

### Instalation using VirtualEnv:
- Download the git repo
- create Virtual Environment and activate it
- Install requirements.txt `pip install -r requirements.txt`
- Load the server `uvicorn main:app --reload`
- Open http://127.0.0.1:8000  in your browser


### Instalation using Docker:
- Download the git repo
- Docker build -t latam .
- Docker run --rm  -p 8000:8000/tcp latam:latest
- Open http://127.0.0.1:8000  in your browser

