import sqlite3
import threading


class DatabaseConnection:
    def __init__(self, connection_id):
        self.connection_id = connection_id
        self.connection = sqlite3.connect(":memory:")
        self.create_tables()
        self.insert_data()

    def create_tables(self):
        create_users_table = """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """
        create_orders_table = """
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        create_products_table = """
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                price REAL NOT NULL
            )
        """
        create_customers_table = """
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT NOT NULL
            )
        """
        cursor = self.connection.cursor()
        cursor.execute(create_users_table)
        cursor.execute(create_orders_table)
        cursor.execute(create_products_table)
        cursor.execute(create_customers_table)
        self.connection.commit()

    def insert_data(self):
        insert_users_data = """
            INSERT INTO users (username, email) VALUES
            ('user1', 'user1@example.com'),
            ('user2', 'user2@example.com'),
            ('user3', 'user3@example.com')
        """
        insert_orders_data = """
            INSERT INTO orders (user_id, total_amount) VALUES
            (1, 100.0),
            (2, 150.0),
            (3, 200.0)
        """
        insert_products_data = """
            INSERT INTO products (name, price) VALUES
            ('product1', 10.0),
            ('product2', 20.0),
            ('product3', 30.0)
        """
        insert_customers_data = """
            INSERT INTO customers (name, email) VALUES
            ('customer1', 'customer1@example.com'),
            ('customer2', 'customer2@example.com'),
            ('customer3', 'customer3@example.com')
        """
        cursor = self.connection.cursor()
        cursor.execute(insert_users_data)
        cursor.execute(insert_orders_data)
        cursor.execute(insert_products_data)
        cursor.execute(insert_customers_data)
        self.connection.commit()

    def execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result


class DatabaseConnectionPool:
    _lock = threading.Lock()

    def __init__(self, pool_size):
        self.pool_size = pool_size
        self.available_connections = [DatabaseConnection(i) for i in range(pool_size)]
        self.in_use_connections = []

    def acquire_connection(self):
        with self._lock:
            if not self.available_connections:
                print("No available connections. Creating a new one.")
                new_connection = DatabaseConnection(len(self.in_use_connections) + len(self.available_connections))
            else:
                new_connection = self.available_connections.pop()
            self.in_use_connections.append(new_connection)
            return new_connection

    def release_connection(self, connection):
        with self._lock:
            self.in_use_connections.remove(connection)
            self.available_connections.append(connection)


if __name__ == "__main__":
    connection_pool = DatabaseConnectionPool(pool_size=3)

    conn1 = connection_pool.acquire_connection()
    conn2 = connection_pool.acquire_connection()
    conn3 = connection_pool.acquire_connection()

    query_result1 = conn1.execute_query("SELECT * FROM users")
    query_result2 = conn2.execute_query("SELECT * FROM orders")
    query_result3 = conn3.execute_query("SELECT * FROM products")

    print("Query Result 1:", query_result1)
    print("Query Result 2:", query_result2)
    print("Query Result 3:", query_result3)

    connection_pool.release_connection(conn1)
    connection_pool.release_connection(conn2)
    connection_pool.release_connection(conn3)

    conn4 = connection_pool.acquire_connection()
    query_result4 = conn4.execute_query("SELECT * FROM customers")
    print("Query Result 4:", query_result4)
