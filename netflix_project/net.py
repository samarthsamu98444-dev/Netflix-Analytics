import pandas as pd 
import sqlite3
 #lode dataset 
netflix = pd.read_csv(r"C:\Users\samar\OneDrive\Desktop\c language\.vscode\project\netflix_project\netflix.txt")
  # Cleaning 
netflix["country"] = netflix["country"].fillna("unknown") 
# Connect DB 
conn = sqlite3.connect("netflix.db") 
# Save tables 
netflix.to_sql("netflix", conn, if_exists="replace", index=False)


print("All tables created successfully")

print(netflix.head())
print(netflix.info())

import matplotlib.pyplot as plt
query="""select type,count(*)as total 
from netflix 
group by type"""
df=pd.read_sql(query,conn) 
plt.pie(df["total"],labels=df["type"],autopct='%1.1f%%')
plt.show() 

query="""select genre,count(*)as total from netflix group by genre order by total desc""" 
df=pd.read_sql(query,conn)
plt.bar(df["genre"],df["total"])
plt.xlabel("genre")
plt.ylabel("total") 
plt.title(" genre wise plots ")
plt.show() 

query=""" select country,count(*)as total from netflix group by country order by total desc""" 
df=pd.read_sql(query,conn)
plt.bar(df["country"],df["total"])
plt.xlabel("country") 
plt.ylabel("total")
plt.title("the countey wise plot") 
plt.show()

query="""select release_year,count(*) as total 
from netflix
group by release_year
order by total """
df=pd.read_sql(query,conn)
plt.plot(df["release_year"],df["total"])
plt.xlabel("release") 
plt.ylabel("total")
plt.title("content growth by year") 
plt.show() 

query="""select rating ,count(*) as total from netflix group by rating"""
df=pd.read_sql(query,conn) 
plt.pie(df["total"],labels=df["rating"],autopct='%1.1f%%') 
plt.show() 

query=""" 
select*,sum(tot_title)over(order by release_year) as t 
from ( select release_year,
count(*)as tot_title 
from netflix 
group by release_year )r;"""
df=pd.read_sql(query,conn)
plt.plot(df["release_year"],df["t"])
plt.xlabel("release-year") 
plt.ylabel("total")
plt.title(" content growth") 
plt.show() 
conn.close(), 