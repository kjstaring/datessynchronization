import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT  
from subprocess import call, run, PIPE
import os 

def create_database():
    #1. Connect to database 
    conn = psycopg2.connect("user=postgres password=1234")
    cur = conn.cursor() 
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT) 

    #2. Create database
    name_database = "bgtdatabase"
    cur.execute("SELECT datname FROM pg_database;")
    list_database = cur.fetchall()
    if (str(name_database), ) in list_database: 
        drop_database = "DROP DATABASE "+ name_database 
        cur.execute(drop_database)
        conn.commit() 
    create_database = "CREATE DATABASE "+ name_database 
    cur.execute(create_database)
    conn.commit()
    conn.close()
    
    #3. Create extensions 
    conn = psycopg2.connect("dbname=bgtdatabase user=postgres password=1234")
    cur = conn.cursor() 
    create_postgis = "CREATE EXTENSION IF NOT EXISTS POSTGIS"
    cur.execute(create_postgis)
    conn.commit()

    create_sfcgal = "CREATE EXTENSION IF NOT EXISTS POSTGIS_SFCGAL"
    cur.execute(create_sfcgal)
    conn.commit()
    
    conn.close()

#1. Create database and extensions 
create_database() 
