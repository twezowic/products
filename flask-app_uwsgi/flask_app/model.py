import sqlite3

database = "database.db"


class Schema:
    def __init__(self):
        self.conn = sqlite3.connect(database)
        self.create_product_table()

    def create_product_table(self):

        query = """
        CREATE TABLE IF NOT EXISTS "Product" (
          id INTEGER PRIMARY KEY,
          NAME TEXT,
          DESCRIPTION TEXT,
          QUANTITY NUMERIC,
          PRICE REAL,
          _date_added DATE DEFAULT CURRENT_DATE
        );
        """

        self.conn.execute(query)


class ProductModel:
    TABLENAME = "PRODUCT"

    def __init__(self):
        self.conn = sqlite3.connect(database)
        self.conn.row_factory = sqlite3.Row

    def create(self, name, description, quantity, price):
        query = f"""insert into {self.TABLENAME}
                (Name, Description, Quantity, Price)
                values (?, ?, ?, ?)"""

        result = self.conn.execute(query, [name, description, quantity, price])
        self.conn.commit()
        self.conn.close()
        return result.lastrowid

    def read(self):
        query = """select name, description, quantity, price from product"""

        cursor = self.conn.execute(query)
        result = [dict(row) for row in cursor.fetchall()]
        self.conn.close()
        return result
