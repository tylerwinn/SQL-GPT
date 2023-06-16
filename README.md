# Text to SQL

This repository contains two Python scripts, sql.py and translate.py, which are designed to interact with a MySQL database. sql.py is used for creating and populating tables with sample data, while translate.py uses OpenAI's GPT to translate natural language queries into SQL queries and execute them on the database.
## Getting Started
### Prerequisites

    Python 3.6+
    MySQL Database
    OpenAI Python library
    MySQLdb Python library
    python-dotenv library
    Faker Python library

### Installation

Clone the repository:

```
git clone https://github.com/tylerwinn/SQL-GPT.git
cd SQL-GPT
```
Install the required Python libraries:
```
pip install mysqlclient openai python-dotenv Faker
```
Set up your MySQL database and ensure it is running.

Create a .env file in the root directory of your project with the following variables:

```
DB_HOST=your_database_host
DB_USERNAME=your_database_username
DB_PASSWORD=your_database_password
DATABASE=your_database_name
OPENAI_API_KEY=your_openai_api_key
```
## Usage
### sql.py

This script creates and populates two tables, 'employees' and 'invoices', in the MySQL database with sample data.

To execute this script, first import create_employees_table and create_invoices_table functions from sql.py into your script.

Establish a connection to your MySQL database.

Call create_employees_table and create_invoices_table with your database connection as an argument.

Example:

python
```
import MySQLdb
from SQL import create_employees_table, create_invoices_table

# Establish a connection
connection = MySQLdb.connect(host='localhost', user='root', passwd='password', db='test_db')

# Create and populate tables
create_employees_table(connection)
create_invoices_table(connection)
```
### translate.py

This script takes a natural language query as input, translates it into an SQL query using OpenAI's GPT, and executes it on the database.

    Run the script:
```
python translate.py
```
Enter a natural language query when prompted, such as "Show me all employees born after 1990".

The script will translate your query into SQL, execute it, and display the results.

Note

Ensure that your MySQL database is properly set up and the connection details in the .env file are correct.

## Built With

    Python
    MySQL
    OpenAI GPT


## Acknowledgments

    OpenAI for providing the GPT model.
    Faker for generating fake data.

## Contributing

Contributions are welcome!

## Contact

Tyler Winn - tyler.winn@pm.me
