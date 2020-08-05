import psycopg2
from sys import argv

# Import the database config file
from db_config import pg_connection_string

# Connect to the database using the config parameters
def connect():
	try:
		connection = psycopg2.connect(pg_connection_string)
	except:
		print("ERROR: Error while connecting to the database using:\n%s" % pg_connection_string)
		raise
	return connection

# Close the connection
def disconnect(connection):
	connection.close()

# Execute the query provided
def execute(connection, query, result):
	try:
		# Create a cursor to the database
		cursor = connection.cursor()
		# Execute the query using the cursor
		cursor.execute(query)
		# Commit the changes to the database
		connection.commit()
		# Return result if asked
		if result:
			return cursor.fetchall()
	except:
		print("ERROR: Error while executing the sql query:\n%s" % query)
		raise
