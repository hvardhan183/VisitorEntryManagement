#imports
from tkinter import *
from tkinter import messagebox as ms
import sqlite3
import smtplib
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from twilio.rest import Client
fromaddr = "xxx@example.com" #Enter the mail ID from which you want to send mails

# make a table Visitor at the beginning if it doesn't exist
# You must create a table hostDetails beforehand in VisitorEntryManagement.db database
with sqlite3.connect('VistorEntryManagement.db') as db: #connect to database
    c = db.cursor()
    #below is the sql statement to create the table
    c.execute('CREATE TABLE IF NOT EXISTS Visitor (visitID INTEGER PRIMARY KEY AUTOINCREMENT, visitorName TEXT NOT NULL ,visitorContact TEXT NOT NULL,visitorEmail TEXT NOT NULL,visitDate TEXT NOT NULL ,entryTime TEXT NOT NULL,exitTime TEXT NOT NULL,host TEXT NOT NULL);')
    db.commit()

client = Client("ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx") #1st parameter is your ACCOUNT SID and 2nd is AUTH TOKEN from your twilio account
#Main Class
class main:
    def __init__(self,master):
    	# Window 
        self.master = master
        #Some Useful variables
        self.visitID = StringVar()
        self.visitorName = StringVar()
        self.visitorContact = StringVar()
        self.visitorEmail = StringVar()
        self.IDNew=StringVar()
        self.exitName=StringVar()
        self.host = StringVar()
        self.token=int()
        #Create Widgets
        self.widgets()

    #Entry Function            
    def visitEntry(self):
        if self.visitorName.get()=='' or self.visitorContact.get()=='' or self.visitorEmail.get()=='' or self.host.get()=='': #If the entries are blank show an error
            ms.showerror('Oops!','Enter all the Details')
        else:
            #Establish Connection
            with sqlite3.connect('VistorEntryManagement.db') as db:
            c = db.cursor()
            c.execute('''SELECT hostEmail, hostContact FROM hostDetails WHERE hostName=?''',[self.host.get()]) #Check if the host exists; If exists get the host's contact and mail
            h=c.fetchone()
            if h: #If hosts exists
                hMail=h[0] #host's mail Id
                hNum=h[1] #host's contact number
                insert = 'INSERT INTO Visitor(visitorName ,visitorContact ,visitorEmail ,visitDate ,entryTime,exitTime,host) VALUES(?,?,?,?,?,?,?)' #sql query statement
                date='{:%d-%m-%Y}'.format(datetime.datetime.now()) #Current date
                time='{:%H:%M:%S}'.format(datetime.datetime.now()) #Current time
                c.execute(insert,[(self.visitorName.get()),(self.visitorContact.get()),(self.visitorEmail.get()),(date),(time),'0',(self.host.get())]) #Insert the details of the visitor into the database 
                find_user = ('SELECT COUNT(*) FROM Visitor WHERE visitDate=?') #Sql query for number of visitors on the particular day
                c.execute(find_user,['{:%d-%m-%Y}'.format(datetime.datetime.now())])
                row=c.fetchone()
                self.token=row[0] #token given to visitor
                #Starting the smtp server
                server = smtplib.SMTP('xxx.example.com', xxx) #For Gmail 'smtp.gmail.com' and port is 587; For Yahoo 'stmp.yahoo.mail.com' and port is 465
                server.starttls()
                server.login(fromaddr, "password") #Replace password with your mail password
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = hMail
                msg['Subject'] = "Visitor Details: "+self.visitorName.get() #Subject of the mail
                body1 = 'Name of the visitor: '+self.visitorName.get()+'\nContact No: '+self.visitorContact.get()+'\nEmail: '+self.visitorEmail.get()+'\nCheck-in Time: '+'{:%H:%M:%S}'.format(datetime.datetime.now()) #body of the mail
                msg.attach(MIMEText(body1, 'plain'))
                text = msg.as_string()
                server.sendmail(fromaddr,hMail, text) #send mail
                server.quit() #stop the server
                phone="+91"+hNum #Adding country Code '+91' for India
                client.messages.create(to=phone, from_="+XXXXXXXXXX", body=body1) #Update this with your twilio number
                ms.showinfo('Success!','Entry Granted') #Success message
                self.info()
            else: #If host doesn't exist Error is displayed
                ms.showerror('Oops!','Host Not Found.')
            db.commit()

    #Exit function
    def visitExit(self):
        check=self.IDNew.get()
        ck=check.isdigit() #check if the token is digit
        if self.IDNew.get()=='' or self.exitName.get()=='' or ck==False: #If the entries are blank or token is not a number show an error
            ms.showerror('Oops!','Enter all the Details!')
        else:
            #Establish Connection
            with sqlite3.connect('VistorEntryManagement.db') as db:
                c=db.cursor()
            find_user = ('SELECT COUNT(*) FROM Visitor WHERE NOT visitDate=?') #sql query for visitors who haven't visited on the following day
            c.execute(find_user,['{:%d-%m-%Y}'.format(datetime.datetime.now())])
            row=c.fetchone()
            name=int(self.IDNew.get())+row[0] #Actual visitID of the visitor
            find = ('SELECT visitorEmail,visitorContact,entryTime,host FROM Visitor WHERE visitID=? AND visitorName=? AND exitTime=?') #Find if the visitor name and token match; If matched get the details
            c.execute(find,[(name),(self.exitName.get()),0])
            v=c.fetchone()
            if v: #Name and token matched 
                time='{:%H:%M:%S}'.format(datetime.datetime.now()) #Current time
                c.execute('''UPDATE Visitor SET exitTime=? WHERE visitID=?''', (time,int(name))) #Update exitTime of the visitor
                vMail=v[0] #Visitor's mail ID
                vNum=v[1] #Visitor contact number
                vEntryTime=v[2] #Check-in Time
                vHost=v[3] #host
                c.execute('''SELECT hostAddress FROM hostDetails WHERE hostName=?''',[vHost]) #Get the host details
                a=c.fetchone()
                Add=a[0] #Host address
                #Starting the smtp server
                server = smtplib.SMTP('xxx.example.com', xxx) #For Gmail 'smtp.gmail.com' and port is 587; For Yahoo 'stmp.yahoo.mail.com' and port is 465
                server.starttls()
                server.login(fromaddr, "password") #Replace password with your mail password
                msg = MIMEMultipart()
                msg['From'] = fromaddr
                msg['To'] = vMail
                msg['Subject'] = "Visit Details of the visit to "+vHost #subject of the mail
                body1 = 'Name: '+self.exitName.get()+'\nContact No: '+vNum+'\nVisit Date: '+'{:%d-%m-%Y}'.format(datetime.datetime.now())+'\nCheck-in Time: '+vEntryTime+'\nCheck-out Time: '+'{:%H:%M:%S}'.format(datetime.datetime.now())+'\nHost Name: '+vHost+'\nAddress Visited: '+Add #body of the mail
                msg.attach(MIMEText(body1, 'plain'))
                text = msg.as_string()
                server.sendmail(fromaddr, vMail, text) #send mail
                server.quit() #stop the server
                phone="+91"+vNum #add Country Code ; '+91' for India
                client.messages.create(to=phone, from_="+XXXXXXXXXX", body=body1) #Update this with your twilio number
                ms.showinfo('Success','Thanks for visiting') #Show success message
                self.log()
            else: #Token and name not matched
                ms.showerror('Oops!','Invalid Details!')
            db.commit()
            
    def info(self): #For giving the details of the visitor (Token number)
        self.head['text'] = 'Entry Granted'
        Label(self.infof,text='Token No: '+str(self.token),font = ('Courier',20),pady=5,padx=5,bg="white",fg="black").pack(side=TOP)
        Label(self.infof,text='Name of the visitor: '+self.visitorName.get(),font = ('Courier',20),pady=5,padx=5,bg="white",fg="black").pack(side=TOP)
        Label(self.infof,text='Contact No: '+self.visitorContact.get(),font = ('Courier',20),pady=5,padx=5,bg="white",fg="black").pack(side=TOP)
        Label(self.infof,text='Email: '+self.visitorEmail.get(),font = ('Courier',20),pady=5,padx=5,bg="white",fg="black").pack(side=TOP)
        self.mainf.pack_forget()
        self.logf.pack_forget()
        self.mainf.pack_forget()
        self.infof.pack()
    def log(self): #Entry page
        self.visitorName.set('')
        self.visitorContact.set('')
        self.visitorEmail.set('')
        self.host.set('')
        self.crf.pack_forget()
        self.infof.pack_forget()
        self.mainf.pack_forget()
        self.head['text'] = 'ENTRY'
        self.logf.pack()
    def cr(self): #Exit Page
        self.visitID.set('0')
        self.head['text'] = 'EXIT'
        self.logf.pack_forget()
        self.infof.pack_forget()
        self.mainf.pack_forget()
        self.crf.pack()
    def mainMenu(self): #Main Menu
        self.head['text']='VISITOR ENTRY MANAGEMENT'
        self.logf.pack_forget()
        self.infof.pack_forget()
        self.crf.pack_forget()
        self.mainf.pack()
    def widgets(self): #Widgets
        self.head = Label(self.master,text = 'VISITOR ENTRY MANAGEMENT',font=('Courier', 35, 'bold italic'),pady = 10,bg="white",fg="black")
        self.head.pack()

        #Main Menu
        self.mainf = Label(self.master,font = ('Courier',35),pady = 10,bg="white",fg="black")
        Button(self.mainf,text = 'ENTRY',bd = 3 ,font = ('Courier',15),padx=5,pady=5,command=self.log,bg="#00a500",fg="white").grid()
        Button(self.mainf,text = 'EXIT',bd = 3 ,font = ('Courier',15),padx=5,pady=5,command=self.cr,bg="#00a500",fg="white").grid(row=0,column=1)
        self.mainf.pack()

        #Entry Page
        self.logf = Frame(self.master,padx =10,pady = 10,bg="white")
        Label(self.logf,text = 'Name: ',font = ('Courier',20, 'italic'),pady=5,padx=5,bg="white",fg="black").grid(sticky = W)
        Entry(self.logf,textvariable = self.visitorName,bd = 5,font = ('Courier',15)).grid(row=0,column=1)
        Label(self.logf,text = 'Contact: ',font = ('Courier',20, 'italic'),pady=5,padx=5,bg="white",fg="black").grid(sticky = W)
        Entry(self.logf,textvariable = self.visitorContact,bd = 5,font = ('Courier',15)).grid(row=1,column=1)
        Label(self.logf,text = 'Email: ',font = ('Courier',20, 'italic'),pady=5,padx=5,bg="white",fg="black").grid(sticky = W)
        Entry(self.logf,textvariable = self.visitorEmail,bd = 5,font = ('Courier',15)).grid(row=2,column=1)
        Label(self.logf,text = 'Host: ',font = ('Courier',20, 'italic'),pady=5,padx=5,bg="white",fg="black").grid(sticky = W)
        Entry(self.logf,textvariable = self.host,bd = 5,font = ('Courier',15)).grid(row=3,column=1)
        Button(self.logf,text = 'ENTER',bd = 3 ,font = ('Courier',15),padx=5,pady=5,command=self.visitEntry,bg="#00a500",fg="white").grid()
        Button(self.logf,text = 'GO TO EXIT',bd = 3 ,font = ('Courier',15),padx=5,pady=5,command=self.cr,bg="#00a500",fg="white").grid(row=4,column=1)
        Button(self.logf,text = 'GO TO MAIN MENU',bd = 3 ,font = ('Courier',15),padx=5,pady=5,command=self.mainMenu,bg="#00a500",fg="white").grid(row=4,column=2)
        
        #Exit Page
        self.crf = Frame(self.master,padx =10,pady = 10,bg="white")
        Label(self.crf,text = 'Token No: ',font = ('Courier',20, 'italic'),pady=5,padx=5,bg="white",fg="black").grid(sticky = W)
        Entry(self.crf,textvariable = self.IDNew,bd = 5,font = ('Courier',15)).grid(row=0,column=1)
        Label(self.crf,text = 'Name: ',font = ('Courier',20, 'italic'),pady=5,padx=5,bg="white",fg="black").grid(sticky = W)
        Entry(self.crf,textvariable = self.exitName,bd = 5,font = ('Courier',15)).grid(row=1,column=1)
        Button(self.crf,text = 'EXIT',bd = 3 ,font = ('Courier',15),padx=5,pady=5,command=self.visitExit,bg="#00a500",fg="white").grid()
        Button(self.crf,text = 'GO TO ENTRY',bd = 3 ,font = ('Courier',15),padx=5,pady=5,command=self.log,bg="#00a500",fg="white").grid(row=2,column=1)
        Button(self.crf,text = 'GO TO MAIN MENU',bd = 3 ,font = ('Courier',15),padx=5,pady=5,command=self.mainMenu,bg="#00a500",fg="white").grid(row=2,column=2)
       
        #Info Page
        self.infof = Frame(self.master,bg="white")
        Button(self.infof,text = 'GO TO ENTRY',bd = 3 ,font = ('Courier',15),padx=0,pady=5,width=30,command=self.log,bg="#00a500",fg="white").pack(side=BOTTOM)
        Button(self.infof,text = 'GO TO EXIT',bd = 3 ,font = ('Courier',15),padx=5,pady=5,width=30,command=self.cr,bg="#00a500",fg="white").pack(side=BOTTOM)
        Button(self.infof,text = 'GO TO MAIN MENU',bd = 3 ,font = ('Courier',15),padx=5,pady=5,width=30,command=self.mainMenu,bg="#00a500",fg="white").pack(side=BOTTOM)

#Create window and application object
root = Tk()
root.title("Visitor Entry Management System")
root.configure(bg="white")
main(root)
root.mainloop()
