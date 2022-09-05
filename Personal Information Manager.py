import random
import mysql.connector
import pyperclip
import webbrowser
import pyfiglet
import time
import sys
import base64
from PIL import Image
import io



connection=mysql.connector.connect(host="localhost",user="root",passwd="karthik123",database="pass_gen")
cursor=connection.cursor()
if connection.is_connected():
    print("success")

def gen_pass():

    s = "abcdefghijklmnopqrtuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@#$%&*!"

    len_pass = int(input("ENTER length PASSWORD"'\t'))

    password = "".join(random.sample(s, len_pass))
    print(password)
    pyperclip.copy(password)
    print("PASSWORD COPIED TO CLIPBOARD")


    query = input("WOULD YOU LIKE TO KEEP THIS PASSWORD?"'\n'"yes/no :-"'\t')
    if ("yes" in query):
        accname=input("ENTER THE NAME OF WEBSITE/APP FOR WHICH YOU WANT TO GENERATE PASSWORD"'\t')
        insert= """INSERT INTO pass_rec(Names,Password) 
                VALUES('{}','{}')""".format(accname,password)
        cursor.execute(insert)
        connection.commit()
        print("Saved succesfully")
        choice()

    else:
        print("OK!")
        choice()


def get_pass():
    m_pass=input("ENTER YOUR ACCESS CODE"'\n')
    if (m_pass=="group3"):
        print("**********ACCESS GRANTED**********")
        ch=int(input("ENTER 1 FOR DISPLAYING ALL PASSWORDS THAT YOU HAVE SAVED"'\n'"ENTER 2 FOR SEARCHING FOR A PASSWORD"'\t'))
        if ch==1:
            def blink_once():
                sys.stdout.write('\rCAUTION : PASSWORDS WONT BE ENCRYPTED')
                time.sleep(0.7)
                b = ("Loading")
                sys.stdout.write('\r     ')
                time.sleep(0.7)

            def blink(number):
                for x in range(0, number):
                    blink_once()

            blink(4)
            exec = "select * from pass_rec"
            cursor.execute(exec)
            data = cursor.fetchall()
            for i in data:
                print(i)
            choice()
        elif ch==2:

            acc_name=input("ENTER NAME OF THE WEBSITE/APP FOR WHICH YOU WANT TO ACCESS PASSWORD"'\t')
            exe="select * from pass_rec where Names ='%s'"%(acc_name,)

            cursor.execute(exe)
            data=cursor.fetchall()
            for row in data:
                copy=row[1]
                string=str(copy)

                pyperclip.copy(string)

            print("PASSWORD SUCCESSFULLY COPIED"'\n')

            ch = input("DO YOU WISH TO GO TO THE DESIRED WEBSITE? "'\n'"yes/no"'\t')
            if ch == "yes":
                if acc_name == "facebook":
                    webbrowser.open('https://www.facebook.com/')
                elif acc_name == "instagram":
                    webbrowser.open('https://www.instagram.com/')
                elif acc_name == "youtube":
                    webbrowser.open('https://www.youtube.com/')
                elif acc_name == "linkedin":
                    webbrowser.open('https://www.linkedin.com')
                elif acc_name == "twitter":
                    webbrowser.open('https://twitter.com/')
                elif acc_name == "google":
                    webbrowser.open('https://google.com')
                elif acc_name == "gmail":
                    webbrowser.open('https://mail.google.com/')
                else:
                    print("WEBSITE/APP NOT FOUND")
                choice()
            elif ch=="no":
                print("OK!")
                choice()
            else:
                print("OH OHH! SEEMS LIKE YOU CHOSE SOMETHING INVALID :('\n'TRY AGAIN")
                choice()

        else:
            print("OH OHH! SEEMS LIKE YOU CHOSE SOMETHING INVALID :('\n'TRY AGAIN")
            choice()

    else:
        print("*****ACCESS DENIED*****")
        choice()



def insert():

    ins=input("ENTER SUBJECT"'\t')
    data=input("ENTER DATA"'\t')
    date=input("ENTER TODAY'S DATE YYYY-MM-DD"'\t')
    insert = """INSERT INTO data_man(Subject,Data,Date) 
                    VALUES('{}','{}','{}')""".format(ins, data,date)
    cursor.execute(insert)
    connection.commit()
    print("Saved succesfully")
    choice()


def getdata():
    ch=int(input("ENTER 1 FOR SHOWING ALL THE DATA"'\n'"ENTER 2 FOR SEARCHING A PARTICULAR DATA"))
    if ch==1:
        from tqdm import tqdm
        loop=tqdm(total=20000,position=0,leave=False)
        for k in range(20000):
            loop.set_description("Fetching details...".format(k))
            loop.update(1)
        loop.close()

        exec = "select * from data_man"
        cursor.execute(exec)
        data = cursor.fetchall()
        #print(data)
        for row in data:
            print(row)
        choice()

    elif ch==2:
        subject= input("ENTER SUBJECT")
        exe = "select * from data_man where Subject ='%s'" % (subject,)

        cursor.execute(exe)
        data = cursor.fetchall()
        for row in data:
            print("SUBJECT:"'\t', row[0])
            print("DATA:"'\t', row[1])
            print("DATE OF CREATION:"'\t', row[2])
            choice()
    else:
        print("OH OHH! SEEMS LIKE YOU CHOSE SOMETHING INVALID :('\n'TRY AGAIN")
        choice()

def img():
    direc= input("enter your image/video directory")
    file = open(direc, 'rb').read()

    # We must encode the file to get base64 string
    file = base64.b64encode(file)

    event=input("ENTER THE EVENT")
    date =input("ENTER EVENT DATE")

    # Sample data to be inserted
    args = (event, file, date)

    # Prepare a query
    query = 'INSERT INTO img_file VALUES(%s, %s, %s)'

    # Execute the query and commit the database.
    cursor.execute(query, args)
    connection.commit()
    print("successfully inserted")
    choice()

def show_img():
    event=input("ENTER EVENT")
    query = "SELECT File FROM img_file where Event='%s'"%(event)

    # Execute the query to get the file
    cursor.execute(query)

    data = cursor.fetchall()

    # The returned data will be a list of list
    image = data[0][0]

    # Decode the string
    binary_data = base64.b64decode(image)

    # Convert the bytes into a PIL image
    image = Image.open(io.BytesIO(binary_data))

    # Display the image
    image.show()
    choice()



def choice():
    choice = input("ENTER 'generate' TO GENERATE A PASSWORD"'\n'
                   "ENTER 'getpass' TO ACCESS YOR SAVED PASSWORDS"'\n'
                   "ENTER 'insert' TO INSERT YOUR IMPORTANT DATA "'\n'
                   "ENTER 'getdata' TO DISPLAY DATA:"'\n'
                   "ENTER 'insert image' TO INSERT AN IMAGE"'\n'
                   "ENTER 'get image' TO ACCESS YOUR STORED IMAGE"'\t')


    if choice == "generate":
        gen_pass()
    elif choice == "getpass":
        get_pass()

    elif choice=="insert":
        insert()
    elif choice=="getdata":
        getdata()
    elif choice=="insert image":
        img()
    elif choice=="get image":
        show_img()
    else:
        print("OH OHH! SEEMS LIKE YOU CHOSE SOMETHING INVALID :('\n'TRY AGAIN")




def to_color(string, color):
    color_code = {'blue': '\033[34m',
                    'yellow': '\033[33m',
                    'green': '\033[32m',
                    'red': '\033[31m'
                    }
    return color_code[color] + str(string) + '\033[0m'

result = pyfiglet.figlet_format("W E L C O M E", font = "slant" )

print(to_color(result,'yellow'))
choice()





