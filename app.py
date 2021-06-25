from __future__ import print_function
import os
from flask import Flask, redirect, url_for, request, render_template, flash, send_from_directory
import mysql.connector
from PIL import Image
import base64
import io
import random

from werkzeug.utils import secure_filename
UPLOAD_FOLDER = 'C:/e_commerce/templates/img'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)

@app.route('/test')
def test():

    cnx = mysql.connector.connect(user='root', database = 'e_commerce')
    cursor = cnx.cursor()
    query = "SELECT * FROM image WHERE img_id=4"
    cursor.execute(query)
    var = "im.jpg"
    for (img_id,img) in cursor:
        ima = f"./templates/img/{var}"
        im = Image.open(ima)
        data = io.BytesIO()
        im.save(data, "JPEG")
        encoded_img_data = base64.b64encode(data.getvalue())
        return render_template("img.html", img_data=encoded_img_data.decode('utf-8'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register_action', methods=['GET','POST'])
def register_action():
    if request.method == 'POST':
        bussiness_type = request.form['bussiness_type']
        bussiness_name = request.form['bussiness_name']
        email = request.form['email']
        password = request.form['password']
        cnx = mysql.connector.connect(user='bcba29ecdd2360', database='heroku_24e66d18bdca2de', password="c533db1f")
        cursor = cnx.cursor()
        query = ("INSERT INTO register" "(bussiness_type,bussiness_name,email,password)"
                 "VALUES(%s,%s,%s,%s)"
                 )
        add_data = (bussiness_type,bussiness_name,email,password)
        cursor.execute(query,add_data)
        cnx.commit()
        cursor.close()
        cnx.close()
        return render_template('home.html')
    else:
        return '''
        <html>
        <body>
        <h4>credetials is not ok!!</h4>
        </body>
        </html>
        '''

@app.route('/login_action', methods=['GET','POST'])
def login_action():
    if request.method == 'POST':
        unique = request.form['unique_id']
        name2 = request.form['name']
        password2 = request.form['password']
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        query = f"SELECT name, password from register where unique_id='{unique}'"
        cursor.execute(query)
        for (name, password) in cursor:
            name1 = name
            password1 = password

            if name1 == name2 and password1==password2:
                return render_template('index.html')
    else:
        return 'not ok'

@app.route('/francise_login')
def francise_login():
    return render_template('francise_login.html')

@app.route('/francise_login_action', methods=['GET','POST'])
def francise_login_action():
    if request.method == 'POST':
        bussiness_name2 = request.form['bussiness_name']
        password2 = request.form['password']
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        query = f"SELECT bussiness_name, password from register where bussiness_name = '{bussiness_name2}' AND password = '{password2}'"
        cursor.execute(query)
        for (bussiness_name, password) in cursor:
            name1 = bussiness_name
            password1 = password

            if name1 == bussiness_name2 and password1==password2:
                return render_template('francise_index.html')
            else:
                return render_template('francise_login.html')
    else:
        return 'not ok'

@app.route('/francise_card')
def francise_card():
    return render_template('francise_card.html')

@app.route('/francise_card_action', methods=['GET','POST'])
def francise_card_action():
    if request.method == 'POST':
        francise_name = request.form['name']
        fran_password = request.form['password']
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        query = f"SELECT unique_id, company, used_by, package from card_details where type_of_bussiness = 'francise' AND name_of_bussiness = '{francise_name}'"
        cursor.execute(query)
        for (unique_id,
             company,used_by,package) in cursor:
            unique_id = unique_id

            company = company
            used_by = used_by
            package = package
            return render_template('francise_result.html',
                                   unique_id = unique_id,

            company = company,
            used_by = used_by,
            package = package)

@app.route('/retailer_login')
def retailer_login():
    return render_template('retailer_login.html')

@app.route('/retailer_login_action', methods=['GET','POST'])
def retailer_login_action():
    if request.method == 'POST':
        company_name = request.form['company_name']

        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        query = f"SELECT bussiness_name from register where bussiness_name='{company_name}'"
        cursor.execute(query)
        for (bussiness_name,) in cursor:
            company_name1 = bussiness_name
            if company_name1==company_name:
                return render_template('retailer_index.html')


@app.route('/retailer_amount')
def retailer_amount():
    return render_template('retailer_amount_found.html')

@app.route('/retailer_amount_found_action', methods=['GET','POST'])
def retailer_amount_action():
    if request.method == 'POST':
        company_name = request.form['company_name']
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        query = f"select product_id, company_name,francise_amount from order_tbl where company_name='{company_name}'"
        cursor.execute(query,multi=True)
        for result in cursor.execute(query, multi=True):
            if result.with_rows:

                #print("Rows produced by statement '{}':".format(
                #result.statement))
                rs = result.fetchall()
                return render_template('francise_amount_action.html',res=rs)


@app.route('/my_order')
def my_order():
    return render_template('my_order.html')

@app.route('/my_order_action', methods=['GET','POST'])
def my_order_action():
    if request.method == 'POST':
        company_id = request.form['company_id']
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        query = f"SELECT * from order_details where unique_id='{company_id}'"
        cursor.execute(query)
        for(unique_id,villege,state,district,post_office,house_no,selling_price,con_quantity,product_tax,total_amount) in cursor:
            unique_id=unique_id
            villege=villege
            state=state
            district=district
            post_office=post_office
            house_no=house_no
            selling_price=selling_price
            con_quantity=con_quantity
            product_tax=product_tax
            total_amount=total_amount
            return render_template('my_order_data.html',
                                   unique_id=unique_id,
            villege=villege,
            state=state,
            district=district,
            post_office=post_office,
            house_no=house_no,
            selling_price=selling_price,
            con_quantity=con_quantity,
            product_tax=product_tax,
            total_amount=total_amount
                                   )

@app.route('/create_card_action', methods=['POST','GET'])
def create_card_action():
    if request.method == 'POST':
        activation_code = random.randint(66784647,78965341)
        package = request.form['package']
        company = request.form['company_name']
        francise_name = request.form['francise_name']
        #name_of_bussiness = request.form['name_of_bussiness']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cnx = mysql.connector.connect(user='root', database = 'e_commerce')
            cursor = cnx.cursor()
            add_data = ("INSERT INTO craete_card1"
                        "(package, company_name,francise_name,activation_code,logo)"
                        "VALUES(%s,%s,%s,%s,%s)")
            data = (package,company,francise_name,activation_code,filename)
            cursor.execute(add_data,data)
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('personal_details'))
    else:
        return 'not ok'

@app.route('/personal_details')
def personal_details():
    return render_template('personel_details.html')

@app.route('/personel_details_action', methods=['POST','GET'])
def personael_details_action():
    if request.method == 'POST':
       #name_of_bussiness = request.form['name_of_bussiness']
       first_name = request.form['first_name']
       last_name = request.form['last_name']
       position = request.form['position']
       phone_number = request.form['phone_number']
       alternate_number = request.form['alternate_phone']
       whatsapp = request.form['whatsapp']
       address = request.form['address']
       email = request.form['email']
       website = request.form['website']
       company_est_date = request.form['company_est_date']
       about = request.form['about']
       latitude = request.form['latitude']
       longitude = request.form['longitude']
       unique_id = request.form['company_name']
       francise_name = request.form['francise_name']
       '''if 'file' not in request.files:
           flash('No file part')
           return redirect(request.url)
       file = request.files['file']
       if file.filename == '':
           flash('No selected file')
           return redirect(request.url)
       if file and allowed_file(file.filename):
           filename = secure_filename(file.filename)
           file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))'''

       cnx = mysql.connector.connect(user='root', database = 'e_commerce')
       cursor = cnx.cursor()
       add_data = ("INSERT INTO personel_details2"
       "(first_name, last_name,position,email,address,company_est_date,website,about,phone_number,Alternate_phone,whatsapp,Latitude,Longitude,company_name,francise_name)"
       "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
       data = (first_name,last_name,position,
       email,address,company_est_date,website,
           about,phone_number,alternate_number,whatsapp,latitude,longitude,unique_id,francise_name)
       cursor.execute(add_data,data)
       cnx.commit()
       cursor.close()
       cnx.close()
       return redirect('social_links')
    else:
       return 'not ok'

@app.route('/social_links')
def social_link():
    return render_template('social_link.html')

@app.route('/social_link_action', methods=['POST','GET'])
def social_link_action():
    if request.method == 'POST':
        #name_of_bussiness = request.form['name_of_bussiness']
        facebook = request.form['facebook']
        instagram = request.form['instagram']
        youtube = request.form['youtube']
        company_name = request.form['company_name']
        francise_name = request.form['francise_name']
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        add_data = ("INSERT INTO social_link"
         "(company_name,francise_name,facebook, instagram,youtube)"
         "VALUES(%s,%s,%s,%s,%s)")
        data = (company_name,francise_name,facebook,instagram,youtube)
        cursor.execute(add_data,data)
        cnx.commit()
        cursor.close()
        return redirect(url_for('ecommerce_tbl'))
    else:
        return 'not ok'



@app.route('/ecommerce_tbl')
def ecommerce_tbl():
    return render_template('ecommerce.html')

@app.route('/ecommerce_tbl_action', methods=['POST','GET'])
def ecommerce_tbl_action():
    if request.method == 'POST':
        company_name = request.form['company_name']
        product_name = request.form['product_name']
        francise_name = request.form['francise_name']
        product_id = request.form['product_id']
        mrp = request.form['mrp']
        selling_price = request.form['selling_price']
        product_tax = request.form['product_tax']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cnx = mysql.connector.connect(user='root', database = 'e_commerce')
            cursor = cnx.cursor()
            add_data = ("INSERT INTO ecommerce"
                        "(company_name,francise_name,product_id,product_name,mrp,selling_price,product_tax,prd_image)"
                        "VALUES(%s,%s,%s,%s,%s,%s,%s,%s)")
            data = (company_name,francise_name,product_id,product_name,mrp,selling_price,product_tax,filename)
            cursor.execute(add_data,data)
            cnx.commit()
            cursor.close()
            cnx.close()
            return render_template('ecommerce.html')

    else:
        return 'not ok'

@app.route('/next', methods=['GET', 'POST'])
def next():
    return redirect(url_for('image'))

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/image_action', methods=['POST','GET'])
def image_action():
    if request.method == 'POST':
        #name_of_bussiness = request.form['name_of_bussiness']
        company_name = request.form['company_name']
        francise_name = request.form['francise_name']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cnx = mysql.connector.connect(user='root', database = 'e_commerce')
            cursor = cnx.cursor()
            add_data = ("INSERT INTO image"
                        "(img,company_name,francise_name)"
                        "VALUES(%s,%s,%s)")
            data = (filename,company_name,francise_name)
            cursor.execute(add_data,data)
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('preview'))

    else:
        return 'not ok'

@app.route('/product_service')
def product_service():
    return render_template('product_service.html')

@app.route('/product_service_action', methods=['POST','GET'])
def product_service_action():
    if request.method == 'POST':
        product_name = request.form['product_name']
        unique_id = request.form['unique_id']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            cnx = mysql.connector.connect(user='root', database = 'e_commerce')
            cursor = cnx.cursor()
            add_data = ("INSERT INTO product_service"
                        "(product_name, product_image,unique_id)"
                        "VALUES(%s,%s,%s)")
            data = (product_name,filename,unique_id)
            cursor.execute(add_data,data)
            cnx.commit()
            cursor.close()
            cnx.close()
            return 'ok'
    else:
        return 'not ok'

@app.route('/unique_id')
def unique_id():
    return render_template('unique_id.html')

@app.route('/payable_amount', methods=['GET','POST'])
def payable_amount():
    if request.method == "POST":
        villege = request.form['villege']
        state = request.form['state']
        district = request.form['district']
        post_office = request.form['post_office']
        house_no = request.form['house_no']
        prd_id = request.form['product_id']
        quantity = request.form['quantity']
        company_name = request.form['company_name']

        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursorf = cnx.cursor()
        qrf = f"SELECT francise_name from craete_card1 where company_name = '{company_name}'"
        cursorf.execute(qrf)
        for (francise_name,) in cursorf:
            francise_namef = francise_name

            con_quantity = float(quantity)
            cnx = mysql.connector.connect(user='root', database='e_commerce')
            cursor2 = cnx.cursor()
            query2 = f"SELECT product_name,selling_price,product_tax from ecommerce where product_id='{prd_id}' and company_name='{company_name}'"
            cursor2.execute(query2)
            for (product_name, selling_price,product_tax) in cursor2:
                 product_name = product_name
                 selling_price = float(selling_price)
                 product_tax = float(product_tax)
                 total_amount = float((selling_price*con_quantity)+product_tax)
                 francise_amount = float(total_amount*0.1)
                 retailer_amount = float(total_amount-francise_amount)
                 francise_name_amount = f'{francise_namef}={francise_amount}'
                 retailer_name_amount = f'{company_name}={retailer_amount}'
                 pass
                 cnx = mysql.connector.connect(user='root', database='e_commerce')
                 cursor1 = cnx.cursor()
                 query1 = ("INSERT INTO order_tbl"
                  "(villege,state,district,post_office,house_no,selling_price,con_quantity,product_tax,total_amount,company_amount,francise_amount,product_id,company_name,francise_name)"
                  "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
                 data = (villege,state,district,post_office,house_no,
                    selling_price,con_quantity,product_tax,total_amount,
                         retailer_name_amount,francise_name_amount,prd_id,
                         company_name,francise_namef
                         )
                 cursor1.execute(query1,data)
                 cnx.commit()
                 cursor1.close()
                 cnx.close()
                 return render_template('payable_amount.html',quantity=quantity,
                                   product_name=product_name,
                                   selling_price=selling_price,
                                   product_tax=product_tax,
                                   total_amount=total_amount)
    else:
        return 'not ok'

@app.route('/francise_amount')
def francise_amount():
    return render_template('francise_amount.html')

@app.route('/francise_amount_action', methods=['GET','POST'])
def francise_name_action():
    if request.method == 'POST':
        francise_name = request.form['francise_name']
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        query = f"select product_id, company_name,francise_amount,company_amount from order_tbl where francise_name='{francise_name}'"
        cursor.execute(query,multi=True)
        for result in cursor.execute(query, multi=True):
            if result.with_rows:
        #print("Rows produced by statement '{}':".format(
        #result.statement))
               rs = result.fetchall()
               return render_template('francise_amount_action.html',res=rs)
        '''for (product_id, company_name,francise_amount) in cursor:
            product_id=product_id
            company_name=company_name
            francise_amount=francise_amount
            return render_template('francise_amount_action.html',product_id=product_id,
                                   company_name=company_name,
                                   francise_amount=francise_amount)'''

@app.route('/preview')
def preview():
    return render_template('preview.html')

@app.route('/digital_card1', methods=['POST','GET'])
def digital_card1():
    if request.method == "POST":
        thm = request.form['theme']
        company_name = request.form['company_name']
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor2 = cnx.cursor()
        query2 = f"SELECT logo FROM craete_card1 where company_name='{company_name}'"
        cursor2.execute(query2)
        for (logo,) in cursor2:
            lg = logo
            ima = f'./templates/img/{lg}'
            im = Image.open(ima)
            data = io.BytesIO()
            im.save(data, "JPEG")
            encoded_img_data = base64.b64encode(data.getvalue())
            img_data=encoded_img_data.decode('utf-8')
            pass
            cnx = mysql.connector.connect(user='root', database='e_commerce')
            cursor3 = cnx.cursor()
            query3 = f"SELECT selling_price, company_name FROM ecommerce WHERE company_name='{company_name}'"
            cursor3.execute(query3)
            for (selling_price,company_name) in cursor3:
                mrp = selling_price
                company_name1 = company_name
                pass
                cnx = mysql.connector.connect(user='root', database='e_commerce')
                cursor1 = cnx.cursor()
                query1 = f"SELECT first_name,last_name, email,about,website, address, whatsapp FROM personel_details2 where company_name='{company_name}'"
                cursor1.execute(query1)
                for (first_name,last_name,email_id,about,website,address,whatsapp) in cursor1:
                    f_name = first_name
                    l_name = last_name
                    what = whatsapp
                    mail = email_id
                    web = website
                    add = address
                    about = about
                    pass
                    cnx = mysql.connector.connect(user='root', database='e_commerce')
                    cursor2 = cnx.cursor()
                    query2 = f"SELECT  product_id, product_name,prd_image FROM ecommerce where company_name='{company_name}'"
                    cursor2.execute(query2)
                    for (product_id,product_name, prd_image,
                         ) in cursor2:
                        product_name=product_name
                        product_image=prd_image
                        product_id = product_id

                        nob = company_name1
                        ima = f'./templates/img/{product_image}'
                        im = Image.open(ima)
                        data = io.BytesIO()
                        im.save(data, "JPEG")
                        encoded_img_data = base64.b64encode(data.getvalue())
                        img_data1=encoded_img_data.decode('utf-8')
                        pass
                        cnx = mysql.connector.connect(user='root', database='e_commerce')
                        cursor4 = cnx.cursor()
                        query4 = f"SELECT company_name,package,francise_name from craete_card1 where company_name='{company_name}'"
                        cursor4.execute(query4)
                        for(company,package,francise_name) in cursor4:
                            com = company
                            fn = francise_name
                            pkg = package
                            pass
                            cnx = mysql.connector.connect(user='root', database='e_commerce')
                            cursor8 = cnx.cursor()
                            qr = ("INSERT INTO card_details"
                                  "(francise_name,company_name,used_by,package)"
                                  "VALUES(%s,%s,%s,%s)")
                            add = (fn,com,f_name,pkg)
                            cursor8.execute(qr,add)
                            cnx.commit()
                            cursor8.close()
                            cnx.close()
                            pass
                            cnx = mysql.connector.connect(user='root', database='e_commerce')
                            cursor9 = cnx.cursor()
                            query9 = f"SELECT facebook, instagram,youtube from social_link where company_name = '{company_name}'"
                            cursor9.execute(query9)
                            for (facebook, instagram, youtube) in cursor9:
                                facebook = facebook
                                instagram = instagram
                                youtube = youtube
                                pass
                                if thm == 'Theme1':
                                   return render_template('theme1.html',
                                                  img_data=img_data,mrp=mrp,img_data1=img_data1,
                                                  what=what,mail=mail,product_name1=product_name,
                                                  web=web,
                                                  add=add,about=about,
                                                  selling_price=selling_price,
                                                      com=com,
                                                      f_name=f_name,
                                                      l_name=l_name, product_id=product_id,
                                                          facebook=facebook,
                                                          instagram=instagram,youtube=youtube
                                                            )
                                elif thm == 'Theme2':
                                    return render_template('theme1.html',
                                                           img_data=img_data,mrp=mrp,img_data1=img_data1,
                                                           what=what,mail=mail,product_name1=product_name,
                                                           web=web,
                                                           add=add,about=about,
                                                           selling_price=selling_price,
                                                           com=com,
                                                           f_name=f_name,
                                                           l_name=l_name, product_id=product_id,
                                                           facebook=facebook,
                                                           instagram=instagram,youtube=youtube
                                                           )
                                elif thm == 'Theme3':
                                    return render_template('theme1.html',
                                                           img_data=img_data,mrp=mrp,img_data1=img_data1,
                                                           what=what,mail=mail,product_name1=product_name,
                                                           web=web,
                                                           add=add,about=about,
                                                           selling_price=selling_price,
                                                           com=com,
                                                           f_name=f_name,
                                                           l_name=l_name, product_id=product_id,
                                                           facebook=facebook,
                                                           instagram=instagram,youtube=youtube
                                                           )
                                elif thm == 'Theme4':
                                    return render_template('theme1.html',
                                                           img_data=img_data,mrp=mrp,img_data1=img_data1,
                                                           what=what,mail=mail,product_name1=product_name,
                                                           web=web,
                                                           add=add,about=about,
                                                           selling_price=selling_price,
                                                           com=com,
                                                           f_name=f_name,
                                                           l_name=l_name, product_id=product_id,
                                                           facebook=facebook,
                                                           instagram=instagram,youtube=youtube
                                                           )
                                elif thm == 'Theme5':
                                    return render_template('theme1.html',
                                                           img_data=img_data,mrp=mrp,img_data1=img_data1,
                                                           what=what,mail=mail,product_name1=product_name,
                                                           web=web,
                                                           add=add,about=about,
                                                           selling_price=selling_price,
                                                           com=com,
                                                           f_name=f_name,
                                                           l_name=l_name, product_id=product_id,
                                                           facebook=facebook,
                                                           instagram=instagram,youtube=youtube
                                                           )
                                else:
                                    return render_template('home.html')

                            else:
                                    return render_template('theme1.html')
    else:
        return 'not ok'

@app.route('/contact', methods=['GET','POST'])
def contact():
    if request.method == "POST":
        name = request.form["cname"]
        email = request.form["email"]
        phone_number = request.form["phone"]
        message = request.form["msg"]
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        qr = ("INSERT INTO contact"
              "(name,email,phone_number,message)"
              "VALUES(%s,%s,%s,%s)")
        add = (name,email,phone_number,message)
        cursor.execute(qr,add)
        cnx.commit()
        cursor.close()
        cnx.close()
        return render_template('home.html')



@app.route('/product_view')
def product_view():
    return render_template('product_view.html')

@app.route('/place_order',methods=['GET','POST'])
def place_order():
    return render_template('delivery_address.html')


@app.route('/final_card', methods=['GET','POST'])
def final_card():
    if request.method == 'POST':
        theme = request.form['theme']
        unique_id = request.form['unique_id']
        company_name = request.form['company_name']
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        query = "SELECT product_name FROM ecommerce where company_name='oracle'"
        cursor.execute(query,)
        for product in cursor:
            prd_name = product
            return render_template('test.html',prd_name=prd_name)

@app.route('/admin')
def admin():
    return render_template('admin.html',id=id)


@app.route('/register_data', methods=['GET','POST'])
def admin_action():
    if request.method == 'POST':
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        query = "select * from register"
        cursor.execute(query)
        for (unique_id,name,email,password) in cursor:
            unique_id = unique_id
            name = name
            email = email
            password = password
            return render_template('register_data.html', unique_id=unique_id,
                                   name=name,
                                   email=email,
                                   password=password)

@app.route('/persons_data', methods=['GET','POST'])
def persons_data():
    if request.method == 'POST':
        cnx = mysql.connector.connect(user='root', database='e_commerce')
        cursor = cnx.cursor()
        query = "select * from personel_details"
        cursor.execute(query)
        for (unique_id,first_name,last_name,designation,email_id,
             address,est_date,website,About,phone,Alt_phone,whatsapp,latitude,longitude) in cursor:
            unique_id = unique_id
            first_name = first_name
            last_name = last_name
            designation = designation
            email_id = email_id
            address = address
            est_date = est_date
            website = website
            About = About
            phone = phone
            Alt_phone = Alt_phone
            whatsapp = whatsapp
            latitude = latitude
            longitude = longitude
            return render_template('persons_data.html', unique_id=unique_id,
                                   first_name = first_name,
            last_name = last_name,
            designation = designation,
            email_id = email_id,
            address = address,
            est_date = est_date,
            website = website,
            About = About,
            phone = phone,
            Alt_phone = Alt_phone,
            whatsapp = whatsapp,
            latitude = latitude,
            longitude = longitude)

@app.route('/theme1')
def theme1():
    return render_template('theme1.html')

@app.route('/theme2')
def theme2():
    return render_template('theme2.html')

@app.route('/theme3')
def theme3():
    return render_template('theme3.html')

@app.route('/theme4')
def theme4():
    return render_template('theme4.html')

@app.route('/theme5')
def theme5():
    return render_template('theme5.html')

@app.route('/theme6')
def theme6():
    return render_template('theme6.html')

@app.route('/theme7')
def theme7():
    return render_template('theme7.html')

@app.route('/8')
def theme8():
    return render_template('theme8.html')

@app.route('/theme9')
def theme9():
    return render_template('theme9.html')

@app.route('/theme10')
def theme10():
    return render_template('theme10.html')

@app.route('/theme11')
def theme11():
    return render_template('theme11.html')

@app.route('/theme12')
def theme12():
    return render_template('theme12.html')

@app.route('/theme13')
def theme13():
    return render_template('theme13.html')

@app.route('/theme14')
def theme14():
    return render_template('theme14.html')

@app.route('/theme15')
def theme15():
    return render_template('theme15.html')

@app.route('/theme16')
def theme16():
    return render_template('theme16.html')

@app.route('/theme17')
def theme17():
    return render_template('theme17.html')

@app.route('/theme18')
def theme18():
    return render_template('theme18.html')

@app.route('/theme19')
def theme19():
    return render_template('theme19.html')

@app.route('/theme20')
def theme20():
    return render_template('theme20.html')

@app.route('/rds')
def rds():
    return render_template('index.html')

@app.route('/create_card_ac',methods=['GET','POST'])
def create_card_ac():
    if request.method == 'POST':
        activation_code = random.randint(66784647,78965341)
        frn = request.form['frn']
        name_of_bussiness = request.form['name_of_bussiness']
        package = request.form['package']
        company = request.form['company']
        unique_id = request.form['unique_id']
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            frn_up = frn.upper()
            cnx = mysql.connector.connect(user='root', database = 'e_commerce')
            cursor = cnx.cursor()
            add_data = ("INSERT INTO create_card1"
                        "(name_of_bussiness,bussiness_type,package, company,logo,unique_id,activation_code)"
                        "VALUES(%s,%s,%s,%s,%s,%s,%s)")
            data = (name_of_bussiness,frn,package,company,filename,unique_id,activation_code)
            cursor.execute(add_data,data)
            cnx.commit()
            cursor.close()
            cnx.close()
            return redirect(url_for('personal_details'))
    else:
        return 'not ok'

if __name__=='__main__':
    app.run(debug=True)
