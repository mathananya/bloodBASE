from datetime import datetime
import mysql.connector

conn = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    password = '1ismynumber',
    database = 'db_bloodbase')

def find_all_tables(conn):
    cursor = conn.cursor()
    cursor.execute('SELECT name FROM sys.tables')
    table_list = []
    for row in cursor:
        print('\nrow = %r' % row)
        print('Table name = %s' %row[0])
        table_list.append(row[0])
    cursor.close()
    return table_list

def show_table_details(conn, table_list):
    cursor = conn.cursor()
    for table in table_list:
        print('\nTable name = %s' %table)
        cursor.execute(f'SELECT * FROM {table}')
        for row in cursor.fetchall():
            print(row)
        print()
    cursor.close()
    return

def create_tables(conn):
    cursor = conn.cursor()
    
    cursor.execute("DROP TABLE IF EXISTS Users;")
    cursor.execute('''
       CREATE TABLE Users (
       user_id nvarchar(20) primary key,
       user_pwd nvarchar(20),
       user_type nvarchar(15)
       )'''
   )
    cursor.execute('''
        INSERT INTO Users (user_id, user_pwd, user_type) VALUES
        ('user1','manager','manager'),
        ('user2','executive','executive'),
        ('user3','tester','tester')
        '''
    )


    cursor.execute("DROP TABLE IF EXISTS Donors;")
    cursor.execute('''CREATE TABLE Donors (
        donor_id nvarchar(10) primary key,
        f_name nvarchar(15),
        l_name nvarchar(15),
        dob date,
        address nvarchar(50),
        email nvarchar(30),
        phone nvarchar(10),
        bgroup nvarchar(10)
        )'''
    )
    cursor.execute('''
        INSERT INTO Donors (donor_id, f_name, l_name, dob, address, email, phone, bgroup) VALUES
        ('DR1','Ananya','Muk','2000-01-01','Noida Espacia','ananya@mail.com','9999 9999','B+')
        '''
    )


    cursor.execute("DROP TABLE IF EXISTS Collections;")
    cursor.execute('''
        CREATE TABLE Collections (
        coll_id nvarchar(10) primary key,
        coll_time datetime,
        donor_id nvarchar(10),
        units int
        )'''
    )    
    cursor.execute("DROP TABLE IF EXISTS Samples;")
    cursor.execute('''
        CREATE TABLE Samples (
        coll_id nvarchar(10) primary key,
        test_time datetime,
        btype nvarchar(10),
        result int
        )'''
    )
    cursor.execute(f'''
        INSERT INTO Collections (coll_id, coll_time, donor_id, units) VALUES
        ('CL1','2024-08-25 18:08:03','DR1',3)
        '''
    )
    cursor.execute(f'''
        INSERT INTO Samples (coll_id) VALUES ('CL1')
        '''
    )


    cursor.execute("DROP TABLE IF EXISTS Rejections;")
    cursor.execute('''
        CREATE TABLE Rejections (
        coll_id nvarchar(10) primary key,
        time datetime,
        units int
        )'''
    )

    cursor.execute("DROP TABLE IF EXISTS Inventory;")
    cursor.execute('''
        CREATE TABLE Inventory (
        coll_id nvarchar(10) primary key,
        units int
        )'''
    )


    cursor.execute("DROP TABLE IF EXISTS Expiries;")
    cursor.execute('''
        CREATE TABLE Expiries (
        coll_id nvarchar(10) primary key,
        time datetime,
        units int
        )'''
    )

    cursor.execute("DROP TABLE IF EXISTS Demand;")
    cursor.execute('''
        CREATE TABLE Demand (
        demand_id nvarchar(10) primary key,
        patient_id nvarchar(10),
        type nvarchar(10),
        units int,
        time datetime,
        status nvarchar(10)
        )'''
    )

    cursor.execute("DROP TABLE IF EXISTS Issues;")
    cursor.execute('''
        CREATE TABLE Issues (
        demand_id nvarchar(10) primary key,
        units int,
        issue_time datetime
        )'''
    )

    cursor.execute("DROP TABLE IF EXISTS Inv_Issue;")
    cursor.execute('''
        CREATE TABLE Inv_Issue (
        coll_id nvarchar(10),
        demand_id nvarchar(10),
        units int
        )'''
    )

    cursor.close()
    return


def check_issues(conn):
    print('\n Script to check issues against demands')
    cursor = conn.cursor()
    sql = "SELECT demand_id, units, status FROM Demand"
    cursor.execute(sql)
    rows = cursor.fetchall()
    for row in rows:
        dmid = row[0]
        dm_units = row[1]
        dm_status = row[2]
        sql = "SELECT COALESCE(SUM(units),0) FROM Inv_Issue WHERE demand_id = ?"
        cursor.execute(sql,dmid)
        units_issued = cursor.fetchone()[0]
        print(f'Demand {dmid} : units demanded {dm_units}, issued {units_issued}, status {dm_status}')
    cursor.close()
    return

    
create_tables(conn)
#check_issues(conn)
show_table_details(conn,['Users','Donors','Collections','Inventory','Demand'])
conn.commit()
conn.close()
