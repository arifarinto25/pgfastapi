import os

 #pipenv install environ python-dotenv
 # LOAD .env
from environs import Env
env = Env()
env.read_env() 

from fastapi import FastAPI

#import database settings
from db import database, engine, metadata

#import routes here
from routes import route_user


app = FastAPI(    
		title="User API",
    	description="User API Documentation",
    	version="1.0.0",)

#create databases.
metadata.create_all(engine)


# connect to database on startup
@app.on_event("startup")
async def startup():
    await database.connect()

#disconnect database on shutdown
@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


#Register routes here.
app.include_router(route_user.router, prefix = "/user", tags = ['user'])
