import pandas as pa
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()

#downloading data from huggingface platform
df = pa.read_csv("hf://datasets/datastax/philosopher-quotes/philosopher-quotes.csv")

#moving data to file data.csv
with open("data.csv", "w", encoding="utf-8") as f: #create and opening the file
    df.to_csv(f, index=False) #write in


#database initialisation
def initdb():
    db = os.getenv("DB") #get postgresql url from env file
    conn = psycopg2.connect(db) #open connection
    ctable = "CREATE TABLE IF NOT EXISTS cit (id SERIAL PRIMARY KEY, quote TEXT, author TEXT)" #for creating table if not exists
    cursor = conn.cursor() #create database writer
    cursor.execute(ctable) #create table
    conn.commit() #update database
    conn.close() #close connection
initdb() #call the function

#our programm
with open("data.csv", "r", encoding="utf-8") as f:  #open data.csv for reading
    while True: #loop
        print("What do you want to find?: ", end="")
        vvod = str(input()) #search input and command line
        if vvod == "exit": #if commandf exit
            print("Exiting...")
            break #break from loop
        if vvod == "/favorit": #if command /favorit
            db = os.getenv("DB") #geting db url from env
            conn = psycopg2.connect(db)#database connection
            query = "SELECT * FROM cit"#command for getting all from table cit
            cursor = conn.cursor() #create cursor writer
            cursor.execute(query)
            result = cursor.fetchall()#save all into result (RAM)
            conn.close() #close connection
            print(f"Your favorite quotes:\n{result}")
            break
        citate = df[df.apply(lambda row: row.astype(str).str.contains(vvod, case=False).any(), axis=1)] #if normal search writting that found
        if citate.empty:
            print("No results found")
            continue
        print(citate)
        print("Do you like to save the result in database? (1/0): ", end="")
        save = str(input())
        if save == "1":
            db = os.getenv("DB")
            conn = psycopg2.connect(db)
            for index, row in citate.iterrows():
                query = "INSERT INTO cit (quote, author) VALUES (%s, %s)"#save in favorite database
                cursor = conn.cursor()
                cursor.execute(query, (row["quote"], row["author"]))
            conn.commit()
            conn.close()
            print("Result saved in database")
            print("Do you want to continue? (1/0): ", end="")
            cont = str(input())
            if cont == "0":
                break
            else:
                continue
        else:
            print("Result not saved")
            break
        if len(citate) == 0:
            print("No results found")
            break
        if vvod == "":
            print("No input provided")
            break