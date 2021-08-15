

from os import name
import mysql.connector
from _datetime import datetime,date

mydb = mysql.connector.connect(host="localhost", user="AravinthKumar", password="redmi100", database="service_provider")
mycursor = mydb.cursor()

class checkproviderlogin:
    def __init__(self,pID,password):
        self.pID = pID
        self.password = password
    #checking provider ID and password to allow and password reset option is availabe 
    def checkProviderLogin(self):
        mycursor.execute("select provider_ID , password from service_provider_details where provider_ID like %s",(self.pID,))
        providerDetails = mycursor.fetchall()

        if len(providerDetails) != 0:
            if self.pID == str(providerDetails[0][0]) and self.password==providerDetails[0][1]:
                return 1
            else:
                print("Provider_ID or password is incorrect" + "\n" + "Forgot Password?\n if forgot enter yes")
                #provider can reset their password if they forget by using phone number
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
                    else:
                        print("Enter Correct phone Number")


        elif len(providerDetails) == 0:
            print("Provider_ID or password is incorrect")



#checking user login to allow and password reset option is available
class checkUserLogin:
    def __init__(self,username,password):
        self.username = username
        self.password = password
    def check_login(self):
        mycursor.execute("select username,password from user_details where username like %s", (self.username,))
        userdetails = mycursor.fetchall()
        if len(userdetails)!=0:
            if (self.username).lower() == userdetails[0][0].lower() and self.password == userdetails[0][1]:
                return 1
            else:
                print("username or password is incorrect" + "\n" + "Forgot Password?\n if forgot enter yes")
                choice = input("")
                #user is allowed to reset their password if they forget by verifying username
                if choice == "yes":
                    newpass = input("Enter new password:")
                    mycursor.execute("update user_details set password = %s where username  =%s ",
                                     (newpass, self.username,))
                    mydb.commit()
                    print("Password has been successfully changed")

        elif len(userdetails)==0:
            print("Password or username is incorrect")


class request_service:
    def __init__(self,username):
        self.username = username
    #making user to request for service untill he exit
    def request_service(self):
        mycursor.execute("select user_ID,email,phone_number,address  from user_details where username = %s",(self.username,))
        userdetails = mycursor.fetchone()
        print("Enter city No:")
        mycursor.execute("select city from city")
        city = mycursor.fetchall()
        #showing availble cities
        for row in range(len(city)):
            print(str(row+1)+":"+city[row][0])
        city_id = int(input())
        print("Services Proivded:")
        mycursor.execute("select service_name from services ")
        services = mycursor.fetchall()
        #showing services available in the cities
        for row in range(len(services)):
            print(str(row+1)+ ":" +services[row][0])
        service_dict = {}
        for row in range(len(services)):
            dict_key = row+1
            dict_value = services[row][0]
            service_dict[dict_key]=dict_value
        print("Enter service NO:")
        option = int(input())
        mycursor.execute("select company_name, email,phone_number,address from service_provider_details")
        service_provider = mycursor.fetchall()
        print("The services are provided by>>>>>>>>>>>>>>")
        #showing service provider details to choose the provider which the user wants
        for row in range(len(service_provider)):
            print(str(row+1)+":"+service_provider[row][0])
        chosen_provider = int(input("Choose your service provider:"))
        provider_dict = {}
        #making option by creating a dictionary using the service values
        for row in range(len(service_provider)):
            dic_key = row+1
            dic_value = [row][0]
            provider_dict[dic_key]=dic_value
        if option >= 1 and option <= 5:
            service = service_dict[option]
            schedule_date = input('Enter your service repair date in YYYY-MM-DD format:')
            schedule_time = input("Enter your time slot:")
            status = "Booked"
            user_ID = userdetails[0]
            booking_date = date.today()
            booking_time = datetime.now().strftime("%H:%M:%S")
            mycursor.execute("insert into booking_details(user_ID,username,service_name,schedule_date,schedule_time,service_status,provider_ID,address,city_ID,booking_time,booking_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(user_ID,username, service, schedule_date, schedule_time, status,chosen_provider,userdetails[3],city_id,booking_time,booking_date,))
            mydb.commit()

            mycursor.execute("select booking_id,user_id,username,service_name,schedule_date,schedule_time,service_status,address from booking_details where username like %s", (username,))
            data = mycursor.fetchall()
            #making payments by online and offline
            payment_method = input("Enter Your Payment Method" + "\n" + "1:online" + "\n" + "2:cash"+"\n")
            if payment_method == "online":
                accountHolderName = str(input('Enter your account holder name:'))
                accountNumber = int(input('Enter your account number:'))
                month = int(input('Enter your account valid month:'))
                year = int(input('Enter your account valid year:'))
                ccv = int(input('Enter your account valid ccv:'))
                paymentTime = datetime.now().strftime("%H:%M:%S")
                paymentDate = date.today()
                mycursor.execute("insert into payment(booking_id,payment_method,account_holder_name,account_no,month,year,ccv,payment_time,payment_date) values(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(data[-1][0], payment_method, accountHolderName, accountNumber, month, year, ccv,paymentTime,paymentDate,))
                mydb.commit()
            else:
                mycursor.execute("insert into payment(booking_id,payment_method)values(%s,%s)",(data[-1][0],payment_method,))
                mydb.commit()
                print("You can pay at the end of the service with cash")
            print("Booking ID:%s" % data[-1][0])
            print("User ID:%s"%data[-1][1])
            print("Name:%s"%data[-1][2])
            print("Requested service:%s" % data[-1][3])
            print("Scheduled Date:%s" % data[-1][4])
            print("Scheduled Time:%s" % data[-1][5])
            print("Service Status:%s" % data[-1][6])
            print("Address :%s"%data[-1][7])
            print("Your service request is successfully booked")
            choice = input("Do you want to add some service request(yes/no):")
            while True:

                if choice == "yes":
                    reques = request_service(username)
                    reques.request_service()
                elif choice =="no":
                    break

        else:
            print("Invalid Option")


    def display(self):
        #displaying the user's previous requests
        mycursor.execute("select username,service_name,schedule_date,schedule_time,service_status,booking_id,ratings_for_service from booking_details where username like %s ", (self.username,))
        data = mycursor.fetchall()
        if data:
            print("Name:%s" % data[0][0])
            for row in range(len(data)):
                print("Requested service:%s" % data[row][1])
                print("Scheduled Date:%s" % data[row][2])
                print("Scheduled Time:%s" % data[row][3])
                print("Service Status:%s" % data[row][4])
                print("Booking ID:%s" % data[row][5])
                print("Rating :%s"%data[row][6])
        else:
            print("No records found")
        return 1




class trackingrequest:
    #allowing user's to track the order by entering booking id
    def __init__(self,booking_id,username):
        self.booking_id =booking_id
        self.username = username
    def track_request(self):
        mycursor.execute("select booking_ID,username,service_status from booking_details where booking_id=%s", (self.booking_id,))
        data = mycursor.fetchall()
        if data:
            if self.booking_id == data[0][0] and username == data[0][1]:
                for row in range(len(data)):
                    status = data[row][2]
                if status == "Booked":
                    print("Your service request is not yet completed")
                elif status =="Cancelled":
                    print("Your service request is Cancelled")
                else:
                    print("Your service request is Completed")
            else:
                print("There is no service request found in your username"+'\n'+"Enter correct Booking ID")
        else:
            print("No Records Found")

class cancelandrate:
    #making user's to cancel their request if they want by using booking id
    def __init__(self,booking_id,username):
        self.booking_id = booking_id
        self.username = username
    def Cancelorder(self):
        mycursor.execute("select service_status,username from booking_details where  booking_id = %s and username like %s",(self.booking_id,self.username,))
        canceldetails = mycursor.fetchone()
        if canceldetails:
            if canceldetails[0]=="Booked":
                mycursor.execute("update booking_details set service_status = %s where booking_id = %s",("Cancelled",self.booking_id))
                mydb.commit()
                mycursor.execute("select username,service_name,schedule_date,schedule_time,service_status,booking_id from booking_details where booking_id=%s", (self.booking_id,))
                data = mycursor.fetchall()
                if data:
                    for row in range(len(data)):
                        print("Name:%s" % data[row][0])
                        print("Requested service:%s" % data[row][1])
                        print("Scheduled Date:%s" % data[row][2])
                        print("Scheduled Time:%s" % data[row][3])
                        print("Service Status:%s" % data[row][4])
                        print("Booking ID:%s" % data[row][5])
                        print("Your request is successfully cancelled")
                else:
                    print("No requests found")
            elif canceldetails[0] == "Cancelled":
                print("Your request is already Cancelled")
            elif canceldetails[0]=="Completed":
                print("Your request is already Completed")
        else:
            print("No requests found in your username")
    #making user to give ratings and a review for the completed service to the service providers
    def giverating(self):
        mycursor.execute("select ratings_for_service from booking_details where booking_id like %s and username like %s",(self.booking_id,self.username,))
        rate = mycursor.fetchone()
        if rate[0]==None:
            mycursor.execute("select username,service_name,service_status,provider_ID from booking_details where booking_id = %s and username like %s",
                             (self.booking_id,self.username))
            details = mycursor.fetchone()
            if details:

                if details[2] == "Completed":
                    rating = int(input("Enter Your Rating out of 5:"))
                    review = input("write a review for our service :) :")
                    mycursor.execute(
                        " update booking_details set ratings_for_service = %s , service_review = %s where booking_ID = %s ",
                        (rating, review, self.booking_id,))
                    mydb.commit()
                    print("Thank you <3")
                elif details[2]=="Booked":
                    print("Your service is not yet done... So you can give review and ratings after the service is done...  :)")
                elif details[2]=="Cancelled":
                    print("Your request is Cancelled ... You can not give rating for cancelled services")
            else:
                print("No Records Found")
        else:
            print("You already rated this service")



class displayforprovider:
    #making serviceprovider to accept the request of the user using provider id
    def __init__(self,provider_ID):
        self.provider_ID = provider_ID
    def display_requests(self):
        mycursor.execute("select username,service_name,schedule_date,schedule_time,service_status,booking_id,address from booking_details where service_status like%s and provider_ID = %s", ("Booked",self.provider_ID,))
        data = mycursor.fetchall()
        if data:
            for row in range(len(data)):
                print("Name:%s" % data[row][0])
                print("Requested service:%s" % data[row][1])
                print("Scheduled Date:%s" % data[row][2])
                print("Scheduled Time:%s" % data[row][3])
                print("Service Status:%s" % data[row][4])
                print("Booking ID:%s" % data[row][5])
                print("Address :%s"%data[row][6])
        else:
            print("No requests found")
    #making service provider to view all of their services
    def displayAll(self):
        mycursor.execute("select username,service_name,schedule_date,schedule_time,service_status,booking_id,rating_for_user  from booking_details where provider_ID =%s",(self.provider_ID,))
        allDetails = mycursor.fetchall()
        if allDetails:
            for row in range(len(allDetails)):
                print("Name:%s" % allDetails[row][0])
                print("Requested service:%s" % allDetails[row][1])
                print("Scheduled Date:%s" % allDetails[row][2])
                print("Scheduled Time:%s" % allDetails[row][3])
                print("Service Status:%s" % allDetails[row][4])
                print("Booking ID:%s" % allDetails[row][5])
                print("Rating :%s"%allDetails[row][6])
        else:
            print("No active requests found")




class update:
    #making service provider to update the completed service request and to give rating for the customer using booking id and provider id
    def __init__(self,booking_id,provider_ID):
        self.booking_id = booking_id
        self.provider_ID = provider_ID
    def update_service(self):
        mycursor.execute("select service_status from booking_details where booking_id like %s and provider_ID like %s",(self.booking_id,self.provider_ID))
        status = mycursor.fetchone()
        if status:
            if status[0]=="Completed":
                print("You already update this service details")
            elif status[0]=="Booked":
                rating = int(input("Enter Rating:"))
                mycursor.execute("update booking_details set service_status=%s where booking_id=%s and provider_ID = %s", ("Completed", self.booking_id,self.provider_ID,))
                mycursor.execute("update booking_details set rating_for_user=%s where booking_id=%s",(rating,self.booking_id,))
                mydb.commit()
                mycursor.execute("select username,service_name,schedule_date,schedule_time,service_status,booking_id,rating_for_user  from booking_details where booking_id=%s", (self.booking_id,))
                data = mycursor.fetchall()
                if data:
                    for row in range(len(data)):
                        print("Name:%s" % data[row][0])
                        print("Requested service:%s" % data[row][1])
                        print("Scheduled Date:%s" % data[row][2])
                        print("Scheduled Time:%s" % data[row][3])
                        print("Service Status:%s" % data[row][4])
                        print("Booking ID:%s" % data[row][5])
                        print("Rating :%s"%data[row][6])
                else:
                    print("No requests found")
            else:
                print("Service request if cancelled")
        else:
            print("Check with your Booking ID")

    



if __name__ == "__main__":
    #main method to login and display the option according to the login type
    print("Welcome to Home service solutions -_-")
    Login_type = input("Are you a user or serviceprovider?" + '\n' + "Type your LoginType:")
    Login_type = Login_type.lower()

    if Login_type == "user":
        username = input("Enter your username:")
        password = input("Enter your password:")
        checkuser = checkUserLogin(username,password)
        user = checkuser.check_login()
        requestdisplay = request_service(username)
        if user:
            print("1:Request for services")
            print("2:Show my previous services")
            print("3:Track my service request")
            print("4:Cancel my service request")
            print("5:Give Ratings for service")
            option = int(input("Enter your option:"))
            if option == 1:
                requestdisplay.request_service()
            elif option == 2:
                requestdisplay.display()
            elif option == 3:
                trackrequest = trackingrequest(int(input("Enter Booking_ID:")),username)
                trackrequest.track_request()
            elif option == 4:
                cancel = cancelandrate(input("Enter Booking ID:"),username)
                cancel.Cancelorder()
            elif option == 5:
                servicerating = cancelandrate(input("Enter Booking ID:"),username)
                servicerating.giverating()
            else:
                print("Enter Correct Option")

    elif Login_type == "serviceprovider":
        provider_ID = input("Enter your ID:")
        password = input("Enter Your Password:")
        checkproviderdetails = checkproviderlogin(provider_ID,password)
        PID = checkproviderdetails.checkProviderLogin()
        display = displayforprovider(provider_ID)

        if PID:
            print("1:Display Service Requests" + '\n' + "2:Update Service Status" + '\n' + "3:Display all the service records")
            print("Enter your option:")
            option = int(input())
            if option == 1:
                display.display_requests()
            if option == 2:
                updateservice =update(int(input("Enter Booking_ID:")),provider_ID)
                updateservice.update_service()
            if option == 3:
                display.displayAll()

    else:
        print("Enter correct LoginType")

