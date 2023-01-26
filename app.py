
from flask import Flask, render_template, current_app, send_from_directory
from flask_mysqldb import MySQL
import MySQLdb.cursors
import pdfkit
from flask import send_file
from datetime import date
from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np
from flask_mysqldb import MySQL
from datetime import date
import os

model = pickle.load(open('fertilizer.pkl', 'rb'))

app = Flask(__name__)

# Database Connection
app = Flask(__name__)
app.secret_key = os.urandom(24)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'fertilizer_predictor'

mysql = MySQL(app)


# -----------------------------------------------------------------------------------------------------------------------------

# Switching webpages
@app.route('/')
def home_page():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # executing query
    cursor.execute(
        "SELECT COUNT(*) AS Users  FROM user_details")
    data01 = cursor.fetchall()
    cursor.execute(
        "SELECT COUNT(*) AS Predictions  FROM prediction_details")
    data02 = cursor.fetchall()

    cursor.execute(
        "SELECT COUNT(DISTINCT Location_of_Farm) AS Locations  FROM prediction_details")
    data03 = cursor.fetchall()
    
    cursor.execute(
        "SELECT COUNT(DISTINCT Gat_Number) AS Plots  FROM prediction_details")
    data04 = cursor.fetchall()

    return render_template('index.html', data01=data01[0].get("Users"), data02=data02[0].get("Predictions"),data03=data03[0].get("Locations"),data04=data04[0].get("Plots"))


@app.route('/user_index')
def user_page():
    return render_template('user/index.html')


@app.route('/index')
def index():
    if 'user_id' in session:
        return render_template('prediction.html')
    else:
        return render_template('login_from_home.html')



@app.route('/login_admin')
def login_admin():
    if 'user_id' in session:
        return render_template('admin/log_out_admin.html')
    else:
        return render_template('login_admin.html')


@app.route('/log_admin', methods=['POST'])
def log_admin():
    email = request.form['email']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM admin_details WHERE Email_Address LIKE '{}' and Password like '{}'".format(email, password))
    user = cur.fetchall()
    if len(user) > 0:
        session['user_id'] = user[0][0]
        cur.close()
        return render_template('login_success_admin.html')
    else:
        cur.close()
        return render_template('login_invalid_admin.html')


@app.route('/logout_admin', methods=['POST'])
def logout_admin():
    session.pop('user_id')
    return render_template('admin/logout_success_admin.html')

@app.route('/logout_admin1')
def logout_admin1():
    session.pop('user_id')
    return render_template('admin/logout_success_admin.html')


@app.route('/fertilizer_prediction')
def fertilizer_prediction():
    if 'user_id' in session:
        return render_template('admin/prediction.html')
    else:
        return render_template('login_admin.html')


@app.route('/admin_index', methods=['POST', 'GET'])
def options_after_admin_login():
    return render_template('admin/index.html')


@app.route('/register_admin')
def register_admin():
    return render_template('admin/register_admin.html')


@app.route('/reg_admin', methods=['POST'])
def reg_admin():
    if request.method == "POST":
        fname = request.form['fname']
        fnum = request.form['fnum']
        fp = request.form['fp']
        fe = request.form['fe']
        fid = request.form['fid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM admin_details WHERE Email_Address LIKE '{}'".format(fe))
        email1 = cur.fetchall()
        cur.execute("SELECT * FROM admin_details WHERE Email_Address LIKE '{}'".format(fid))
        id1 = cur.fetchall()
        cur.execute("SELECT * FROM admin_details WHERE Mobile_Number LIKE '{}'".format(fnum))
        mob_num1 = cur.fetchall()
        if len(email1) == 0 and len(mob_num1) == 0 and len(id1) == 0:
            cur.execute(
                "INSERT INTO admin_details(Admin_ID, Admin_Name, Mobile_Number,Email_Address, Password) VALUES (%s,%s,%s,%s,%s)",
                (fid, fname, fnum, fe, fp))
            mysql.connection.commit()
            cur.close()
            return render_template('admin/register_success_admin.html')
        else:
            cur.close()
            return render_template('admin/register_fail_admin.html')


@app.route('/register_tester')
def register_tester():
    return render_template('admin/register_tester.html')


@app.route('/reg_tester', methods=['POST'])
def reg_tester():
    if request.method == "POST":
        fname = request.form['fname']
        fnum = request.form['fnum']
        fp = request.form['fp']
        fe = request.form['fe']
        fid = request.form['fid']
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM tester_details WHERE Email_Address LIKE '{}'".format(fe))
        email1 = cur.fetchall()
        cur.execute("SELECT * FROM tester_details WHERE Tester_ID LIKE '{}'".format(fid))
        id1 = cur.fetchall()
        cur.execute("SELECT * FROM tester_details WHERE Mobile_Number LIKE '{}'".format(fnum))
        mob_num1 = cur.fetchall()
        if len(email1) == 0 and len(mob_num1) == 0 and len(id1) == 0:
            cur.execute(
                "INSERT INTO tester_details(Tester_ID, Name, Mobile_Number,Email_Address, Password) VALUES (%s,%s,%s,%s,%s)",
                (fid, fname, fnum, fe, fp))
            mysql.connection.commit()
            cur.close()
            return render_template('admin/register_success_tester.html')
        else:
            cur.close()
            return render_template('admin/register_fail_tester.html')


@app.route('/register_user')
def register_user():
    return render_template('admin/register_user.html')


@app.route('/reg_user', methods=['POST'])
def reg_user():
    if request.method == "POST":
        fname = request.form['fname']
        fnum = request.form['fnum']
        reg_by = session['user_id']
        fv = request.form['fv']
        fp = request.form['fp']
        cur = mysql.connection.cursor()

        cur.execute("SELECT * FROM user_details WHERE Mobile_Number LIKE '{}'".format(fnum))
        mob_num1 = cur.fetchall()
        if len(mob_num1) == 0:
            cur.execute(
                "INSERT INTO user_details( Name, Mobile_Number, Village,Password,Registered_by) VALUES (%s,%s,%s,%s,%s)",
                (fname, fnum, fv, fp, reg_by))
            mysql.connection.commit()
            cur.close()
            return render_template('admin/register_success_user.html')
        else:
            cur.close()
            return render_template('admin/register_fail_user.html')


@app.route('/login_user')
def login_user():
    if 'user_id' in session:
        return render_template('user/log_out_user.html')
    else:
        return render_template('/login_user.html')

@app.route('/logout_user', methods=['POST'])
def logout_user():
    session.pop('user_id')
    return render_template('user/logout_success_user.html')

@app.route('/logout_user1')
def logout_user1():
    session.pop('user_id')
    return render_template('user/logout_success_user.html')

# **************************************************************DELETE USER START***************************************************************

@app.route('/del_user', methods=['POST'])
def del_user():
    fnum = request.form['fnum']
    fp = request.form['fp']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_details WHERE Mobile_Number LIKE '{}' and Password like '{}'".format(fnum, fp))
    user = cur.fetchall()
    if len(user) > 0:
        cur.execute("DELETE FROM user_details WHERE Mobile_Number LIKE '{}'".format(fnum))
        mysql.connection.commit()
        cur.close()
        return render_template('admin/delete_success.html')
    else:
        cur.close()
        return render_template('admin/delete_fail_user.html')

@app.route('/del_user1')
def del_user1():
   
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_details WHERE Mobile_Number LIKE '{}'".format(session['user_id']))
    user = cur.fetchall()
    if len(user) > 0:
        cur.execute("DELETE FROM user_details WHERE Mobile_Number LIKE '{}'".format(session['user_id']))
        mysql.connection.commit()
        cur.close()
        return render_template('user/delete_success.html')
    else:
        cur.close()
        return render_template('user/delete_fail_user.html')


@app.route('/delete_user')
def delete_user():
    return render_template('admin/delete_user.html')


# **************************************************************DELETE USER END***************************************************************


# **************************************************************DELETE ADMIN START***************************************************************

@app.route('/delete_admin')
def delete_admin():
    if 'user_id' in session:
        return render_template('admin/delete_admin.html')
    else:
        return render_template('/')


@app.route('/del_admin', methods=['POST'])
def del_admin():
    fnum = request.form['fnum']
    fp = request.form['fp']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin_details WHERE Mobile_Number LIKE '{}' and Password like '{}'".format(fnum, fp))
    user = cur.fetchall()
    if len(user) > 0:
        if (session['user_id'] == user[0][0]):
            session.pop('user_id')
        cur.execute("DELETE FROM admin_details WHERE Mobile_Number LIKE '{}' and Password like '{}'".format(fnum, fp))
        mysql.connection.commit()
        cur.close()
        return render_template('admin/delete_success.html')
    else:
        cur.close()
        return render_template('admin/delete_fail_admin.html')


# **************************************************************DELETE ADMIN END***************************************************************


# **************************************************************UPDATE ADMIN START***************************************************************

#admin section
@app.route('/view_profile_admin')
def view_profile_admin():
    data= session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin_details WHERE Admin_ID LIKE '{}'".format(data))
    user = cur.fetchall()
    cur.close()
    return render_template('admin/view_profile_admin.html',user=user)

#admin section
@app.route('/fetch_admin')
def fetch_admin():
    return render_template('admin/fetch_admin.html')


#admin section
@app.route('/update_admin',methods=['POST'])
def update_admin():
   
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin_details WHERE Admin_ID LIKE '{}' ".format(session['user_id']))
    admin_data = cur.fetchall()
    if len(admin_data) > 0:
        cur.close()
        return render_template('admin/update_admin.html', admin_data=admin_data)
    else:
        cur.close()
        return render_template('admin/fetch_admin_fail.html')

#admin section
@app.route('/update_admin1')
def update_admin1():
   
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM admin_details WHERE Admin_ID LIKE '{}' ".format(session['user_id']))
    admin_data = cur.fetchall()
    if len(admin_data) > 0:
        cur.close()
        return render_template('admin/update_admin.html', admin_data=admin_data)
    else:
        cur.close()
        return render_template('admin/fetch_admin_fail.html')


#admin section
@app.route('/update_admin_data', methods=['POST'])
def update_admin_data():
    fname = request.form['fname']
    fnum = request.form['fnum']
    fe = request.form['fe']
    Mobile = request.form['mb']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE admin_details SET Admin_Name=%s, Mobile_Number=%s, Email_Address=%s WHERE Mobile_Number=%s ",
                (fname, fnum, fe, Mobile))
    mysql.connection.commit()
    cur.close()
    return render_template('admin/update_success.html')


# **************************************************************UPDATE ADMIN END***************************************************************


# **************************************************************UPDATE USER START***************************************************************

#admin
@app.route('/fetch_user')
def fetch_user():
    return render_template('admin/fetch_user.html')

#user view profile   
@app.route('/view_profile_user')
def view_profile_user():
    data= session['user_id']
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM user_details WHERE Mobile_Number LIKE '{}'".format(data))
    user = cur.fetchall()
    cur.close()
    return render_template('user/view_profile_user.html',user=user)


#user section- update profile

@app.route('/update_user1')
def update_user1():   
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM user_details WHERE Mobile_Number LIKE '{}'".format(session['user_id']))
    user_data = cur.fetchall()
    if len(user_data) > 0:
        cur.close()
        return render_template('user/update_user.html', user_data=user_data)
    else:
        cur.close()
        return render_template('admin/fetch_user_fail.html') 

#admin section update user
@app.route('/update_user', methods=['POST'])
def update_user():
    fnum = request.form['fnum']
    password = request.form['fp']
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM user_details WHERE Mobile_Number LIKE '{}' and Password like '{}'".format(fnum, password))
    user_data = cur.fetchall()
    if len(user_data) > 0:
        cur.close()
        return render_template('admin/update_user.html', user_data=user_data)
    else:
        cur.close()
        return render_template('admin/fetch_user_fail.html')

#user section update data
@app.route('/update_user_data1', methods=['POST'])
def update_user_data1():
    fname = request.form['fname']
    fnum = request.form['fnum']
    Mobile = request.form['mb']
    password = request.form['fp']
    fv = request.form['fv']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE user_details SET Mobile_Number=%s, Name=%s,Village=%s, Password=%s WHERE Mobile_Number=%s ",
                (fnum,fname, fv, password, Mobile))
    mysql.connection.commit()
    cur.close()
    return render_template('user/update_success.html')

#Admin section
@app.route('/update_user_data', methods=['POST'])
def update_user_data():
    fname = request.form['fname']
    fnum = request.form['fnum']
    Mobile = request.form['mb']
    password = request.form['fp']
    fv = request.form['fv']
    cur = mysql.connection.cursor()
    cur.execute("UPDATE user_details SET Mobile_Number=%s, Name=%s,Village=%s, Password=%s WHERE Mobile_Number=%s ",
                ( fnum,fname, fv, password, Mobile))
    mysql.connection.commit()
    cur.close()
    return render_template('admin/update_success.html')





# **************************************************************UPDATE USER END***************************************************************


@app.route('/log_user', methods=['POST'])
def log_user():
    fnum = request.form['fnum']
    password = request.form['password']
    cur = mysql.connection.cursor()
    cur.execute(
        "SELECT * FROM user_details WHERE Mobile_Number LIKE '{}' and Password like '{}'".format(fnum, password))
    user = cur.fetchall()
    if len(user) > 0:
        session['user_id'] = user[0][0]
        cur.close()
        return render_template('login_success_user.html')
    else:
        cur.close()
        return render_template('login_invalid_user.html')





# ------------------------------------------------------------------------------------------------------------------------

# Making Prediction

@app.route('/prediction', methods=['POST'])
def prediction():
    data1 = request.form['Temperature']
    data2 = request.form['Humidity']
    data3 = request.form['N']
    data4 = request.form['P']
    data5 = request.form['K']
    data6 = request.form['Soil']
    data7 = request.form['Crop']
    data8 = request.form['Mobile_Number']
    data9 = request.form['Location_of_Farm']
    data10 = request.form['Submitted_Date']
    data11= request.form['Gat_Number']

 

    if data6 == "rice":
        data6 = 0
    elif data6 == "Coconut":
        data6 = 1
    elif data6 == "Maize":
        data6 = 2
    elif data6 == "Cotton":
        data6 = 3
    elif data6 == "Tabacco":
        data6 = 4
    elif data6 == "Paddy":
        data6 = 5
    elif data6 == "Barley":
        data6 = 6
    elif data6 == "Wheat":
        data6 = 7
    elif data6 == "Millets":
        data6 = 8
    elif data6 == "Oil seeds":
        data6 = 9
    elif data6 == "Sugarcane":
        data6 = 10
    elif data6 == "Pulses":
        data6 = 11
    elif data6 == "Ground Nuts":
        data6 = 12

    if data7 == "Clayey":
        data7 = 0
    elif data7 == "laterite":
        data7 = 1
    elif data7 == "silty clay":
        data7 = 2
    elif data7 == "sandy":
        data7 = 3
    elif data7 == "coastal":
        data7 = 4
    elif data7 == "clay loam":
        data7 = 5
    elif data7 == "alluvial":
        data7 = 6
    elif data7 == "Sandy":
        data7 = 7
    elif data7 == "Loamy":
        data7 = 8
    elif data7 == "Black":
        data7 = 9
    elif data7 == "Red":
        data7 = 10

    arr = np.array([[data1, data2, data3, data4, data5, data6, data7]])
    pred = model.predict(arr)
    cur = mysql.connection.cursor()
    # cust_id=session['user_id']
    curr_date = date.today()
    result = ""
    if pred == 0:
        result = "DAP and MOP"
    elif pred == 1:
        result = "Good NPK"
    elif pred == 2:
        result = "MOP"
    elif pred == 3:
        result = "Urea and DAP"
    elif pred == 4:
        result = "Urea and MOP"
    elif pred == 5:
        result = "Urea"
    elif pred == 6:
        result = "DAP"
    elif pred == 7:
        result = "14-35-14"
    elif pred == 8:
        result = "28-28"
    elif pred == 9:
        result = "17-17-17"
    elif pred == 10:
        result = "20-20"
    elif pred == 11:
        result = " 10-26-26"

    cur.execute("SELECT * FROM user_details WHERE Mobile_Number LIKE '{}'".format(data8))
    user = cur.fetchall()
    if not (len(user)):
        cur.close()
        return render_template('admin/user_doesnot_exist.html')

    data12 = session['user_id']
    cur.execute(
        "INSERT INTO prediction_details(Mobile_Number,Location_of_Farm, Temperature, Humidity, N, P, K, Soil_Type, Crop_Type, Fertilizer, Submitted_Date,Processed_Date,Tested_By,Gat_Number) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
        (data8, data9, data1, data2, data3, data4, data5, data6, data7, result, data10, curr_date, data12,data11))
    mysql.connection.commit()
    cur.close()
    return render_template('admin/prediction.html', data=pred)


@app.route('/projectlist', methods=['GET', 'POST'])
def projectlist():
    # creating variable for connection
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # executing query
    cursor.execute(
        "SELECT DISTINCT * from (prediction_details INNER JOIN user_details on user_details.Mobile_Number=prediction_details.Mobile_Number INNER JOIN admin_details on prediction_details.Tested_By=admin_details.Admin_ID) where prediction_details.Test_ID=(select max(prediction_details.Test_ID) from prediction_details)")
    # fetching all records from database
    data = cursor.fetchall()
    # returning back to projectlist.html with all records from MySQL which are stored in variable data
    return render_template("admin/projectlist.html", data=data)


@app.route('/search')
def search():
    return render_template('admin/search.html')

@app.route('/table_search', methods=['GET', 'POST'])
def table_search():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        testid = request.form['testid']
        datep = request.form['datep']
        datel = request.form['datel']
        # search by author or book
        cursor.execute(
            "SELECT n.Test_ID,n.Mobile_Number, n.Location_of_farm,n.Temperature,n.Humidity,n.N,n.P,n.K,n.Crop_Type,n.Soil_Type,n.fertilizer,n.Processed_Date,s.Name  ,a.Admin_Name, n.Gat_Number from (prediction_details n INNER JOIN user_details s on s.Mobile_Number=n.Mobile_Number INNER JOIN admin_details a on n.Tested_By=a.Admin_ID) where n.Mobile_Number LIKE %s AND n.Processed_Date BETWEEN %s AND %s",
            (testid, datep, datel))

        data = cursor.fetchall()

        if len(data)>0:
            return render_template('admin/table_search.html', data=data)
        else:
            return render_template('admin/NoData.html')

@app.route('/search_user')
def search_user():
    return render_template('user/search.html')


@app.route('/table_search_user', methods=['GET', 'POST'])
def table_search_user():
    if request.method == "POST":
        cursor = mysql.connection.cursor()
        testid = request.form['testid']
        datep = request.form['datep']
        datel = request.form['datel']
        # search by author or book
        cursor.execute(
            "SELECT n.Test_ID,n.Mobile_Number, n.Location_of_farm,n.Temperature,n.Humidity,n.N,n.P,n.K,n.Crop_Type,n.Soil_Type,n.fertilizer,n.Processed_Date,s.Name  ,a.Admin_Name,n.Gat_Number from (prediction_details n INNER JOIN user_details s on s.Mobile_Number=n.Mobile_Number INNER JOIN admin_details a on n.Tested_By=a.Admin_ID) where n.Mobile_Number LIKE %s AND n.Processed_Date BETWEEN %s AND %s",
            (testid, datep, datel))

        data = cursor.fetchall()

        if len(data)>0:
            return render_template('user/table_search.html', data=data)
        else:
            return render_template('user/NoData.html')





# -----------------------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    app.run(debug=True)
