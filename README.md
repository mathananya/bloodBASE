# bloodBASE
#### A centralised blood bank management system to support the smooth and efficient functioning of blood banks across cities and towns.
  

## Introduction
Blood is an extremely valuable resource that needs to managed very carefully. Many peoples lives depend on the its timely and efficient availability and supply.
In modern society, one of the most wonderful achievements is the setup of a system by which ordinary citizens (if medically fit) can donate blood for other citizens who are in need of blood transfusion. This system saves many lives in times of catastrophe and during normal medical procedures and emergencies.  
  
A blood bank is usually a dedicated clinic or department of a hospital, within a clinical pathology laboratory where the storage of blood product occurs and where pre-transfusion and blood compatibility testing is performed. Blood donors (ordinary citizens) arrive at the blood bank to donate blood, but mobile camps are also sometimes set up for blood collection drives.  
  
Blood products are perishable and needs to be handled very carefully. Transfusion of the wrong blood type causes serious medical complications for the receiver.  The processing, testing, handling and transportation of blood products needs to be recorded very carefully, so that full traceability exists thereby ensuring safety. Relational databases are the ideal software platform to keep such records.  
  
We shall be creating a centralised blood bank database where all records of blood products shall be kept with full details that record its complete traceability – from donor to recipient. The system shall also ensure management of blood product inventory ensuring minimal wastage due to expiry, while ensuring that all expired blood product units are safely disposed.  

## Features
1. Main features of the blood bank system shall include
2. A full-scale relational database (MySQL from Oracle) to store data
3. A python program to provide the user front-end to manage the regular blood bank transactions (such as blood collection, blood test, blood issue, blood disposal)
4. User authentication and password based security for multiple user access
5. A database schema that shall be normalised to ensure complete consistency across tables. Multiple tables with foreign key joins that ensure no duplication of data storage.
6. Ensure that any unit of blood has complete traceability across all operations. Audit trail features.
7. Business reports for daily transactions at the blood bank
8. Business reports for inventory levels with blood product group details.
9. Business reports for ageing analysis.
10. Automated checks for blood product inventory levels, with warning notifications for manager.
11. Automated checks for blood product inventory expired, with disposal of products by manager. Different blood products have different durations for expiry - Red blood cells (42 days), Plasma (1 year), and Platelets (5 days).
12. Ensures that minimal blood is disposed/wasted due to expiration. System automatically tries to issue the oldest permissible units that are in the inventory using a FIFO logic.

## Validations and checks
- Several validations and checks must be ensured:
- Validate the right person is accessing the system.
- Validate that transactions are available to the user based on their role.
- Validate that the system does not store duplicate or inconsistent data. 
- Every unit of data is uniquely identified – validate no duplicates in identifier key.
- Every unit of blood product is fully traceable from donation to transfusion / expiry. Validate no data is missing.
- Blood product inventory of any type cannot be negative. Check sufficient inventory before issue of blood.
- The inventory of blood product cannot exceed overall blood storage capacity of the blood bank. Check storage availability before accepting blood donation.
- Check issue of right blood group for any requirement.
- Check the first-in-first-out (FIFO) policy, so that oldest blood collected is issued first.
- Check blood unit expiry date before issuing. Blood products have different durations of expiry - Red blood cells (42 days), Plasma (1 year), and Platelets (5 days).
- Validate that donor age is over 18 years.

## Project Flow Diagram
<p align="center">
<img width="700" alt="image" src="https://github.com/user-attachments/assets/c25dd3bf-ec73-4ef3-956c-3d04af79a3f5" />
</p>

## Project Flow Details

- The blood bank manager logs in with his/her credentials.
  - 3 Reports are available to see the status of blood bank inventory. SQL queries are triggered in the back-end to fetch the latest data for each report. The data is formatted in tables and presented on the user-interface/screen.
  - Choosing report 1 shows the details of all the transactions that have happened over the last 3 days
  - Choosing report 2 shows the details of the current inventory of blood units as per blood group
  - Choosing report 3 shows the ageing analysis of the current inventory of blood units including the units that have expired. The manager is given an option to dispose the expired inventory units. If confirmed, the updates are made to the inventory table in the database.
  
- The blood bank executive logs in with his/her credentials.
  - 3 Transactions are available - Blood collection, Send for tests, and Blood issue.
  - Choosing transaction 1 (blood collection) will open UI where the details of the blood donor, the time-stamp, and the quantity of blood will be captured. If it is a new donor, Specific validations such as age, and unique Aadhaar id will be done before confirming that the entry has been posted in the donors table of the database. Donation details will be written in donation table after a validation that storage capacity is available.
  - Choosing transaction 2 (send for tests) will open UI where the details of all blood donations pending testing will be shown. All/some of the blood units can be dispatched for testing with the timestamp being captured. Updates will be made to the respective tables in the database.
  - Choosing transaction 3 (blood issue) will open an UI where the details of any new patient will be captured, with validation of unique adhaar. Based on quantity of specific/blood group requirement, a check of inventory will be done to find the oldest units of blood that match, but within the expiry date. The units (up to desired quantity) will be issued and the inventory table will be updated.
  
- The blood tester logs in with his / her credentials
  - The UI shows a list of samples that are awaiting testing. The tester performs the necessary lab tests and updates the results on the system.
  - The updates can be made using various options – Pass all samples, Fail all samples, Select samples to pass, Select samples to fail
  - The inventory table is updated in the database according to the samples that are passed.
  - The samples that are failed are updated in the sample_failure table with details of failure reason

## Results
### PERSONA : MANAGER 
```
*****************************************************************
Welcome to Bloodbase - the Blood Bank Database Management System
-----------------------------------------------------------------
What is your user id? user1
What is your password? 
Password did not match! Please retry.

What is your user id? user1
What is your password? 
Success user1. You are logged in now as manager.

*****************************************************************
Welcome to the Manager homepage. Please select from options below
-----------------------------------------------------------------

Select -
Option 1 : Report all blood sample collections
Option 2 : Report all blood issue transactions
Option 3 : Report current blood inventory - ageing status
Option 4 : Report all donor details
Option 5 : Logout as manager

Enter 1 / 2 / 3 / 4 / 5 as choice from above :1

Printing Collection Details:
Collection id    Collection Date-time        Donor id    Blood group      Units
---------------  --------------------------  ----------  -------------  -------
CL1              2024-08-25 18:08:03         DR1         B+                   3
CL10             2024-11-03 23:23:35.727000  DR1         B+                   3
CL11             2024-11-04 01:21:43.090000  DR3         B-                   3
CL12             2024-11-09 19:43:56.957000  DR1         B+                   4
CL2              2024-08-25 21:17:34.753000  DR2         O-                   4
CL3              2024-08-27 22:50:54.597000  DR1         B+                   5
CL4              2024-08-27 22:55:00.300000  DR3         B-                   1
CL5              2024-08-27 23:02:07.540000  DR2         O-                   1
CL6              2024-11-03 17:05:12.153000  DR3         B-                   4
CL7              2024-11-03 17:42:08.977000  DR4         B+                   3
CL8              2024-11-03 17:43:41.253000  DR2         O-                   3
CL9              2024-11-03 22:07:14.943000  DR1         B+                   4

... csv file *COL_2024-12-27.csv* saved. Returning to manager menu.


Select -
Option 1 : Report all blood sample collections
Option 2 : Report all blood issue transactions
Option 3 : Report current blood inventory - ageing status
Option 4 : Report all donor details
Option 5 : Logout as manager

Enter 1 / 2 / 3 / 4 / 5 as choice from above :3

Printing Inventory details:
Collection id    Blood type      Units left  Collection date-time
---------------  ------------  ------------  --------------------------
CL12             RbcB+                    2  2024-11-09 19:43:56.957000
CL6              RbcB-                    4  2024-11-03 17:05:12.153000

... csv file *INV_2024-12-27.csv* saved. Returning to menu.


Select -
Option 1 : Report all blood sample collections
Option 2 : Report all blood issue transactions
Option 3 : Report current blood inventory - ageing status
Option 4 : Report all donor details
Option 5 : Logout as manager

Enter 1 / 2 / 3 / 4 / 5 as choice from above :4

Printing Donor details:
Donor id    First name    Last name    Blood group
----------  ------------  -----------  -------------
DR1         Ananya        Muk          B+
DR2         Ani           Mukherjee    O-
DR3         Ra            Mukh         B-
DR4         Pavni         Sethia       B+

... csv file *DON_2024-12-27.csv* saved. Returning to menu.


Select -
Option 1 : Report all blood sample collections
Option 2 : Report all blood issue transactions
Option 3 : Report current blood inventory - ageing status
Option 4 : Report all donor details
Option 5 : Logout as manager

Enter 1 / 2 / 3 / 4 / 5 as choice from above :5

 ******** Logging off as manager. Bye.
```

### PERSONA : EXECUTIVE 
```
*****************************************************************
Welcome to Bloodbase - the Blood Bank Database Management System
-----------------------------------------------------------------
What is your user id? user2
What is your password? 
Success user2. You are logged in now as executive.


*****************************************************************
Welcome to the Executive homepage. Please select from options below
-----------------------------------------------------------------

Select -
Option 1 : Register a new donor
Option 2 : Record a new blood donation
Option 3 : Record a new demand for blood
Option 4 : Issue available matching blood for all pending demands
Option 5 : Logout as executive

Enter 1 / 2 / 3 / 4 / 5 as choice from above :1

Creating new donor - Please enter details below
First Name: John
Last Name: Galt
DoB as YYYY-MM-DD: 2001-01-31
Address: Bluestone Apartment, Noida Sector 93
Email id: john.galt@email.com
Phone no: 9999-8888
Blood group A+/A-/B+/B-/AB+/AB-/O+/O-: O+

Successfully created new donor with a Donor ID = DR5 ****

Select -
Option 1 : Register a new donor
Option 2 : Record a new blood donation
Option 3 : Record a new demand for blood
Option 4 : Issue available matching blood for all pending demands
Option 5 : Logout as executive

Enter 1 / 2 / 3 / 4 / 5 as choice from above :2

Welcome to blood donation station. Please provide your registered Donor id (format DRx): DR3
Hi Ra. THANK YOU for your donation.
Your blood group is registered as B-.
This collection has id CL13. We are confirming number of units donated today (enter integer) :5

Successfully created new collection with a Collection ID = CL13 ****
A sample of this collection has been successfully registered for testing.


Select -
Option 1 : Register a new donor
Option 2 : Record a new blood donation
Option 3 : Record a new demand for blood
Option 4 : Issue available matching blood for all pending demands
Option 5 : Logout as executive

Enter 1 / 2 / 3 / 4 / 5 as choice from above :3
Please enter a valid patient id :121212
Please enter a valid blood type from list ['Platelet', 'RbcA+', 'RbcA-', 'RbcB+', 'RbcB-', 'RbcAB+', 'RbcAB-', 'RbcO+', 'RbcO-', 'PlsA+', 'PlsA-', 'PlsB+', 'PlsB-', 'PlsAB+', 'PlsAB-', 'PlsO+', 'PlsO-']: RbcB-
Please enter number of units needed: 4

Successfully created new demand with a Demand ID = DM11 ****

Select -
Option 1 : Register a new donor
Option 2 : Record a new blood donation
Option 3 : Record a new demand for blood
Option 4 : Issue available matching blood for all pending demands
Option 5 : Logout as executive

Enter 1 / 2 / 3 / 4 / 5 as choice from above :4

New demand DM11 for 4 units of type RbcB-:
Inv_Issue of 4 units from CL6
For demand id DM11, a total of 4 units is issued.

Select -
Option 1 : Register a new donor
Option 2 : Record a new blood donation
Option 3 : Record a new demand for blood
Option 4 : Issue available matching blood for all pending demands
Option 5 : Logout as executive

Enter 1 / 2 / 3 / 4 / 5 as choice from above :5

 ******** Logging off as executive. Bye.
```
### PERSONA : TESTER
```
 *****************************************************************
Welcome to Bloodbase - the Blood Bank Database Management System
-----------------------------------------------------------------
What is your user id? user3
What is your password?
Success user3. You are logged in now as tester.

*****************************************************************
Welcome to the Tester homepage. Please select from options below
-----------------------------------------------------------------

Select -
Option 1 : Test pending blood samples
Option 2 :  Check current blood inventory
Option 3 : Logout as tester

Enter 1 / 2 / 3 as choice from above :1

We have 3 pending testing. Please enter the id from list below :
['CL11', 'CL13', 'CL7']
Enter the id (in format CLx) chosen from list above :CL13
Confirm blood group from list ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'] :B-
Enter the result of the test for chosen sample id CL13 below.
Enter y/n for whether sample passed all screening checks :y

Test result ** y ** updated in database at time 2024-12-28 00:26:50.593558.

Successfully updated inventory with batch of 5 units ****

Testing done. Returning to menu.

Select -
Option 1 : Test pending blood samples
Option 2 :  Check current blood inventory
Option 3 : Logout as tester

Enter 1 / 2 / 3 as choice from above :2

Printing Inventory details:
Collection id    Blood type      Units left  Collection date-time
---------------  ------------  ------------  --------------------------
CL12             RbcB+                    2  2024-11-09 19:43:56.957000
CL13             RbcB-                    5  2024-12-27 23:58:56.210000

... csv file *INV_2024-12-28.csv* saved. Returning to menu.


Select -
Option 1 : Test pending blood samples
Option 2 :  Check current blood inventory
Option 3 : Logout as tester

Enter 1 / 2 / 3 as choice from above :3

 ******** Logging off as tester. Bye.
```
### PERSONA : MANAGER 
```
*****************************************************************
Welcome to Bloodbase - the Blood Bank Database Management System
-----------------------------------------------------------------
What is your user id? user1
What is your password? 
Success user1. You are logged in now as manager.

*****************************************************************
Welcome to the Manager homepage. Please select from options below
-----------------------------------------------------------------

Select -
Option 1 : Report all blood sample collections
Option 2 : Report all blood issue transactions
Option 3 : Report current blood inventory - ageing status
Option 4 : Report all donor details
Option 5 : Logout as manager

Enter 1 / 2 / 3 / 4 / 5 as choice from above :1

Printing Collection Details:
Collection id    Collection Date-time        Donor id    Blood group      Units
---------------  --------------------------  ----------  -------------  -------
CL1              2024-08-25 18:08:03         DR1         B+                   3
CL10             2024-11-03 23:23:35.727000  DR1         B+                   3
CL11             2024-11-04 01:21:43.090000  DR3         B-                   3
CL12             2024-11-09 19:43:56.957000  DR1         B+                   4
CL13             2024-12-27 23:58:56.210000  DR3         B-                   5
CL2              2024-08-25 21:17:34.753000  DR2         O-                   4
CL3              2024-08-27 22:50:54.597000  DR1         B+                   5
CL4              2024-08-27 22:55:00.300000  DR3         B-                   1
CL5              2024-08-27 23:02:07.540000  DR2         O-                   1
CL6              2024-11-03 17:05:12.153000  DR3         B-                   4
CL7              2024-11-03 17:42:08.977000  DR4         B+                   3
CL8              2024-11-03 17:43:41.253000  DR2         O-                   3
CL9              2024-11-03 22:07:14.943000  DR1         B+                   4

... csv file *COL_2024-12-28.csv* saved. Returning to manager menu.


Select -
Option 1 : Report all blood sample collections
Option 2 : Report all blood issue transactions
Option 3 : Report current blood inventory - ageing status
Option 4 : Report all donor details
Option 5 : Logout as manager

Enter 1 / 2 / 3 / 4 / 5 as choice from above :2

Printing Issuing Details:
Demand id    Blood type      Demanded units    Issued units  Issuing Date-time
-----------  ------------  ----------------  --------------  --------------------------
DM1          PlsO-                        2               0  2024-11-03 14:54:00
DM10         RbcB+                        2               2  2024-11-09 19:54:37
DM11         RbcB-                        4               4  2024-12-28 00:24:13
DM2          RbcO-                        2               1  2024-11-03 14:54:00
DM3          RbcB+                        2               0  2024-11-03 14:54:00
DM6          RbcB+                        3               3  2024-11-03 22:12:15
DM7          RbcB+                        3               2  2024-11-03 22:55:07
DM8          RbcB+                        2               0  2024-11-03 23:24:54
DM9          RbcB+                        4               3  2024-11-03 23:27:53

... csv file *ISS_2024-12-28.csv* saved. Returning to manager menu.


Select -
Option 1 : Report all blood sample collections
Option 2 : Report all blood issue transactions
Option 3 : Report current blood inventory - ageing status
Option 4 : Report all donor details
Option 5 : Logout as manager

Enter 1 / 2 / 3 / 4 / 5 as choice from above :3

Printing Inventory details:
Collection id    Blood type      Units left  Collection date-time
---------------  ------------  ------------  --------------------------
CL12             RbcB+                    2  2024-11-09 19:43:56.957000
CL13             RbcB-                    5  2024-12-27 23:58:56.210000

... csv file *INV_2024-12-28.csv* saved. Returning to menu.


Select -
Option 1 : Report all blood sample collections
Option 2 : Report all blood issue transactions
Option 3 : Report current blood inventory - ageing status
Option 4 : Report all donor details
Option 5 : Logout as manager

Enter 1 / 2 / 3 / 4 / 5 as choice from above :4

Printing Donor details:
Donor id    First name    Last name    Blood group
----------  ------------  -----------  -------------
DR1         Ananya        Muk          B+
DR2         Ani           Mukherjee    O-
DR3         Ra            Mukh         B-
DR4         Pavni         Sethia       B+
DR5         John          Galt         O+

... csv file *DON_2024-12-28.csv* saved. Returning to menu.


Select -
Option 1 : Report all blood sample collections
Option 2 : Report all blood issue transactions
Option 3 : Report current blood inventory - ageing status
Option 4 : Report all donor details
Option 5 : Logout as manager

Enter 1 / 2 / 3 / 4 / 5 as choice from above :5

 ******** Logging off as manager. Bye.
```
### MANAGEMENT REPORTS (CSV FILES)
```
DONOR FILE: DON_2024-12-28.csv

Donor id,First name,Last name,Blood group
DR1,Ananya,Muk,B+
DR2,Ani,Mukherjee,O-
DR3,Ra,Mukh,B-
DR4,Pavni,Sethia,B+
DR5,John,Galt,O+


COLLECTIONS FILE: COL_2024-12-28.csv

Collection id,Collection Date-time,Donor id,Blood group,Units
CL1,2024-08-25 18:08:03,DR1,B+,3
CL10,2024-11-03 23:23:35.727000,DR1,B+,3
CL11,2024-11-04 01:21:43.090000,DR3,B-,3
CL12,2024-11-09 19:43:56.957000,DR1,B+,4
CL13,2024-12-27 23:58:56.210000,DR3,B-,5
CL2,2024-08-25 21:17:34.753000,DR2,O-,4
CL3,2024-08-27 22:50:54.597000,DR1,B+,5
CL4,2024-08-27 22:55:00.300000,DR3,B-,1
CL5,2024-08-27 23:02:07.540000,DR2,O-,1
CL6,2024-11-03 17:05:12.153000,DR3,B-,4
CL7,2024-11-03 17:42:08.977000,DR4,B+,3
CL8,2024-11-03 17:43:41.253000,DR2,O-,3
CL9,2024-11-03 22:07:14.943000,DR1,B+,4


ISSUES FILE: ISS_2024-12-28.csv

Demand id,Blood type,Demanded units,Issued units,Issuing Date-time
DM1,PlsO-,2,0,2024-11-03 14:54:00.627000
DM10,RbcB+,2,2,2024-11-09 19:54:37.690000
DM11,RbcB-,4,4,2024-12-28 00:24:13.930000
DM2,RbcO-,2,1,2024-11-03 14:54:00.637000
DM3,RbcB+,2,0,2024-11-03 14:54:00.640000
DM6,RbcB+,3,3,2024-11-03 22:12:15.860000
DM7,RbcB+,3,2,2024-11-03 22:55:07.473000
DM8,RbcB+,2,0,2024-11-03 23:24:54.797000


INVENTORY FILE: INV_2024-12-28.csv

Collection id,Blood type,Units left,Collection date-time
CL12,RbcB+,2,2024-11-09 19:43:56.957000
CL13,RbcB-,5,2024-12-27 23:58:56.210000
```
