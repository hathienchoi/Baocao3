from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Kết nối cơ sở dữ liệu
def connect_to_db():
    connection = psycopg2.connect(
        dbname="mystore_db",
        user="postgres",
        password="hathien2003",
        host="localhost"
    )
    return connection

# Hàm đăng nhập
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        connection = connect_to_db()
        if connection:
            flash("Đăng nhập thành công!", "success")
            return redirect(url_for('menu'))
        else:
            flash("Đăng nhập thất bại!", "danger")
    return render_template('login.html')

# Menu chính
@app.route('/menu')
def menu():
    return render_template('menu.html')

# Chức năng tìm kiếm sản phẩm
@app.route('/search', methods=['GET', 'POST'])
def search_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        connection = connect_to_db()
        with connection.cursor() as cursor:
            query = "SELECT * FROM products WHERE product_name ILIKE %s"
            cursor.execute(query, ('%' + product_name + '%',))
            products = cursor.fetchall()
        return render_template('search_product.html', products=products)
    return render_template('search_product.html')

# Chức năng thêm sản phẩm
@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        product_name = request.form['product_name']
        product_price = request.form['product_price']
        category_id = request.form['category_id']
        connection = connect_to_db()
        with connection.cursor() as cursor:
            query = "INSERT INTO products (product_name, product_price, category_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (product_name, float(product_price), int(category_id)))
            connection.commit()
        flash("Thêm sản phẩm thành công!", "success")
        return redirect(url_for('menu'))
    return render_template('add_product.html')

if __name__ == '__main__':
    app.run(debug=True)
