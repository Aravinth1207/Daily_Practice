
from os import name
import mysql.connector

mydb = mysql.connector.connect(host="localhost", user="AravinthKumar", password="redmi100", database="service_provider")
mycursor = mydb.cursor()

class checkproviderlogin:
    def __init__(self,pID,password):
        self.pID = pID
        self.password = password
    def checkProviderLogin(self):
        mycursor.execute("select provider_ID , password from service_provider_details where provider_ID like %s",(self.pID,))
        providerDetails = mycursor.fetchall()

        if len(providerDetails) != 0:
            if self.pID == str(providerDetails[0][0]) and self.password==providerDetails[0][1]:
                return 1
            else:
                print("Provider_ID or password is incorrect" + "\n" + "Forgot Password?\n if forgot enter yes")
                choice = input("")
                if choice == "yes":
                    newpass = input("Enter new password:")
                    phnumber = input("Enter Your Phone Number:")
                    mycursor.execute("select phone_number from service_provider_details where provider_ID =%s",(self.pID,))
                    ph =mycursor.fetchone()
                    if ph[0]==phnumber:
                        mycursor.execute("update service_provider_details set password = %s where phone_number =%s ",
                                         (newpass, phnumber,))
                        mydb.commit()
                        print("Password has been successfully changed")


        elif len(providerDetails) == 0:
            print("Provider_ID or password is incorrect")




class checkUserLogin:
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def check_login(self):
        mycursor.execute("select username,password from user_details where username like %s", (self.username,))
        userdetails = mycursor.fetchall()
        if len(userdetails)!=0:
            if self.username == userdetails[0][0].lower() and self.password == userdetails[0][1]:
                return 1
            else:
                print("username or password is incorrect" + "\n" + "Forgot Password?\n if forgot enter yes")
                choice = input("")
                if choice == "yes":
                    newpass = input("Enter new password:")
                    mycursor.execute("update user_details set password = %s where username  =%s ",
                                     (newpass, self.username,))
                    mydb.commit()
                    print("Password has been successfully changed")

        elif len(userdetails)==0:
            print("Password or username is incorrect")



def request_service(username):


    print("Select city:")
    mycursor.execute("select city from city")
    city = mycursor.fetchall()
    for row in range(len(city)):
        print(str(row+1)+":"+city[row][0])
    city = int(input())
    print("Services Proivded:")
    mycursor.execute("select service_name from services ")
    services = mycursor.fetchall()
    for row in range(len(services)):
        print(str(row+1)+ ":" +services[row][0])
    service_dict = {}
    for row in range(len(services)):
        dict_key = row+1
        dict_value = services[row][0]
        service_dict[dict_key]=dict_value
    print("Select service:")
    option = int(input())
    mycursor.execute("select company_name, email,phone_number,address from service_provider_details")
    service_provider = mycursor.fetchall()
    print("The services are provided by>>>>>>>>>>>>>>")
    for row in range(len(service_provider)):
        print(str(row+1)+":"+service_provider[row][0])
    chosen_provider = int(input("Choose your service provider:"))
    provider_dict = {}
    for row in range(len(service_provider)):
        dic_key = row+1
        dic_value = [row][0]
        provider_dict[dic_key]=dic_value
    if option >= 1 and option <= 5:
        service = service_dict[option]
        schedule_date = input('Enter your service repair date in YYYY-MM-DD format:')
        schedule_time = input("Enter your time slot:")
        status = "Booked"
        mycursor.execute("insert into booking_details(username,service_name,schedule_date,schedule_time,service_status,provider_ID) values(%s,%s,%s,%s,%s,%s)",(username, service, schedule_date, schedule_time, status,chosen_provider,))
        mydb.commit()
        mycursor.execute("select * from booking_details where username like %s", (username,))
        data = mycursor.fetchall()
        print("Name:%s" % data[-1][0])
        print("Requested service:%s" % data[-1][1])
        print("Scheduled Date:%s" % data[-1][2])
        print("Scheduled Time:%s" % data[-1][3])
        print("Service Status:%s" % data[-1][4])
        print("Booking ID:%s" %data[-1][5])
        while True:
            choice = input("Do you want to add some service request(yes/no):")
            if choice == "yes":
                request_service(username)
            else:
                break

    else:
        print("Invalid Option")






def display(username):
    mycursor.execute("select * from booking_details where username like %s and service_status like %s", (username,"Booked",))
    data = mycursor.fetchall()
    if data:
        print("Name:%s" % data[0][0])
        for row in range(len(data)):
            print("Requested service:%s" % data[row][1])
            print("Scheduled Date:%s" % data[row][2])
            print("Scheduled Time:%s" % data[row][3])
            print("Service Status:%s" % data[row][4])
            print("Booking ID:%s" % data[row][5])
    else:
        print("No records found")
    return 1


def display_requests():
    mycursor.execute("select * from booking_details where service_status like%s", ("Booked",))
    data = mycursor.fetchall()
    for row in range(len(data)):
        print("Name:%s" % data[row][0])
        print("Requested service:%s" % data[row][1])
        print("Scheduled Date:%s" % data[row][2])
        print("Scheduled Time:%s" % data[row][3])
        print("Service Status:%s" % data[row][4])
        print("Booking ID:%s" % data[row][5])


def update_service(booking_id):
    rating = int(input("Enter Rating:"))
    mycursor.execute("update booking_details set service_status=%s where booking_id=%s", ("Completed", booking_id,))
    mycursor.execute("update booking_details set rating_for_user=%s where booking_id=%s",(rating,booking_id,))
    mydb.commit()
    mycursor.execute("select * from booking_details where booking_id=%s", (booking_id,))
    data = mycursor.fetchall()
    for row in range(len(data)):
        print("Name:%s" % data[row][0])
        print("Requested service:%s" % data[row][1])
        print("Scheduled Date:%s" % data[row][2])
        print("Scheduled Time:%s" % data[row][3])
        print("Service Status:%s" % data[row][4])
        print("Booking ID:%s" % data[row][5])
        print("Rating :%s"%data[row][6])


def track_request(booking_id,username):
    mycursor.execute("select booking_ID,username,service_status from booking_details where booking_id=%s", (booking_id,))
    data = mycursor.fetchall()
    if booking_id == data[0][0] and username == data[0][1]:
        for row in range(len(data)):
            status = data[row][2]
        if status == "Booked":
            print("Your service request is not yet completed")
        else:
            print("Completed")
    else:
        print("There is no service request found"+'\n'+"Enter correct Booking ID")

def displayAll():
    mycursor.execute("select * from booking_details")
    allDetails = mycursor.fetchall()
    for row in range(len(allDetails)):
        print("Name:%s" % allDetails[row][0])
        print("Requested service:%s" % allDetails[row][1])
        print("Scheduled Date:%s" % allDetails[row][2])
        print("Scheduled Time:%s" % allDetails[row][3])
        print("Service Status:%s" % allDetails[row][4])
        print("Booking ID:%s" % allDetails[row][5])


class cancelorder:
    def __init__(self,booking_id):
        self.booking_id = booking_id
    def Cancelorder(self):
        mycursor.execute("update booking_details set service_status = %s where booking_id = %s",("Cancelled",self.booking_id))
        mydb.commit()
        mycursor.execute("select * from booking_details where booking_id=%s", (self.booking_id,))
        data = mycursor.fetchall()
        for row in range(len(data)):
            print("Name:%s" % data[row][0])
            print("Requested service:%s" % data[row][1])
            print("Scheduled Date:%s" % data[row][2])
            print("Scheduled Time:%s" % data[row][3])
            print("Service Status:%s" % data[row][4])
            print("Booking ID:%s" % data[row][5])

def giverating(booking_id):
    mycursor.execute("select service_name,service_status,provider_ID from booking_details where booking_id = %s",(booking_id,))
    details = mycursor.fetchone()
    if details[1] == "Completed":
        rating = int(input("Enter Your Rating out of 5:"))
        review = input("write a review for our service :) :")
        mycursor.execute(" update booking_details set ratings_for_service = %s , service_review = %s where booking_ID = %s ",(rating,review,booking_id,))
        mydb.commit()
        print("Thank you <3")
    else:
        print("Your service is not yet done... So you can give review and ratings after the service is done...  :)")
if __name__ == "__main__":
    print("Welcome to Home service solutions -_-")
    Login_type = input("Are you a user or serviceprovider?" + '\n' + "Type your LoginType:")
    Login_type = Login_type.lower()

    if Login_type == "user":
        username = input("Enter your username:")
        password = input("Enter your password:")
        checkuser = checkUserLogin(username,password)
        user = checkuser.check_login()
        if user:
            print("1:Request for services")
            print("2:Show my previous services")
            print("3:Track my service request")
            print("4:Cancel my service request")
            print("5:Give Ratings for service")
            option = int(input("Enter your option:"))
            if option == 1:
                if request_service(username):
                    print("Success")
            elif option == 2:
                display(username)
            elif option == 3:
                track_request(int(input("Enter Booking_ID:")),username)
            elif option == 4:
                cancel = cancelorder(input("Enter Booking ID:"))
                cancel.Cancelorder()
            elif option == 5:
                giverating(input("Enter Booking ID:"))
            else:
                print("Enter Correct Option")

    elif Login_type == "serviceprovider":
        provider_ID = input("Enter your ID:")
        password = input("Enter Your Password:")
        checkproviderdetails = checkproviderlogin(provider_ID,password)
        PID = checkproviderdetails.checkProviderLogin()
        if PID:
            print("1:Display Service Requests" + '\n' + "2:Update Service Status" + '\n' + "3:Display all the service records")
            print("Enter your option:")
            option = int(input())
            if option == 1:
                display_requests()
            if option == 2:
                update_service(int(input("Enter Booking_ID:")))
            if option == 3:
                displayAll()

        else:
            print("Enter correct LoginType")

