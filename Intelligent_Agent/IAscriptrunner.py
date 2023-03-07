import os
import sqlite3
import csv

db_is_new = not os.path.exists("SDGP.db")
db_is_new = True

header = []

tempManCap = open("COMPONENT MANUFACTURER CAPACITY.csv", "r")
tempCompReq = open("COMPONENT REQUIREMENTS.csv", "r")
tempCourierCap = open("COURIER CAPACITY.csv", "r")

manCap = csv.reader(tempManCap)
header = next(manCap)

compReq = csv.reader(tempCompReq)
header = next(compReq)

courierCap = csv.reader(tempCourierCap)
header = next(courierCap)


with sqlite3.connect("SDGP.db") as conn:
    if db_is_new:
        print ('Creating schema')
        with open("schemaIA.sql", 'rt') as f:
            schema = f.read()
        conn.executescript(schema)

        for row in manCap:    
            conn.execute("""insert into components (component, manufacturer1, capacity1,
            manufacturer2, capacity2, manufacturer3, capacity3, manufacturer4, capacity4,
            manufacturer5, capacity5) 
            values ((?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?))""", 
            (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))
        
        for row in courierCap:    
            conn.execute("""insert into courier (dayReq, courier1, capacity1,
            courier2, capacity2, courier3, capacity3, courier4, capacity4,
            courier5, capacity5) 
            values ((?), (?), (?), (?), (?), (?), (?), (?), (?), (?), (?))""", 
            (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10]))

        for row in compReq:    
            conn.execute("""insert into requirements (dayReq, component1, quantity1,
            component2, quantity2) 
            values ((?), (?), (?), (?), (?))""", 
            (row[0], row[1], row[2], row[3], row[4]))
    
        conn.commit()
    else:
        print ('Database exists, assume schema does, too.')

tempManCap.close()
tempCompReq.close()
tempCourierCap.close() 