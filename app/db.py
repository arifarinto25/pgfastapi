import os
from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,create_engine)
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from databases import Database


DATABASE_URL=os.getenv("DATABASE_URL")

# SQLAlchemy
engine = create_engine(DATABASE_URL)
metadata = MetaData()


# create tbl_users table
tbl_users = Table(
	'tbl_users',
	metadata,
	   Column('id', Integer, unique=True, primary_key = True), 
	   Column('user_name', String, unique=True), 
	   Column('first_name', String),
	   Column('last_name', String)
)

# databases query builder
database = Database(DATABASE_URL)
