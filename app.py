from flask import Flask,render_template,request,json
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)

mysql = MySQL()

#MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'bucketlist'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

#koneksi ke db
conn = mysql.connect()

#make cursor
cursor = conn.cursor()

@app.route("/")
def main():
	return render_template('index.html')

@app.route('/showSignUp/')
def showSignUp():
	return render_template('signup.html')

@app.route('/signUp/',methods=['POST'])
def signUp():
	#create user code will be here
	#It's recommended also to use request.form.get('param') instead of request.form['param']
	#read the posted values from UI
	_name = request.form['inputName']
	_email = request.form['inputEmail']
	_password = request.form['inputPassword']
	
	#validate the received values
	"""if _name and _email and _password:
		return json.dumps({'html': '<span>All fields good !!</span>'})
	else:
		return json.dumps({'html':'<span> Enter the required fields</span>'});"""
	
	_hashed_password = generate_password_hash(_password)
	
	cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
	data = cursor.fetchall()
 
	if len(data) is 0:
		conn.commit()
		return json.dumps({'message':'User created successfully !'})
	else:
		return json.dumps({'error':str(data[0])})
	
if __name__ == "__main__":
	app.run()