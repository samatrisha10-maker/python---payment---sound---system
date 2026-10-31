from abc import ABC ,abstractmethod
import random as dm
from datetime import datetime as dt
import pyttsx3 as pt
import mysql.connector as mysql

e=pt.init()
con=mysql.connect (
    host="localhost",
    user="root",
    password="123456",
    db="bank"
)

class payment (ABC):
    @abstractmethod
    def pay (self,amt):
        pass
    def save_transaction (self,app_name,amt):
        cursor=None
        try:
            cursor=con.cursor()
            transaction_id=dm.randint(1,999999)
            transaction_date=dt.now()

            query="insert into transactions (transaction_id,payment_app,amount,transaction_date) values (%s,%s,%s,%s)"
            values=(
                transaction_id,
                app_name,
                amt,
                transaction_date
            )

            cursor.execute(query,values)
            con.commit()

            print("transaction details ")
            print("transaction_id : = ", transaction_id)
            print("transaction_date:= ",transaction_date)

        except mysql.Error as err:

            print("mysql error ",err)
            con.rollback()
        finally:
            if cursor is not None:
                cursor.close()

class phonepay(payment):
    def pay(self,amt):
        self.amt=amt
        msg=str(amt)+"rupees received by phonpay thank you boss"
        e.say(msg)
        e.runAndWait()
        self.save_transaction("phonepay",amt)

class gpay(payment):
    def pay(self,amt):
        self.amt=amt
        msg=str(amt)+"rupees received by gpay thank you boss"
        e.say(msg)
        e.runAndWait()
        self.save_transaction("gpay",amt)

class other(payment):
    def pay(self,amt):
        self.amt=amt
        msg=str(amt)+"rupees received by other thank you boss"
        e.say(msg)
        e.runAndWait()
        self.save_transaction("other",amt)

try:
    c=int(input("enter number 1.phonepay,2.gpay,3.other"))
    if c not in (1,2,3):
        print("invalid choose number ")
    else:
        amt=int(input("enter the amount"))
        if amt <=0:
            print("invalid amount")
        else:
            if c==1:
                app=phonepay()
            elif c==2:
                app=gpay()
            elif c==3:
                app=other()
            else:
                print("invalid app")
            app.pay(amt)

finally:
    if con is not None and con.is_connected():
        con.close()
        print("database connection closed ")


