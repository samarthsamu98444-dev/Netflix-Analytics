import pandas as pd
import sqlite3 

customer = pd.read_csv(r"C:\Users\samar\OneDrive\Desktop\c language\.vscode\project\p1.txt")
orders = pd.read_csv(r"C:\Users\samar\OneDrive\Desktop\c language\.vscode\project\p2.txt")
payments = pd.read_csv(r"C:\Users\samar\OneDrive\Desktop\c language\.vscode\project\p3.txt")


# Cleaning
customer["name"] = customer["name"].fillna("unknown")
customer["city"] = customer["city"].fillna("unknown")
customer["city"] = customer["city"].str.strip()

orders["quantity"] = orders["quantity"].fillna(1)
orders["order_date"] = orders["order_date"].fillna("2024-01-01")
orders["product"] = orders["product"].fillna("unknown")

payments["payment_method"] = payments["payment_method"].fillna("unknown")

# Connect DB
conn = sqlite3.connect("ecommerce.db")

# Save tables
customer.to_sql("customer", conn, if_exists="replace", index=False)
orders.to_sql("orders", conn, if_exists="replace", index=False)
payments.to_sql("payments", conn, if_exists="replace", index=False)

print("All tables created successfully")

import matplotlib.pyplot as plt

query = """
SELECT SUM(price*quantity) AS total_revenue
FROM orders
"""

df = pd.read_sql(query,conn)

print(df)

query=""" select count(*) as total_orders
from orders"""
df=pd.read_sql(query,conn)
print (df)

query="""select avg(price*quantity) as avg_value
from orders """
df=pd.read_sql(query,conn)
print(df)


query="""select category, sum(price*quantity) as revenue
from orders
group by category"""
df=pd.read_sql(query,conn)
plt.bar(df["category"],df["revenue"])
plt.xlabel("category")
plt.ylabel("revenue")
plt.title("category vs revenue bar ")
plt.show()


query ="""select strftime('%m', order_date) as month, sum(price*quantity) as revenue
from orders
group by month"""
df=pd.read_sql(query,conn)
plt.plot(df["month"],df["revenue"])
plt.xlabel("month")
plt.ylabel("revenue")
plt.title("monthly revenue")
plt.show()


query="""select payment_method,count(*) as total
from payments
group  by payment_method""" 
df=pd.read_sql(query,conn)
plt.pie(df["total"],labels=df["payment_method"],autopct='%1.1f%%')
plt.show()

query="""select c.name, sum(o.price*o.quantity)as revenue
from orders o join customer c on c.customer_id=o.customer_id
group by c.name
order by sum(o.price*o.quantity) desc

limit 5"""

df=pd.read_sql(query,conn)
print(df) 

##in the second month the revenue as increased 
##and the elecrtonics category has earned more revenue
##UPI and Credit Card dominated payments
