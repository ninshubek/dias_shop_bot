from db import conn, cursor

def create_table_product():
    query = """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name VARCHAR,
            description TEXT,
            price INT,
            photo VARCHAR,
            color VARCHAR,
            brand VARCHAR,
            call_back VARCHAR);"""
    cursor.execute(query=query)
    conn.commit()

    
def insert_product(name: str, 
                   description: str, 
                   price: int, 
                   photo: str, 
                   color: str, 
                   brand:str, 
                   call_back:str):
    query = f"""
        INSERT INTO products (
            name, description, price, photo, color
        )VALUES (
            '{name}', '{description}', {price}, '{photo}', '{color}', '{brand}','{call_back}'
        );"""
    cursor.execute(query=query)
    conn.commit()