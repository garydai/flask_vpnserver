from flask import Flask
from flask_restful import Resource, Api
from flask.ext.mysql import MySQL
from flask_restful import reqparse

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'zhulong'
app.config['MYSQL_DATABASE_PASSWORD'] = 'zhulong123'
app.config['MYSQL_DATABASE_DB'] = 'radius'
app.config['MYSQL_DATABASE_HOST'] = '47.88.149.225'


mysql.init_app(app)

api = Api(app)

app = Flask(__name__)
api = Api(app)

class CreateUser(Resource):
	
	def post(self):
		try:
	    	# Parse the arguments
			parser = reqparse.RequestParser()
			parser.add_argument('userid', type=str)
			args = parser.parse_args()
			userId = args['userid']
			if userId is None:
				return {'error': 'no userid'} 

			conn = mysql.connect()
			cursor = conn.cursor()
			sql = "insert into radcheck (username, attribute, op, value) VALUES ('%s', 'Cleartext-Password', ':=', 'gagatechang') " % userId 
			print sql
			cursor.execute(sql)
			conn.commit()
			return {'status':200}

		except Exception as e:
		
			return {'error': str(e)}

class GetUser(Resource):
	def post(self):
		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			sql = "select * from radpostauth"
			cursor.execute(sql)
			data = cursor.fetchall()

			if(len(data)>0):
				return {'status':200,'UserId':str(data[0][0])}
		except Exception as e:
			return {'error': str(e)}

api.add_resource(CreateUser, '/adduser')
api.add_resource(GetUser, '/getuser')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


