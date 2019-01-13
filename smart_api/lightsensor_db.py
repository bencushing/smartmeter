from datetime import datetime
import sqlite3


def create_connection(db_file):
	""" create a database connection to the SQLite database
		specified by db_file
	:param db_file: database file
	:return: Connection object or None
	"""
	try:
		conn = sqlite3.connect(db_file, detect_types=sqlite3.PARSE_DECLTYPES)
		return conn
	except Error as e:
		print(e)
 
	return None

def create_table(conn, create_table_sql):
	""" create a table from the create_table_sql statement
	:param conn: Connection object
	:param create_table_sql: a CREATE TABLE statement
	:return:
	"""
	try:
		c = conn.cursor()
		c.execute(create_table_sql)
	except Error as e:
		print(e)
	

def get_max_id(conn, tablename):
	cur = conn.cursor()
	
	cur.execute("select max(id) from " + tablename)
	return int(cur.fetchone()[0])
	
	
def check_table_schema(conn, tablename):
	sql = ".schema " + tablename
	cur = conn.cursor()
	print(type(tablename))
	
	cur.execute(sql)
	print(cur.fetchone())
	return 0 
	
	
def add_pulse(conn, pulse_datetime):
	"""
	Create a new project into the projects table
	:param conn:
	:param project:
	:return: project id
	"""
	sql = ''' INSERT INTO pulses(id, pulse_datetime)
			  VALUES(?,?) '''
	cur = conn.cursor()
	newid = get_max_id(conn, 'pulses') + 1
	
	cur.execute(sql, (newid, pulse_datetime))
	return cur.lastrowid

def get_last_pulse(conn):
	sql = ''' SELECT pulse_datetime FROM pulses
			  ORDER BY id DESC
			  LIMIT 1 '''
	cur = conn.cursor()
	cur.execute(sql);
	return cur.fetchone()[0]
	
def get_last_pulses(conn, limit):
	sql = ''' SELECT pulse_datetime FROM pulses
			  ORDER BY id DESC
			  LIMIT ''' + str(limit)
	cur = conn.cursor()
	cur.execute(sql);
	return cur.fetchall()

	
sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS pulses (
                                        id integer PRIMARY KEY,
                                        pulse_datetime timestamp
                                    ); """
