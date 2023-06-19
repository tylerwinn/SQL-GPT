# Import necessary libraries and modules
from dotenv import load_dotenv
from datetime import datetime
import os
import MySQLdb
import openai
import sql

# Load environment variables from .env file
load_dotenv()

# Set the API key for OpenAI from environment variable
openai.api_key = os.getenv("OPENAI_API_KEY")

# Establish a connection to the MySQL database using the environment variables
# The connection uses SSL with a certification file "cert.pem" for security.
connection = MySQLdb.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USERNAME"),
    passwd=os.getenv("DB_PASSWORD"),
    db=os.getenv("DATABASE"),
    autocommit=True,
    ssl={
        "ca": "cert.pem"
    }
)

# Fetch the schema of all tables in the database
# get_all_table_schemas is a function in the sql module that retrieves the schema information
schema = sql.get_all_table_schemas(connection)

# Prompt the user to enter a natural language query
user_input = input("Please enter a query: ")

# Gets the current datetime to supply to chatGPT
current_datetime = datetime.now()

# Call the OpenAI ChatCompletion API with a conversation history to convert natural language query to SQL
# The conversation includes system instructions, user providing the database schema, and the natural language query
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[
    {"role": "system", "content": f"The current datetime is: {current_datetime} You convert natural speech to SQL Queries. Respond with nothing but an SQL query. The user will provide the schema like ['table1 (column1:date, column2:varchar, column3:int)', 'table2 (column1:decimal, column2:decimal, column3:varchar)']"},
    {"role": "user", "content": f"My schema is {schema}"},
    {"role": "user", "content": f"{user_input}"}
  ]
)

# Extract the SQL query from the API response's content field
# and replace newline characters with spaces to format the query into a single line
sql_query = completion.choices[0].message["content"].replace("\\n", " ")

# Print the SQL query to the console
print(sql_query)

# Create a cursor object to interact with the MySQL database
cursor = connection.cursor()

# Execute the SQL query using the cursor
cursor.execute(sql_query)

# Fetch the result set of the query and print each row
# This is relevant for queries that retrieve data, such as SELECT statements
results = cursor.fetchall()
for row in results:
    print(row)

# Close the cursor to free up resources
cursor.close()

# Close the database connection
connection.close()
