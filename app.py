import pyodbc
from flask import Flask, render_template, request
import os

app = Flask(__name__)

ACCESS_DB = os.path.abspath("form_data.accdb")  # Ensure full path
DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'
CONN_STR = f'DRIVER={DRIVER};DBQ={ACCESS_DB};'

def insert_submission(name, mobile, address, aadhar, cost):
    try:
        conn = pyodbc.connect(CONN_STR)
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO submissions (name, mobile, address, aadhar, cost)
            VALUES (?, ?, ?, ?, ?)
        """, (name, mobile, address, aadhar, cost))
        conn.commit()
        conn.close()
    except Exception as e:
        print("Database Error:", e)

@app.route('/', methods=['GET'])
def form():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    mobile = request.form['mobile']
    address = request.form['address']
    aadhar = request.form['aadhar']
    cost = float(request.form['cost'])

    insert_submission(name, mobile, address, aadhar, cost)

    return render_template('response.html', name=name, mobile=mobile, address=address, aadhar=aadhar, cost=cost)

if __name__ == "__main__":
    app.run(debug=True)



