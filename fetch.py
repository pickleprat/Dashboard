import psycopg2 as psy 
import os 
import pandas as pd 

connection = psy.connect(
    database=os.environ["DB_NAME"], 
    user=os.environ["DB_USER"], 
    host=os.environ["DB_HOST"], 
    port=os.environ["DB_PORT"], 
    password=os.environ["DB_PASSWORD"], 
)

cursor = connection.cursor()
cursor.execute(
    "SELECT * FROM public.home_denormalized; "
)
data = cursor.fetchall()
descriptors = [desc[0] for desc in cursor.description]
df = pd.DataFrame(data, columns=descriptors)
df.to_csv("data/denormalized.csv", index=False)