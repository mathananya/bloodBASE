#import pyodbc
from datetime import datetime
from tabulate import tabulate
import csv

blood_group = ["A+","A-","B+","B-","AB+","AB-","O+","O-"]

blood_type = ["Platelet","RbcA+","RbcA-","RbcB+","RbcB-","RbcAB+","RbcAB-","RbcO+","RbcO-",
              "PlsA+","PlsA-","PlsB+","PlsB-","PlsAB+","PlsAB-","PlsO+","PlsO-"]


# conn = pyodbc.connect("Driver={ODBC Driver 17 for SQL Server};"
#                       "Server=localhost;"
#                       "Database=db_bloodbase;"
#                       "Trusted_Connection=yes;")

import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1ismynumber',
    database = 'db_bloodbase')


def show_table_details(table_list):
    cursor = conn.cursor()
    for table in table_list:
        print('\nTable name = %s' %table)
        cursor.execute(f'SELECT * FROM {table}')
        for row in cursor.fetchall():
            print(row)
        print()
    cursor.close()
    return


def create_donor():
    cursor = conn.cursor()
    # finding the next larger donor id in format DRx
    sql = "SELECT donor_id FROM Donors ORDER BY donor_id DESC"
    cursor.execute(sql)
    id_list = [x[0] for x in cursor.fetchall()]
    did = "DR1"
    while did in id_list:
        #keep incrementing
        did = "DR"+str(int(did[2:])+1)
    # capturing all donor details as user inputs
    print(f"\nCreating new donor - Please enter details below")
    fname = input("First Name: ")
    lname = input("Last Name: ")
    dob = input("DoB as YYYY-MM-DD: ")
    address = input("Address: ")
    email = input("Email id: ")
    phone = input("Phone no: ")
    bg = ''
    while bg not in blood_group:
        bg = input("Blood group A+/A-/B+/B-/AB+/AB-/O+/O-: ")
    # writing to Donor table in database
    val = (did, fname, lname, dob, address, email, phone, bg)
    sql = "INSERT INTO Donors (donor_id, f_name, l_name, dob, address, email, phone, bgroup) VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    try:
        cursor.execute(sql,val)
        print(f"\nSuccessfully created new donor with a Donor ID = {did} ****")
    except:
        print(f"\nSorry - the donor data provided could not be registered ****")
    conn.commit()
    cursor.close()
    return


def collect_blood():
    did = input("\nWelcome to blood donation station. Please provide your registered Donor id (format DRx): ")
    # check if the donor id exists in the Donors table
    cursor = conn.cursor()
    sql = "SELECT donor_id FROM Donors"
    cursor.execute(sql)
    all_ids = [i[0] for i in cursor.fetchall()]
    if did in all_ids:
        sql = "SELECT f_name, l_name, bgroup FROM Donors WHERE donor_id = ?"
        cursor.execute(sql,did)
        info = cursor.fetchone()
        print(f"Hi {info[0]}. THANK YOU for your donation.\nYour blood group is registered as {info[2]}.")
        cursor.fetchall()   #to empty the cursor
        # finding the next larger collection id in format CLx
        sql = "SELECT coll_id FROM Collections ORDER BY coll_id DESC"
        cursor.execute(sql)
        id_list = [x[0] for x in cursor.fetchall()]
        cid = "CL1"
        while cid in id_list:
            #keep incrementing
            cid = "CL"+str(int(cid[2:])+1)
        qty = input(f"This collection has id {cid}. We are confirming number of units donated today (enter integer) :")
        tim = datetime.now()
        val = (cid, tim, did, int(qty))
        sql = "INSERT INTO Collections (coll_id, coll_time, donor_id, units) VALUES (?, ?, ?, ?)"
        
        try:
            cursor.execute(sql,val)
            print(f"\nSuccessfully created new collection with a Collection ID = {cid} ****")
            # create a sample for testing
            sql = "INSERT INTO Samples (coll_id) VALUES (?)"
            val = (cid)
            try:
                cursor.execute(sql,val)
                print("A sample of this collection has been successfully registered for testing.")
            except:
                print("Alert - sample could not get created for testing!!")
        except:
            print(f"\nSorry - the collection data could not be registered !!!!")  
     
    else:
        print("Sorry - your Id is not registered. Please register yourself first as new donor.")
    conn.commit()
    cursor.close()
    return


def test_blood():
    # list collections pending test
    cursor = conn.cursor()
    sql = "SELECT coll_id FROM Samples WHERE result IS NULL"
    cursor.execute(sql)
    all_ids = [i[0] for i in cursor.fetchall()]
    print(f"We have {len(all_ids)} pending testing. Please enter the id from list below :")
    print(all_ids)
    if len(all_ids)==0:
        print('Returning to menu, as no samples are awaiting testing.')
        return
    # choose a cid and provide test result
    cid = ''
    while cid not in all_ids:
        cid = input("Enter the id (in format CLx) chosen from list above :")
    bgroup = ''
    while bgroup not in blood_group:
        bgroup = input(f'Confirm blood group from list {blood_group} :')
    btype = "Rbc"+bgroup
    print(f"Enter the result of the test for chosen sample id {cid} below.")
    result = ''
    while result not in ['y','n']:
        result = input("Enter y/n for whether sample passed all screening checks :")
    result_int = {'y':1,'n':0}[result]
    tim = datetime.now()
    sql = "UPDATE Samples SET test_time = ?, btype = ?, result = ? WHERE coll_id = ?"
    val = (tim, btype, result_int, cid)
    try:
        cursor.execute(sql,val)
        print(f"\nTest result ** {result} ** updated in database at time {tim}.")
    except:
        print("Alert - test results could not be updated!!")
    # if passed update inventory , else update rejections
    if result == 'y':
        sql = "SELECT units FROM Collections WHERE coll_id = ?"
        cursor.execute(sql,cid)
        info = cursor.fetchone()        
        val = (cid, info[0])
        sql = "INSERT INTO Inventory (coll_id, units) VALUES (?, ?)"
        try:
            cursor.execute(sql,val)
            print(f"\nSuccessfully updated inventory with batch of {info[0]} units ****")
        except:
            print(f"\nAlert - inventory could not be updated !!!")
    else:
        sql = "SELECT units FROM Collections WHERE coll_id = ?"
        cursor.execute(sql,cid)
        info = cursor.fetchone()
        val = (cid, info[0], tim)
        sql = "INSERT INTO Rejections (coll_id, units, time) VALUES (?, ?, ?)"
        try:
            cursor.execute(sql,val)
            print(f"\nSuccessfully updated rejection with batch of {info[0]} units ****")
        except:
            print(f"\nAlert - Rejections could not be updated !!!")
    conn.commit()
    cursor.close()
    print('\nTesting done. Returning to menu.')
    return


def check_inventory():
    return

def create_demand():
    cursor = conn.cursor()
    # finding the next larger demand id in format DMx
    sql = "SELECT demand_id FROM Demand ORDER BY demand_id DESC"
    cursor.execute(sql)
    row=cursor.fetchone()
    if row is not None:
        dmid_no = int(row[0][2:]) + 1
        dmid = "DM"+str(dmid_no)
    else:
        dmid = "DM1"
    cursor.fetchall()   #to empty the cursor
    pid = input("Please enter a valid patient id :")
    btype = ''
    while btype not in blood_type:
        btype = input(f"Please enter a valid blood type from list {blood_type}: ")
    qty = int(input("Please enter number of units needed: "))
    tim = datetime.now()
    val = (dmid, pid, btype, qty, tim, 'new')
    sql = "INSERT INTO Demand (demand_id, patient_id, type, units, time, status) VALUES (?, ?, ?, ?, ?, ?)"
    try:
        cursor.execute(sql,val)
        print(f"\nSuccessfully created new demand with a Demand ID = {dmid} ****")
    except:
        print(f"\nSorry - the demand data could not be registered **!!")
    conn.commit()
    cursor.close()
    return


def issue_blood():
    #look for created dmid in Demand that has status 'new'. Note type needed
    cursor = conn.cursor()
    sql = "SELECT demand_id, type, units FROM Demand WHERE status = 'new'"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        dmid = row[0]
        dtype = row[1]
        units_demanded = row[2]
    #query Inventory for coll_id entries that have btype in Samples same as type needed, sorted by test_time
        sql = "SELECT coll_id FROM Samples WHERE btype = ? ORDER BY test_time ASC"
        cursor.execute(sql,dtype)
        coll_ids = cursor.fetchall()
        coll_ids = [i[0] for i in coll_ids]
        # for coll_id in coll_ids:
        #     sql = "SELECT units FROM Inventory WHERE coll_id = ?"
        #     qty = cursor.execute(sql,coll_id).fetchone()[0]
        #     print(f'Inventory item for {coll_id}, has {qty} units')

        print(f"\nNew demand {dmid} for {units_demanded} units of type {dtype}:")
    #start reducing units from coll_id Inventory entries  till all completed or demand units met
        units_remaining = units_demanded
        for coll_id in coll_ids:
            sql = "SELECT units FROM Inventory WHERE coll_id = ?"
            cursor.execute(sql, coll_id)
            units_found = [i[0] for i in cursor.fetchall()]
            if units_remaining > 0 and len(units_found) == 1:
                units_found = units_found[0]
                if units_found == 0:
                    pass
                elif units_found <= units_remaining:
                    sql = "INSERT INTO Inv_Issue (coll_id, demand_id, units) VALUES (?, ?, ?)"
                    val = (coll_id, dmid, units_found)
                    cursor.execute(sql, val)
                    print(f'Inv_Issue of {units_found} units from {coll_id}')
                    sql = "UPDATE Inventory SET units = 0 WHERE coll_id = ?"
                    cursor.execute(sql, coll_id)
                    units_remaining -= units_found
                else:
                    sql = "INSERT INTO Inv_Issue (coll_id, demand_id, units) VALUES (?, ?, ?)"
                    val = (coll_id, dmid, units_remaining)
                    cursor.execute(sql, val)
                    print(f'Inv_Issue of {units_remaining} units from {coll_id}')
                    sql = "UPDATE Inventory SET units = ? WHERE coll_id = ?"
                    val = (units_found - units_remaining, coll_id)
                    cursor.execute(sql, val)
                    units_remaining = 0
        #update the demand status as part/fully met
        if units_remaining > 0:
            # demand status - part met
            sql = "UPDATE Demand SET status = ? WHERE demand_id = ?"
            val = ('less'+str(units_remaining),dmid)
        else:
            # demand status - fully met
            sql = "UPDATE Demand SET status = ? WHERE demand_id = ?"
            val = ('complete',dmid)
        cursor.execute(sql,val)

        #create entry for the demand_id also in Issues table with total units
        sql = "SELECT COALESCE(SUM(units),0) FROM Inv_Issue WHERE demand_id = ?"
        cursor.execute(sql,dmid)
        units_issued = cursor.fetchone()[0]
        if not(units_demanded == units_issued + units_remaining):
            print('Something is wrong with issue total units')
        else:
            sql = "INSERT INTO Issues (demand_id, units, issue_time) VALUES (?, ?, ?)"
            tim = datetime.now()
            val = (dmid, units_issued, tim)
            cursor.execute(sql,val)
            print(f'For demand id {dmid}, a total of {units_issued} units is issued.')
    conn.commit()
    cursor.close()
    return

def login():
    import getpass
    global authenticated
    print('*'*65)
    print('Welcome to Bloodbase - the Blood Bank Database Management System')
    print('-'*65)
    while not authenticated:
        usr = input('What is your user id? ')
        pwd = getpass.getpass('What is your password? ')
        cursor = conn.cursor()
        try:
            sql = "SELECT user_pwd, user_type FROM Users WHERE user_id = ?"
            cursor.execute(sql,usr)
            info = cursor.fetchone()
            if info[0] == pwd:
                role = info[1]
                print(f'Success {usr}. You are logged in now as {role}.\n') 
                authenticated = True    
            else:
                print('Password did not match! Please retry.\n') 
        except:
            print(f"User id does not exist! Please retry.\n")
    return role



def samples_report1():
    cursor = conn.cursor()
    try:
        sql = "SELECT Collections.coll_id, Collections.coll_time, Collections.donor_id, Donors.bgroup, Collections.units FROM Collections INNER JOIN Donors ON Collections.donor_id=Donors.donor_id"
        cursor.execute(sql)
        info = list(cursor)
        head = ['Collection id','Collection Date-time', 'Donor id', 'Blood group','Units']
        print('\nPrinting Collection Details:')
        print(tabulate(info, headers=head))
        csv_name = 'COL_'+datetime.today().strftime('%Y-%m-%d')+'.csv'
        with open(csv_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([head]+info)
        print(f'\n... csv file *{csv_name}* saved. Returning to manager menu.\n')
    except:
            print('Some problem in Collections table! Please retry.\n')
    
    return

def issues_report2():
    cursor = conn.cursor()
    try:
        sql = "SELECT Demand.demand_id, Demand.type, Demand.units, Issues.units, Issues.issue_time FROM Demand JOIN Issues ON Demand.demand_id=Issues.demand_id"
        cursor.execute(sql)
        info = list(cursor)
        head = ['Demand id','Blood type','Demanded units','Issued units','Issuing Date-time']
        print('\nPrinting Issuing Details:')
        print(tabulate(info, headers=head))
        csv_name = 'ISS_'+datetime.today().strftime('%Y-%m-%d')+'.csv'
        with open(csv_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([head]+info)
        print(f'\n... csv file *{csv_name}* saved. Returning to manager menu.\n')
    except:
            print('Some problem in Issues table! Please retry.\n')  
    return


def inventory_report3():
    cursor = conn.cursor()
    try:
        sql = "SELECT Inventory.coll_id, Samples.btype, Inventory.units, Collections.coll_time FROM Inventory INNER JOIN Samples ON Inventory.coll_id=Samples.coll_id INNER JOIN Collections ON Samples.coll_id=Collections.coll_id"
        cursor.execute(sql)
        info = [inv for inv in list(cursor) if inv[2]>0]
        head = ['Collection id','Blood type', 'Units left', 'Collection date-time']
        print('\nPrinting Inventory details:')
        print(tabulate(info, headers=head))
        csv_name = 'INV_'+datetime.today().strftime('%Y-%m-%d')+'.csv'
        with open(csv_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([head]+info)
        print(f'\n... csv file *{csv_name}* saved. Returning to menu.\n')
    except:
            print('Some problem in Inventory table! Please retry.\n')
    return

def donors_report4():
    cursor = conn.cursor()
    try:
        sql = "SELECT donor_id, f_name, l_name, bgroup FROM Donors"
        cursor.execute(sql)
        info = list(cursor)
        head = ['Donor id','First name', 'Last name', 'Blood group']
        print('\nPrinting Donor details:')
        print(tabulate(info, headers=head))
        csv_name = 'DON_'+datetime.today().strftime('%Y-%m-%d')+'.csv'
        with open(csv_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows([head]+info)
        print(f'\n... csv file *{csv_name}* saved. Returning to menu.\n')
    except:
            print('Some problem in Donors table! Please retry.\n')
    return

def manager_menu():
    print('*'*65)
    print('Welcome to the Manager homepage. Please select from options below')
    print('-'*65)
    while True:
        print('\nSelect -')
        print('Option 1 : Report all blood sample collections')
        print('Option 2 : Report all blood issue transactions')
        print('Option 3 : Report current blood inventory - ageing status')
        print('Option 4 : Report all donor details')
        print('Option 5 : Logout as manager')
        choice = input('\nEnter 1 / 2 / 3 / 4 / 5 as choice from above :')
        if choice == '1':
            samples_report1()
        elif choice == '2':
            issues_report2()
        elif choice == '3':
            inventory_report3()
        elif choice == '4':
            donors_report4()
        elif choice == '5':
            print('\n ******** Logging off as manager. Bye. \n')
            return

def executive_menu():
    print('*'*65)
    print('Welcome to the Executive homepage. Please select from options below')
    print('-'*65)
    while True:
        print('\nSelect -')
        print('Option 1 : Register a new donor')
        print('Option 2 : Record a new blood donation')
        print('Option 3 : Record a new demand for blood')
        print('Option 4 : Issue available matching blood for all pending demands')
        print('Option 5 : Logout as executive')
        choice = input('\nEnter 1 / 2 / 3 / 4 / 5 as choice from above :')
        if choice == '1':
            create_donor()
        elif choice == '2':
            collect_blood()
        elif choice == '3':
            create_demand()
        elif choice == '4':
            issue_blood()  
        elif choice == '5':
            print('\n ******** Logging off as executive. Bye. \n')
            return

def tester_menu():
    print('*'*65)
    print('Welcome to the Tester homepage. Please select from options below')
    print('-'*65)
    while True:
        print('\nSelect -')
        print('Option 1 : Test pending blood samples')
        print('Option 2 :  Check current blood inventory')
        print('Option 2 : Logout as tester')
        choice = input('\nEnter 1 / 2 / 3 as choice from above :')
        if choice == '1':
            test_blood()
        elif choice == '2':
            inventory_report3()
        elif choice == '3':
            print('\n ******** Logging off as tester. Bye. \n')
            return

authenticated = False
usr_role = login()
if usr_role == 'manager':
    manager_menu()
elif usr_role == 'executive':
    executive_menu()
elif usr_role == 'tester':
    tester_menu()
