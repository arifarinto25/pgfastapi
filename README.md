# fastapi-basic-structure-postgre
## Installation

Using pipenv

```bash
pipenv shell
pipenv install -r ./requirements.txt
```

## Connecting to PostgreSQL

create .env file inside /app and insert

```bash
DATABASE_URL='<your-postgre-url>'
```
## Run FastAPI server

```bash
uvicorn app.main:app --reload
```


## Access Swagger Documentation
```bash
http://127.0.0.1:8000/docs
http://127.0.0.1:8000/redoc
```
## Sample Swagger Doc
![Swagger](https://i.imgur.com/5nTIlYY.png)


## SUKSES PG ASYNC SIMPLE