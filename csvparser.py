import pandas as pa
from dotenv import load_dotenv
import os
import psycopg2

load_dotenv()


df = pa.read_csv("hf://datasets/datastax/philosopher-quotes/philosopher-quotes.csv")

with open("data.csv", "w", encoding="utf-8") as f:
    df.to_csv(f, index=False)
def initdb():
    db = os.getenv("DB")
    conn = psycopg2.connect(db)
    ctable = "CREATE TABLE IF NOT EXISTS cit (id SERIAL PRIMARY KEY, quote TEXT, author TEXT)"
    cursor = conn.cursor()
    cursor.execute(ctable)
    conn.commit()
    conn.close()
initdb()
with open("data.csv", "r", encoding="utf-8") as f:
    while True:
        print("What do you want to find?: ", end="")
        vvod = str(input())
        if vvod == "exit":
            print("Exiting...")
            break
        if vvod == "/favorit":
            db = os.getenv("DB")
            conn = psycopg2.connect(db)
            query = "SELECT * FROM cit"
            cursor = conn.cursor()
            cursor.execute(query)
            result = cursor.fetchall()
            conn.close()
            print(f"Your favorite quotes:\n{result}")
            break
        citate = df[df.apply(lambda row: row.astype(str).str.contains(vvod, case=False).any(), axis=1)]
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
                query = "INSERT INTO cit (quote, author) VALUES (%s, %s)"
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