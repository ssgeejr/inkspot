import csv
import mysql.connector
from datetime import datetime

# Database configuration
db_config = {
    'host': 'enceladus',
    'user': 'enceladus',
    'password': 'twilightzone',
    'database': 'enceladus'
}

# CSV file path
csv_file_path = 'phishing.csv'

# Connect to the MySQL database
db_connection = mysql.connector.connect(**db_config)
cursor = db_connection.cursor()

# Create table if it doesn't exist
create_table_query = '''
CREATE TABLE IF NOT EXISTS phishing (
    id INT NOT NULL AUTO_INCREMENT,
    email VARCHAR(36),
    action VARCHAR(36),
    dt datetime,
    ip VARCHAR(15),
    PRIMARY KEY (id)
)
'''

cursor.execute(create_table_query)

date_format = '%m/%d/%Y %H:%M'



# Open the CSV file and insert each record
with open(csv_file_path, mode='r', encoding='utf-8') as file:
    csv_reader = csv.reader(file)
#    next(csv_reader)  # Skip the header row, remove this line if your CSV doesn't have a header
    counter = 0 
    total = 0 
    for row in csv_reader:
        #datetime_obj = 
        row[1] = datetime.strptime(row[1],date_format)
 #       print(row[1])
 #       exit(-1)
        
        insert_query = 'INSERT INTO phishing (email, dt, action, ip) VALUES (%s, %s, %s, %s)'
        
        cursor.execute(insert_query, row)
        counter += 1  # Increment the counter
        total += 1
        # Commit every 100 rows
        if counter % 100 == 0:
            db_connection.commit()
            print("Committed 100 rows * total of %s" % total)
    db_connection.commit()
    print("Committed %s rows * total of %s" % (counter,total))
# Commit changes and close the connection
db_connection.commit()
cursor.close()
db_connection.close()
