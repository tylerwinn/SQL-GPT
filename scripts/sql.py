import random
from datetime import datetime, timedelta
from faker import Faker

# Function to create and populate the 'employees' table in the given database connection.
def create_employees_table(connection):
    # Creating a cursor to execute SQL statements.
    cursor = connection.cursor()
    
    # SQL query to create the 'employees' table.
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            birthday DATE,
            salary DECIMAL(10, 2),
            position VARCHAR(100)
        )'''
    
    # Executing the SQL query to create the 'employees' table.
    cursor.execute(create_table_query)
    
    # SQL query to insert test data into the 'employees' table.
    insert_query = '''
        INSERT INTO employees (first_name, last_name, birthday, salary, position)
        VALUES (%s, %s, %s, %s, %s)'''
    
    # Test data for populating the 'employees' table.
    first_names = ['John', 'Jane', 'Bob', 'Alice', 'Charlie']
    last_names = ['Doe', 'Smith', 'Johnson', 'Brown', 'Williams']
    positions = ['Software Engineer', 'Data Scientist', 'Manager', 'Analyst', 'Technician']
    
    # Generating test data.
    test_data = []
    for _ in range(50):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        birthday = datetime.strptime('1/1/1960', '%m/%d/%Y') + timedelta(days=random.randint(0, 20000))
        salary = round(random.uniform(40000, 100000), 2)
        position = random.choice(positions)
        test_data.append((first_name, last_name, birthday.date(), salary, position))
    
    # Inserting test data into the 'employees' table.
    cursor.executemany(insert_query, test_data)
    
    # Closing the cursor.
    cursor.close()

# Function to create and populate the 'invoices' table in the given database connection.
def create_invoices_table(connection):
    # Creating a cursor to execute SQL statements.
    cursor = connection.cursor()
    
    # SQL query to create the 'invoices' table.
    create_table_query = '''
        CREATE TABLE IF NOT EXISTS invoices (
            id INT AUTO_INCREMENT PRIMARY KEY,
            invoice_date DATE,
            due_date DATE,
            paid_date DATE,
            amount_due DECIMAL(10, 2),
            amount_paid DECIMAL(10, 2),
            customer_name VARCHAR(100)
        )'''
    
    # Executing the SQL query to create the 'invoices' table.
    cursor.execute(create_table_query)
    
    # SQL query to insert test data into the 'invoices' table.
    insert_query = '''
        INSERT INTO invoices (invoice_date, due_date, paid_date, amount_due, amount_paid, customer_name)
        VALUES (%s, %s, %s, %s, %s, %s)'''
    
    # Creating a Faker instance to generate random test data.
    fake = Faker()
    
    # Generating test data.
    test_data = []
    for _ in range(200):
        invoice_date = fake.date_between(start_date='-1y', end_date='today')
        due_date = invoice_date + timedelta(days=30)
        paid_date = due_date - timedelta(days=random.randint(0, 10)) if random.choice([True, False]) else None
        amount_due = round(random.uniform(100, 1000), 2)
        amount_paid = round(random.uniform(0, amount_due), 2) if paid_date else 0.0
        customer_name = fake.name()
        test_data.append((invoice_date, due_date, paid_date, amount_due, amount_paid, customer_name))
    
    # Inserting test data into the 'invoices' table.
    cursor.executemany(insert_query, test_data)
    
    # Closing the cursor.
    cursor.close()

# Function to get the names of all tables in the database.
def get_all_table_names(connection):
    # Creating a cursor to execute SQL statements.
    cursor = connection.cursor()

    # SQL query to get all table names in the database.
    cursor.execute("SHOW TABLES")

    # Fetching all rows from the last executed statement.
    results = cursor.fetchall()

    # Closing the cursor.
    cursor.close()

    # Returning the table names.
    return [table_name for (table_name,) in results]

# Function to get the schema of a specific table.
def get_table_schema(connection, table_name):
    # Creating a cursor to execute SQL statements.
    cursor = connection.cursor()

    # SQL query to get the columns and data types of the specified table.
    cursor.execute(f"""
        SELECT COLUMN_NAME, DATA_TYPE 
        FROM INFORMATION_SCHEMA.COLUMNS
        WHERE TABLE_NAME = '{table_name}'
    """)

    # Fetching all rows from the last executed statement.
    results = cursor.fetchall()

    # Creating a string representation of the schema.
    schema_str = f"{table_name} ("
    schema_str += ', '.join([f"{column}:{datatype}" for column, datatype in results])
    schema_str += ")"

    # Closing the cursor.
    cursor.close()

    # Returning the string representation of the schema.
    return schema_str

# Function to get the schemas of all tables in the database.
def get_all_table_schemas(connection):
    # Getting all table names.
    table_names = get_all_table_names(connection)

    # Getting the schema for each table.
    schemas = [get_table_schema(connection, table_name) for table_name in table_names]

    # Returning the list of schemas.
    return schemas
