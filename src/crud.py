from database import get_connection

def get_top_products(limit=10):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT product_name, COUNT(*) as mention_count
        FROM analytics.fct_messages
        JOIN analytics.dim_products USING(product_id) -- hypothetical join
        GROUP BY product_name
        ORDER BY mention_count DESC
        LIMIT %s;
    """
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def get_channel_activity(channel_name):
    conn = get_connection()
    cursor = conn.cursor()
    query = """
        SELECT date, COUNT(*) as message_count
        FROM analytics.fct_messages
        JOIN analytics.dim_channels USING(channel_id)
        WHERE channel_name = %s
        GROUP BY date
        ORDER BY date;
    """
    cursor.execute(query, (channel_name,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

def search_messages(query):
    conn = get_connection()
    cursor = conn.cursor()
    sql = """
        SELECT message_id, channel_name, message_text, message_date
        FROM analytics.fct_messages
        JOIN analytics.dim_channels USING(channel_id)
        WHERE message_text ILIKE %s
        ORDER BY message_date DESC
        LIMIT 50;
    """
    cursor.execute(sql, (f'%{query}%',))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
