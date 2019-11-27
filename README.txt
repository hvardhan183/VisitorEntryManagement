This is a Visitor Entry Management System made using Python GUI- Tkinter and sqlite3 created by hvardhan183
===========================REQUIREMENTS=====================

Python 3+
Modules:
	Tkinter (For GUI)
	sqlite3 (For connection with the datebase)
	smtplib (For sending Emails)
	twilio (For sending SMS)
		For sending SMS using twilio, you should have a twilio account with upgraded pack. I've checked this project using trial pack which can send SMS only to people registered with twilio. Using the twilio trial pack, you get a note "Twilio trial account." in the SMS.
Any Data-Base Browser for viewing the database

=========================ADDING DETAILS IN THE CODE===========

Before running the program, make sure you edit the details in the code with your credentials
In line 10: edit fromaddr to the mail ID from which you want to send the mails
In line 20: In Client the 1st parameter is your	ACCOUNT SID and 2nd is AUTH TOKEN from your twilio account
In line 60 & 108: The smtp server and port are updated based on your mail provider: For Gmail 'smtp.gmail.com' and port is 587;For Yahoo 'stmp.yahoo.mail.com' and port is 465
In line 62 & 110: Provide the password of the email account from which you want to send the mails. Make sure that APP access is given. You can go to the email account and update this in the settings.(Control access to less secure apps in GMAIL) 
In line 73 & 121: Update the from_= to your twilio number
Enter the details of the host in the database under the table hostDetails
hostDetails:
	hostName: Name of the host
	hostContact: Contact number of the host (without '+91')
	hostEmail: Email ID of the host
	hostAddress: Address of the host (Host's cabin or anything like that)

==========================WORKING==============================

After you run the file VisitorEntryManagement.py, you get a Main Menu with two options: ENTRY & EXIT
If the visitor is entering the office, choose ENTRY
if the visitor is exiting the office, choose EXIT
ENTRY:
	Once you choose ENTRY, you'll be directed to a form asking the details of the visitor
	Name:
	Contact:
	Email:
	Host:(Host refers to the person he would like to visit)
		A point to be noted here is that the details of the hosts have to put into the DATABASE under the Table hostDetails. I'm also attaching the database file with the name VisitorEntryManagement.db with 2 tables; Visitor and hostDetails
		Make sure you enter the details of all the hosts in the Table hostDetails.
	If the host exists(There is a host by the name requested by the visitor), then the host gets a mail and an SMS specifying the details of the Visitor and his check-in Time. You'll be directed to a page which gives the token number along with visitor details. This token number is given to the visitor and this token number refreshes everyday.(Token starts from 1 everyday) Here you redirect to the page you want (ENTRY, EXIT, MAINMENU) by clicking the button that specifies.
	If the host doesn't exist you get an error stating that Host not found.
EXIT:
	Once you choose EXIT, you'll be directed to a formasking for the token number and Name of the visitor
	If the token number corresponds to the visitor, then you get a Success message and the visitor gets an email and an SMS stating the details of his visit.
	If the token number doesn't match you get an error message.

The working of the code is explicitly mentioned in the code with comments
=========================================================================================


