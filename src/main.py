from pathlib import Path
import sqlite3, pandas as pd
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True); db=OUT/'ecommerce.db'
if db.exists(): db.unlink()
con=sqlite3.connect(db)
for name in ['customers','products','orders','order_items','payments']:
    pd.read_csv(ROOT/f'data/{name}.csv').to_sql(name,con,index=False,if_exists='replace')
queries={
'monthly_revenue':"SELECT substr(o.order_date,1,7) month, ROUND(SUM(oi.quantity*oi.unit_price),2) revenue FROM orders o JOIN order_items oi USING(order_id) WHERE o.status='Completed' GROUP BY month ORDER BY month",
'top_customers':"SELECT c.customer_id,c.customer_name,ROUND(SUM(oi.quantity*oi.unit_price),2) lifetime_value FROM customers c JOIN orders o USING(customer_id) JOIN order_items oi USING(order_id) WHERE o.status='Completed' GROUP BY c.customer_id,c.customer_name ORDER BY lifetime_value DESC LIMIT 20",
'category_performance':"SELECT p.category,ROUND(SUM(oi.quantity*oi.unit_price),2) revenue,SUM(oi.quantity) units FROM products p JOIN order_items oi USING(product_id) JOIN orders o USING(order_id) WHERE o.status='Completed' GROUP BY p.category ORDER BY revenue DESC",
'country_performance':"SELECT c.country,COUNT(DISTINCT o.order_id) orders,ROUND(SUM(oi.quantity*oi.unit_price),2) revenue FROM customers c JOIN orders o USING(customer_id) JOIN order_items oi USING(order_id) WHERE o.status='Completed' GROUP BY c.country ORDER BY revenue DESC",
'repeat_customers':"WITH x AS (SELECT customer_id,COUNT(*) completed_orders FROM orders WHERE status='Completed' GROUP BY customer_id) SELECT * FROM x WHERE completed_orders>=3 ORDER BY completed_orders DESC",
'product_rank_by_category':"WITH r AS (SELECT p.category,p.product_name,SUM(oi.quantity*oi.unit_price) revenue FROM products p JOIN order_items oi USING(product_id) JOIN orders o USING(order_id) WHERE o.status='Completed' GROUP BY p.category,p.product_name) SELECT category,product_name,ROUND(revenue,2) revenue,DENSE_RANK() OVER(PARTITION BY category ORDER BY revenue DESC) category_rank FROM r ORDER BY category,category_rank"
}
for name,q in queries.items(): pd.read_sql_query(q,con).to_csv(OUT/f'{name}.csv',index=False)
print(pd.read_sql_query(queries['category_performance'],con).to_string(index=False)); con.close(); print('SQLite database:',db)
