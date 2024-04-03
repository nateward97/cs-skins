import requests
import mysql.connector

# Fetch data from API
api_url = "https://api.steamapihub.com/market-places/all"
api_key = "lrt8tPNhX8znmOdpTAh7Uihu5gePg8Mv"
app_id = "730"
params = {"apiKey": api_key, "appId": app_id}

response = requests.get(api_url, params=params)
data = response.json()

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host='localhost',
    user='aigumniz_andy',
    password='%RS}&.3gr[gH',
    database='aigumniz_pricedata'
)
cursor = db_connection.cursor()

for product_name, product_data in data.items():
    # Insert product into Products table
    sql = "INSERT INTO products (product_name) VALUES (%s)"
    cursor.execute(sql, (product_name,))
    product_id = cursor.lastrowid

    for source, order_data in product_data.items():
        for order_type, order_details in order_data.items():
            # Insert order into Sell Orders or Buy Orders table
            if order_type in ['sellOrder', 'buyOrder']:
                price = order_details.get('original').get('price')
                currency = order_details.get('original').get('currency')
                count = order_details.get('count')
                updated_at = order_details.get('updatedAt')

                if order_type == 'sellOrder':
                    table_name = 'sell_orders'
                else:
                    table_name = 'buy_orders'

                sql = f"INSERT INTO {table_name} (product_id, source, price, currency, count, updated_at) VALUES (%s, %s, %s, %s, %s, %s)"
                values = (product_id, source, price, currency, count, updated_at)
                cursor.execute(sql, values)

# Commit changes and close connections
db_connection.commit()
cursor.close()
db_connection.close()
