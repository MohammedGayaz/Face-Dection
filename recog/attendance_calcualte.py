import pandas as pd
from datetime import datetime
import mysql.connector


mydb = mysql.connector.connect(
    host="sql.freedb.tech",
    port=3306,
    user="freedb_sairevan",
    password="ywjNCF*cBdG2W#P",
    database="freedb_facere"
)

mycursor = mydb.cursor()

print(mydb)

now = datetime.now()
date = now.strftime('%d-%m-%Y')
month = now.strftime('%B')

final_attendance = dict()


def calculate_attendance():
    attendance_data = pd.read_csv(f"Attendance_{month}.csv")
    usns = attendance_data["USN"].to_list()
    for usn in usns:
        if usn not in final_attendance:
            final_attendance[usn] = 1
        else:
            final_attendance[usn] += 1
    print(final_attendance)

    for usn, no_classes in final_attendance.items():
        print(mycursor.rowcount)
        if mycursor.rowcount < 1:
            print('hello')
            sql = "update student SET no_classes =(%s) where USN =(%s)"
            val = (no_classes, usn)
            mycursor.execute(sql, val)
            mydb.commit()
        else:
            sql = "INSERT INTO attendance (USN, no_classes) VALUES (%s, %s)"
            val = (usn, no_classes)
            mycursor.execute(sql, val)
            mydb.commit()
    print(mycursor.rowcount, "record inserted.")

