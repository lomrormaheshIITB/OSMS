import argparse, csv, hashlib, psycopg2, re, os, shutil, xlrd
from datetime import datetime

# Import the query execution function from db_execute
import db_execute as db

# Global variables
# BASE_DIR = 'E:/OTHER_STUFF/Django_projects/LATEST/osms/'
BASE_DIR = '/home/shashankkumar/Downloads/osms/'
MEDIA_DIR = os.path.join(BASE_DIR, 'media/')
NOW = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')

# Converts x to int
def toInt(x):
	try:
		return int(float(x))
	except:
		return 0

# Converts the given element to upper case if string
# Otherwise returns the int representation
def toUpper(x):
	try:
		return int(float(x))
	except:
		return x.upper()

# Returns the boolean value for critical field
def toBoolCritical(x):
	return (x == 'YES')

# Remove extra spaces
def removeSpace(x):
	try:
		return re.sub(' +', ' ', x)
	except:
		return x

# Create directory structure in media folder to save images
def createDir(spare_class, equipment_class):
	global MEDIA_DIR
	# 'MEDIA_DIR/<spare_class>/'
	path_spare_class = os.path.join(MEDIA_DIR, spare_class)
	if (not os.path.isdir(path_spare_class)):
		os.mkdir(path_spare_class)

	# 'MEDIA_DIR/<spare_class>/<equipment_class>'
	path_equipment_class = os.path.join(path_spare_class, equipment_class)
	if (not os.path.isdir(path_equipment_class)):
		os.mkdir(path_equipment_class)
	return path_equipment_class

# Check image extension
def checkImage(imagepath):
	if (os.path.isfile(imagepath)):
		name, extension = os.path.splitext(imagepath)
		return (extension in ['.png', '.jpg', '.jpeg'])
	else:
		return False

# Return the md5 hash of the file
def md5Image(imagepath):
	with open(imagepath, 'rb') as file:
		filehash = hashlib.md5(file.read())
	return filehash.hexdigest()

# Save the images to the database
def saveImage(imagepath, spare_class, equipment_class):
	global MEDIA_DIR
	# Create mediapath = MEDIA_DIR/<spare_class>/<equipment_class>/
	mediapath = os.path.join(MEDIA_DIR, spare_class, equipment_class)
	# Create a temporary directory at MEDIA_DIR
	temp_dir = os.path.join(MEDIA_DIR, 'temp')
	os.mkdir(temp_dir)
	
	# Copy the file from the path specified in excel to temp folder in media
	shutil.copy(imagepath, temp_dir)

	# Get the name and extension of the image
	imagename  = os.path.basename(imagepath)
	imagebase, imageextension = os.path.splitext(imagename)
	
	# Get the path to this image in the temp folder
	imagepath_temp = os.path.join(temp_dir, imagename)
	
	# Reaname the image with spare id and move it to media folder
	imagename_new = f"{md5Image(imagepath)}{imageextension}"
	imagepath_new = os.path.join(mediapath, imagename_new)
	shutil.move(imagepath_temp, imagepath_new)

	# Remove the temp directory
	shutil.rmtree(temp_dir)
	return imagename_new

# Get the spare with maximum id
def getMaximumSpareId():
	query = f"""SELECT MAX(id) FROM data_spares;"""
	result = db.execute(connection, query, True)
	return result[0][0]

# Get maximum id from the issue table
def getMaximumIssueId():
	query = f"""SELECT MAX(id) FROM data_issue;"""
	result = db.execute(connection, query, True)
	return result[0][0]

# Get maximum id from the postsurvey table
def getMaximumPostSurveyId():
	query = f"""SELECT MAX(id) FROM data_postsurvey;"""
	result = db.execute(connection, query, True)
	return result[0][0]

# Insert the specified spare quantity to the survey table
def insertSurveyTable(connection, spare_id, quantity_tosurvey):
	query = f"""
	INSERT INTO data_survey(spare_id, quantity_tosurvey) VALUES ({spare_id}, {quantity_tosurvey});
	"""
	db.execute(connection, query, False)

# Insert the specified quantity spare to the demand table
def insertDemandTable(connection, spare_id, quantity_todemand):
	global NOW
	# Create a survey entry with 'NA' as the survey_number
	query = f"""INSERT INTO data_postsurvey (spare_id, survey_number, quantity_surveyed, survey_number_date, survey_report_date, remarks) 
	VALUES ('{spare_id}', 'NA', '{quantity_todemand}', '{NOW}', '{NOW}', 'CONSUMABLE SPARE');"""
	db.execute(connection, query, False)

	survey_number_id = getMaximumPostSurveyId()
	query = f"""
	INSERT INTO data_demand(spare_id, quantity_todemand, survey_entry_id) VALUES ('{spare_id}', '{quantity_todemand}', '{survey_number_id}');
	"""
	db.execute(connection, query, False)

# Insert into the issuelist table and survey/demand table based on category of the spare
def insertIssueListTable(connection, delta):
	# Fetch the spare with maximum id
	spare_id = getMaximumSpareId()
	# Create an issue entry for the spare
	query = f""" 
	INSERT INTO data_issue(spare_id, username, quantity_issued, remarks) VALUES ('{spare_id}', 'DEFAULT_USER', '{delta}', ' Onoard held quantity is less than authorised quantity.');
	"""
	db.execute(connection, query, False)
	issue_id = getMaximumIssueId()
	# Insert into the issuelist table
	query = f""" 
	INSERT INTO data_issuelist(issue_entry_id, quantity_toreturn) VALUES ('{issue_id}', '{delta}');
	"""
	db.execute(connection, query, False)
	# Insert into  survey/demand table
	if (row[labels['category']] == "CONSUMABLE"):
		insertDemandTable(connection, spare_id, delta)
	else:
		insertSurveyTable(connection, spare_id, delta)

# Driver routine
if __name__ == '__main__':
	# Create a arguemnt parser with file path as argument
	parser = argparse.ArgumentParser()
	parser.add_argument('--file', type=str, required=True, help='The path to the excel file.')
	args = parser.parse_args()

	# Create a connection to the database
	connection = db.connect()

	# Open the excel book
	book =  xlrd.open_workbook(args.file)

	# Create a set for the spare class
	set_spare_class = set()
	num_spare_class = 0

	# Create a set for the equipment class
	set_equipment_class = set()
	num_equipment_class = 0

	# Create a set for the denominations
	set_denos = set()
	num_denos = 0

	# Number of new entries entered in the database
	new_entries = 0

	# Save the excel data to databases
	for sheet in book.sheets():
		labels = list(map(lambda x: x.lower(), sheet.row_values(0)))
		labels = dict(zip(labels, range(sheet.ncols)))
		for i in range(1, sheet.nrows):
			# Convert data to upper case
			row = list(map(lambda x: toUpper(x), sheet.row_values(i)))
			
			# Replace forward slash('/') with 'OR'
			row[labels['class of spare']] = row[labels['class of spare']].replace('/', ' OR ')
			row[labels['class of equipments/valves/fittings/pll as per d787j']] = row[labels['class of equipments/valves/fittings/pll as per d787j']].replace('/', ' OR ')

			# Remove redundant spaces
			row = list(map(lambda x: removeSpace(x), row))

			# Replace the picture path without any of the above changes
			row[labels['picture path']] = sheet.row_values(i)[labels['picture path']]

			pattern_number = row[labels['pattern number']]
			spare_class = row[labels['class of spare']]
			equipment_class = row[labels['class of equipments/valves/fittings/pll as per d787j']]

			# Ignore entry if spare_class or equipment_class missing
			if (not spare_class or not equipment_class):
				print("Spare class or equipment class missing. Ignoring entry.")
				continue

			# Check if an entry corresponding to a pattern number exists
			if (pattern_number):
				check_query = f"""SELECT count(*) FROM data_spares 
					WHERE pattern_number='{pattern_number}'"""
				result = db.execute(connection, check_query, True)
				if result[0][0] != 0:
					print("Entry corresponding to pattern number: %s already exists. Ignoring this entry." % pattern_number)
					continue

			# Insert if entry not found
			insert_query = f"""
			INSERT INTO data_spares(
								pattern_number,
								spare_class, 
								equipment_class, 
								description, 
								category, 
								critical, 
								compartment, 
								location, 
								denomination, 
								quantity_authorised, 
								quantity_available, 
								authority,
								page, 
								line,
								image
								) 
			VALUES (
				'{pattern_number}',
				'{spare_class}',
				'{equipment_class}',
				'{row[labels['description']]}',
				'{row[labels['category']]}',
				'{toBoolCritical(row[labels['critical']])}',
				'{row[labels['onboard location']]}',
				'{row[labels['box number']]}',
				'{row[labels['denomination']]}',
				'{row[labels['quantity authorised']]}',
				'{row[labels['quantity held']]}',
				'{row[labels['authority']]}',
				'{row[labels['d787j page number']]}',
				'{toInt(row[labels['d787j line number']])}',
			"""
			
			set_spare_class.add(spare_class)
			set_equipment_class.add((spare_class, equipment_class))
			set_denos.add(row[labels['denomination']])

			# Check if a new entry is added to set_spare_class or set_equipment_class
			if (num_spare_class != len(set_spare_class) or num_equipment_class != len(set_equipment_class)):
				num_spare_class = len(set_spare_class)
				num_equipment_class = len(set_equipment_class)
				createDir(spare_class, equipment_class)

			# Complete the insert query and add image to the appropriate directory
			imagepath = row[labels['picture path']]
			if (imagepath and checkImage(imagepath)):
				imagename_new = saveImage(imagepath, spare_class, equipment_class)
				insert_query += f"'{spare_class}/{equipment_class}/{imagename_new}');"
			else:
				insert_query += f"'default.png');"
			
			# Insert record to the database
			db.execute(connection, insert_query, False)
			new_entries += 1

			# Insert spare to the issuelist table based on the quantity held and authorised
			delta = row[labels['quantity authorised']] - row[labels['quantity held']]
			if (delta > 0):
				insertIssueListTable(connection, delta)

	# Add spare_class entries to database table
	for c in set_spare_class:
		insert_query = f"INSERT INTO data_spareclass(name) VALUES ('{c}');"
		db.execute(connection, insert_query, False)	

	# Add equipment_class entries to database table
	for c in set_equipment_class:
		insert_query = f"INSERT INTO data_equipmentclass(spare_class, name) VALUES ('{c[0]}', '{c[1]}');"
		db.execute(connection, insert_query, False)	

	# Add denos entries to database table
	for d in set_denos:
		insert_query = f"INSERT INTO data_denomination(name) VALUES ('{d}');"
		db.execute(connection, insert_query, False)	

	# Add authority to database table
	authority = ['D787J', 'ALLOWANCE LIST', 'COMMAND APPROVAL', 'IHQ APPROVAL']
	for a in authority:
		insert_query = f"INSERT INTO data_authority(name) VALUES ('{a}');"
		db.execute(connection, insert_query, False)

	# Add rank to database table
	rank = ['MCHMECH','MCHERA','SLT', 'LT', 'LT CDR', 'CDR']
	for b in rank:
		insert_query = f"INSERT INTO users_rank(name) VALUES ('{b}');"
		db.execute(connection, insert_query, False)

	# Add department to database table
	department = ['ENGINEERING','ELECTRICAL', 'EXECUTIVE', 'LOGISTICS', 'NBCD']
	for a in department:
		insert_query = f"INSERT INTO users_department(name) VALUES ('{a}');"
		db.execute(connection, insert_query, False)


	print("%d New entries added to the database." % new_entries)

	# Add a default user_profile in CustomUserProfile	
	Y = ['CDR','ABC','XYZ','ADMIN','NA','NA']	
	insert_query = f"""INSERT INTO users_customuserprofile(rank_id, firstname, lastname, access_level, department_id, personal_number, section, remarks, ship_joining_date) 
					   VALUES ('{5}', '{Y[1]}', '{Y[2]}', '0', '1', '{Y[3]}', '{Y[4]}', '{Y[5]}', {NOW});"""
	db.execute(connection, insert_query, False)	
	print('Default user profile created successfully')

	# Close the connection
	db.disconnect(connection)
