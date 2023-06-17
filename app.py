from flask import Flask, request, render_template
import os
import MySQLdb
import openai
from datetime import datetime
import sql

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        db_host = request.form['db_host']
        db_username = request.form['db_username']
        db_password = request.form['db_password']
        database = request.form['database']
        openai_api_key = request.form['openai_api_key']
        user_query = request.form['user_query']

        # Establish a connection to the MySQL database
        connection = MySQLdb.connect(
            host=db_host,
            user=db_username,
            passwd=db_password,
            db=database,
            autocommit=True,
            ssl={
                "ca": "cert.pem"
            }
        )

        # Fetch the schema of all tables in the database
        schema = sql.get_all_table_schemas(connection)

        # Set the API key for OpenAI
        openai.api_key = openai_api_key

        # Gets the current datetime to supply to chatGPT
        current_datetime = datetime.now()

        # Call the OpenAI ChatCompletion API
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"The current datetime is: {current_datetime} You convert natural speech to SQL Queries. Respond with nothing but an SQL query. The user will provide the schema like ['table1 (column1:date, column2:varchar, column3:int)', 'table2 (column1:decimal, column2:decimal, column3:varchar)']"},
                {"role": "user", "content": f"My schema is {schema}"},
                {"role": "user", "content": f"{user_query}"}
            ]
        )

        # Extract the SQL query from the API response
        sql_query = completion.choices[0].message["content"].replace("\\n", " ")

        # Create a cursor object to interact with the MySQL database
        cursor = connection.cursor()

        # Execute the SQL query using the cursor
        cursor.execute(sql_query)

        # Fetch the result set of the query
        results = cursor.fetchall()

        # Close the cursor and the connection
        cursor.close()
        connection.close()

        return render_template('index.html', results=results, sql_query=sql_query)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
