#installing modules
import os
os.system("pip3 install -r requirements.txt")
import sys
if sys.platform == 'darwin':
    os.system("source ~/.bash_profile")
    print("Ready for mac.")

# Importing modules
from flask import Flask, request, jsonify, redirect, render_template
import pymysql
import shortuuid
from tempfile import NamedTemporaryFile
from InvoiceGenerator.api import Invoice, Item, Client, Provider, Creator
from InvoiceGenerator.pdf import SimpleInvoice
import webbrowser

os.environ["INVOICE_LANG"] = "en"

# defining url for website & table name & defining template folders.
baseurl = 'http://127.0.0.1:10000'
table_name = 'urls'
app = Flask(__name__, template_folder='templates')

# Setting up mysql connection
def connection():
    connection = pymysql.connect(host='localhost', user='root', password='123456',
                                 charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)
    return connection

webbrowser.open('http://localhost:10000')

# Main page of site


@app.route('/')
def render():
    return render_template('index.html')

# Shortner page


@app.route('/shortner', methods=['GET', 'POST'])
def shorten():
    if request.method == 'POST':
        LINK = request.form['url']
        SHORT = request.form['custom']
        if not SHORT:
            SHORT = shortuuid.ShortUUID().random(length=7)
        if not LINK:
            return jsonify({'ERROR': 'Please give link'})
        conn = connection()
        mydb = conn.cursor()
        mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
        mydb.execute("USE schoolproject")
        createtable = """CREATE TABLE IF NOT EXISTS urls(id INT AUTO_INCREMENT PRIMARY KEY,LINK TEXT,SHORT TEXT);"""
        mydb.execute(createtable)
        query2 = f"SELECT SHORT FROM urls WHERE SHORT = '{SHORT}'"
        mydb.execute(query2)
        try:
            U = mydb.fetchone()['SHORT']
            if U:
                return jsonify({"Error": 'That short code is already in use.'})
            query = 'INSERT INTO urls (LINK, SHORT) VALUES(%s, %s)'
            mydb.execute(query, (LINK, SHORT))
            conn.commit()
            return render_template('short.html', short_url=baseurl+'/'+SHORT)
        except:
            query = 'INSERT INTO urls (LINK, SHORT) VALUES(%s, %s)'
            mydb.execute(query, (LINK, SHORT))
            conn.commit()
            return render_template('short.html', short_url=baseurl+'/'+SHORT)
    return render_template('short.html')

# hotel management page


@app.route('/hotel')
def hotelpage():
    return render_template("hotel.html")

# hotel customer details


@app.route('/hotel/customerdetails', methods=['GET', 'POST'])
def customerdetails():
    if request.method == 'POST':
        createTable = """CREATE TABLE IF NOT EXISTS customer_details(CID VARCHAR(20),NAME VARCHAR(30),ADDRESS VARCHAR(30),AGE INT,NATIONALITY VARCHAR(30) ,PHONENO CHAR(10),EMAIL VARCHAR(30));"""
        cid = request.form['cid']
        name = request.form['name']
        address = request.form['address']
        age = request.form['age']
        nationality = request.form['nationality']
        phoneno = request.form['phoneno']
        email = request.form['email']
        conn = connection()
        mydb = conn.cursor()
        mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
        mydb.execute("USE schoolproject")
        mydb.execute(createTable)
        query = """INSERT INTO customer_details(cid, name, address,age,nationality,phoneno,email) VALUES('{}','{}','{}','{}','{}','{}','{}')""".format(
            cid, name, address, age, nationality, phoneno, email)
        mydb.execute(query)
        conn.commit()
        return render_template('customerdetails.html', prin="New Customer added to data.")
    return render_template('customerdetails.html')

# hotel bookings


@app.route('/hotel/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        createTable = """CREATE TABLE IF NOT EXISTS BOOKING(CID VARCHAR(20),CHECK_IN DATE,CHECK_OUT DATE);"""
        cid = request.form['cid']
        checkin = request.form['checkin']
        checkout = request.form['checkout']
        conn = connection()
        mydb = conn.cursor()
        mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
        mydb.execute("USE schoolproject")
        mydb.execute(createTable)
        query = """INSERT INTO booking(cid,check_in,check_out) VALUES('{}','{}','{}')""".format(
            cid, checkin, checkout)
        mydb.execute(query)
        conn.commit()
        return render_template('bookings.html', prin="New Booking added.")
    return render_template("bookings.html")

# hotel room rent


@app.route('/hotel/roomrent', methods=['GET', 'POST'])
def roomrent():
    if request.method == 'POST':
        createTable = """CREATE TABLE IF NOT EXISTS ROOM_RENT(CID VARCHAR(20),ROOM_CHOICE INT,NO_OF_DAYS INT,ROOM_NO INT ,ROOMBILL INT);"""
        cid = request.form['cid']
        room_choice = int(request.form.get('roomchoice'))
        print(room_choice)
        room_no = int(request.form['roomno'])
        no_of_days = int(request.form.get('nodays'))
        if room_choice == 1:
            roomrent = no_of_days*2000
        elif room_choice == 2:
            roomrent = no_of_days*4000
        elif room_choice == 3:
            roomrent = no_of_days*6000
        elif room_choice == 4:
            roomrent = no_of_days*8000
        else:
            return render_template("roomrent.html", prin="Wrong Room Choice")
        query = """INSERT INTO room_rent(cid,room_choice,room_no,no_of_days,roombill)VALUES(' {}','{}','{}','{}','{}')""".format(
            cid, room_choice, room_no, no_of_days, roomrent)
        conn = connection()
        mydb = conn.cursor()
        mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
        mydb.execute("USE schoolproject")
        mydb.execute(createTable)
        mydb.execute(query)
        conn.commit()
        return render_template("roomrent.html", prin=f"Thanks! Your Room is booked for {no_of_days} days and total room rent is Rs.{roomrent}/-")
    return render_template("roomrent.html")

# Hotel Restaurant


@app.route("/hotel/restaurant", methods=['GET', 'POST'])
def restaurant():
    if request.method == 'POST':
        createTable = """CREATE TABLE IF NOT EXISTS RESTAURANT(CID VARCHAR(20),MEAL_CHOICE INT,QUANTITY INT,RESTAURANT_BILL INT);"""
        conn = connection()
        mydb = conn.cursor()
        mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
        mydb.execute("USE schoolproject")
        mydb.execute(createTable)
        cid = request.form['cid']
        meal_choice = int(request.form.get("choose"))
        quantity = int(request.form.get("quantity"))
        print(meal_choice)
        print(quantity)

        if meal_choice == 1:
            restaurant_bill = quantity*300
        elif meal_choice == 2:
            restaurant_bill = quantity*500
        else:
            return render_template("restaurant.html", prin="Wrong meal choice.")

        query = """INSERT INTO restaurant(cid,meal_choice,quantity,restaurant_bill)VALUES('{}','{}','{}',' {}')""".format(
            cid, meal_choice, quantity, restaurant_bill)
        mydb.execute(query)
        conn.commit()
        return render_template("restaurant.html", prin=f"Your total bill for meal is Rs.{restaurant_bill}/-")
    return render_template("restaurant.html")

# room rent function


def room_rent(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")
    query1 = f"SELECT ROOMBILL FROM ROOM_RENT WHERE CID = {cid}"
    mydb.execute(query1)
    roomrent = mydb.fetchone()['ROOMBILL'] or 0
    print(roomrent)
    return roomrent

# restaurent function


def rest(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")
    query1 = f"SELECT RESTAURANT_BILL FROM RESTAURANT WHERE CID = {cid}"
    mydb.execute(query1)
    roomrent = mydb.fetchone()['RESTAURANT_BILL'] or 0
    print(roomrent)
    return roomrent

# hotel total bill


@app.route("/hotel/total", methods=['GET', 'POST'])
def total():
    if request.method == 'POST':
        createTable = """CREATE TABLE IF NOT EXISTS TOTAL_AMOUNT(CID VARCHAR(20),ROOMBILL INT ,RESTAURANT_BILL INT ,GRANDTOTAL INT)"""
        conn = connection()
        mydb = conn.cursor()
        mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
        mydb.execute("USE schoolproject")
        mydb.execute(createTable)
        cid = request.form['cid']
        try:

            roomrent = room_rent(cid)
            restaurantbill = rest(cid)
            grandtotal = roomrent + restaurantbill
            query = f"""INSERT INTO total_amount(cid,roombill,restaurant_bill,grandTotal) VALUES('{cid}',{roomrent},{restaurantbill},{grandtotal})"""
            mydb.execute(query)
            conn.commit()
            return render_template("total.html", prin=f'Your total bill is Rs.{grandtotal}')
        except:
            return jsonify({"Error": f"No data found for id: {cid}"})
    return render_template("total.html")


def getname(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")
    cid = request.form['cid']
    query = f"""SELECT NAME FROM customer_details WHERE CID = '{cid}'"""
    mydb.execute(query)
    name = mydb.fetchone()['NAME']
    return name


def getaddress(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")
    cid = request.form['cid']
    query = f"""SELECT ADDRESS FROM customer_details WHERE CID = '{cid}'"""
    mydb.execute(query)
    address = mydb.fetchone()['ADDRESS']
    return address


def getage(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")
    cid = request.form['cid']
    query = f"""SELECT AGE FROM customer_details WHERE CID = '{cid}'"""
    mydb.execute(query)
    age = mydb.fetchone()['AGE']
    return age


def getnation(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")
    cid = request.form['cid']
    query = f"""SELECT NATIONALITY FROM customer_details WHERE CID = '{cid}'"""
    mydb.execute(query)
    nationality = mydb.fetchone()['NATIONALITY']
    return nationality


def getphone(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")
    cid = request.form['cid']
    query = f"""SELECT PHONENO FROM customer_details WHERE CID = '{cid}'"""
    mydb.execute(query)
    phoneno = mydb.fetchone()['PHONENO']
    return phoneno


def getemail(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")
    cid = request.form['cid']
    query = f"""SELECT EMAIL FROM customer_details WHERE CID = '{cid}'"""
    mydb.execute(query)
    email = mydb.fetchone()['EMAIL']
    return email
# Show records


@app.route("/hotel/showrecord", methods=['GET', 'POST'])
def show():
    if request.method == 'POST':
        conn = connection()
        mydb = conn.cursor()
        mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
        mydb.execute("USE schoolproject")
        cid = request.form['cid']
        try:
            query = f"SELECT cid FROM customer_details WHERE CID = '{cid}'"
            mydb.execute(query)
            name = getname(cid)
            address = getaddress(cid)
            age = getage(cid)
            nation = getnation(cid)
            phone = getphone(cid)
            email = getemail(cid)
            return render_template("data.html", para=f'Here are details:', cid=f'Customer Id: {cid}', name=f'Name: {name}', address=f'Address: {address}', age=f'Age: {age}', nation=f'Nationality: {nation}', phone=f'Phone No: {phone}', email=f'Email Id: {email}')
        except:
            return jsonify({"Error": f"Data not found for Id: {cid}"})
    return render_template("data.html")

#delete record from particular table
@app.route('/hotel/delete', methods=['GET', 'POST'])
def delete():
    if request.method == 'POST':
        conn = connection()
        mydb = conn.cursor()
        mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
        mydb.execute("USE schoolproject")
        cid = request.form['cid']
        select = request.form.get("choose")
        try:
            if select == 'all':
                query1 = f"DELETE FROM customer_details WHERE CID='{cid}'"
                query2 = f"DELETE FROM BOOKING WHERE CID='{cid}'"
                query3 = f"DELETE FROM RESTAURANT WHERE CID='{cid}'"
                query4 = f"DELETE FROM room_rent WHERE CID={cid}"
                query5 = f"DELETE FROM TOTAL_AMOUNT WHERE CID='{cid}'"
                mydb.execute(query1)
                mydb.execute(query2)
                mydb.execute(query3)
                mydb.execute(query4)
                mydb.execute(query5)
                conn.commit()
                return render_template("delete.html", para = f'Deleted data from all tables for {cid}')
            elif select == 'bookings':
                query2 = f"DELETE FROM BOOKING WHERE CID='{cid}'"
                mydb.execute(query2)
                conn.commit()
                return render_template("delete.html", para = f'Deleted data from Booking table for {cid}')
            elif select == 'customer':
                query1 = f"DELETE FROM customer_details WHERE CID='{cid}'"
                mydb.execute(query1)
                conn.commit()
                return render_template("delete.html", para = f'Deleted data from Customer Details table for {cid}')
            elif select == 'restaurant':
                query3 = f"DELETE FROM RESTAURANT WHERE CID='{cid}'"
                mydb.execute(query3)
                conn.commit()
                return render_template("delete.html", para = f'Deleted data from Restaurant table for {cid}')
            elif select == 'roomrent':
                query4 = f"DELETE FROM room_rent WHERE CID={cid}"
                mydb.execute(query4)
                conn.commit()
                return render_template("delete.html", para = f'Deleted data from Room Rent table for {cid}')
            elif select == 'total':
                query5 = f"DELETE FROM TOTAL_AMOUNT WHERE CID='{cid}'"
                mydb.execute(query5)
                conn.commit()
                return render_template("delete.html", para = f'Deleted data from Grand Total table for {cid}')
            else:
                return render_template("delete.html", para = f'Please select a valid option.')

        except:
            return jsonify({"Error": "Data not found."})
    return render_template("delete.html")

#invoice
def cuname(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")

    mydb.execute(f'SELECT NAME FROM customer_details WHERE CID = {cid}')
    name=mydb.fetchone()['NAME']
    conn.commit()
    return name

def roomrentforin(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")

    mydb.execute(f'SELECT ROOM_CHOICE FROM ROOM_RENT WHERE CID = {cid}')
    choice = mydb.fetchone()['ROOM_CHOICE']
    mydb.execute(f'SELECT NO_OF_DAYS FROM ROOM_RENT WHERE CID = {cid}')
    days = mydb.fetchone()['NO_OF_DAYS']
    conn.commit()
    price=0
    if choice == 1:
        price+=2000
    elif choice == 2:
        price+=4000
    elif choice == 3:
        price+=6000
    elif choice == 4:
        price+=8000
    return price, days

def restaurantforin(cid):
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")

    mydb.execute(f'SELECT MEAL_CHOICE FROM RESTAURANT WHERE CID = {cid}')
    choice = mydb.fetchone()['MEAL_CHOICE']
    mydb.execute(f'SELECT QUANTITY FROM RESTAURANT WHERE CID = {cid}')
    quantity = mydb.fetchone()['QUANTITY']
    conn.commit()
    price=0
    if choice == 1:
        price+=300
    elif choice == 2:
        price+=500
    return price, quantity


@app.route('/hotel/invoice', methods=['GET', 'POST'])
def invoice():
    if request.method == 'POST':
        conn = connection()
        mydb = conn.cursor()
        mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
        mydb.execute("USE schoolproject")
        cid = request.form['cid']
        try:
            name=cuname(cid)
            days = roomrentforin(cid)[1]
            price = roomrentforin(cid)[0]
            restquan = restaurantforin(cid)[1]
            restprice = restaurantforin(cid)[0]

            client = Client(f'{cid}.'+f' {name}')
            provider = Provider('Canary', bank_account='2600420569', bank_code='2022')
            creator = Creator('ANSH TYAGI')

            invoice = Invoice(client, provider, creator)
            invoice.currency='Rs.'
            invoice.add_item(Item(days, price,description='Room Rent'))
            invoice.add_item(Item(restquan, restprice, description='Restaurant'))

            pdf = SimpleInvoice(invoice)
            pdf.gen(f"invoice.pdf", generate_qr_code=True)
            return jsonify({"SUCCESS": "CHECK SAME DIRECTORY TO SEE PDF."})
        except:
            return jsonify({"Error": 'Data not found!'})
    return render_template("invoice.html")



# redirecting to long link
@app.route('/<SHORT>')
def getlink(SHORT):
    SHORT = str(SHORT)
    conn = connection()
    mydb = conn.cursor()
    mydb.execute("CREATE DATABASE IF NOT EXISTS schoolproject")
    mydb.execute("USE schoolproject")
    try:
        query = 'SELECT LINK FROM urls WHERE SHORT = %s '
        mydb.execute(query, (SHORT))
        redirectURL = mydb.fetchone()['LINK']
        print(redirectURL)
        return redirect(redirectURL, code=301)
    except:
        return jsonify({"ERROR": 'Data not found!'})


# running site
if __name__ == '__main__':
    app.run(host='0.0.0.0', port='10000')
