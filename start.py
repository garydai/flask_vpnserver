from flask import Flask
from flask_restful import Resource, Api
from flask.ext.mysql import MySQL
from flask_restful import reqparse
import datetime
mysql = MySQL()
app = Flask(__name__)

# MySQL configurationsU
app.config['MYSQL_DATABASE_USER'] = 'daitechang'
app.config['MYSQL_DATABASE_PASSWORD'] = 'zhulong123'
app.config['MYSQL_DATABASE_DB'] = 'radius'
app.config['MYSQL_DATABASE_HOST'] = '42.96.152.105'


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
			sql = "select * from radcheck where username = '%s'" % str(userId)
			cursor.execute(sql)
			data = cursor.fetchall()
			if len(data) == 0:

				sql = "insert into radcheck (username, attribute, op, value, dsttime) VALUES ('%s', 'Cleartext-Password', ':=', 'gagatechang', '%s') " % (userId, (datetime.datetime.now() + datetime.timedelta(days=31)).strftime("%Y-%m-%d %H:%M")) 
				print sql
				cursor.execute(sql)
				conn.commit()
			return {'statusCode':200}

		except Exception as e:
			print str(e)		
			return {'error': str(e)}

class GetUser(Resource):
	def post(self):
		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			parser = reqparse.RequestParser()
			parser.add_argument('userid', type=str)
			args = parser.parse_args()
			userId = args['userid']
			if userId is None:
				return {'error': 'no userid'}
			sql = "select * from radcheck where username = '%s'" % str(userId)
			cursor.execute(sql)
			data = cursor.fetchall()
			ret = {}
			if len(data) > 0:
				for r in data:
					ret['username'] = r[0]
					ret['dsttime'] = r[5].strftime("%Y-%m-%d %H:%M")
                        return {'statusCode':200, 'data':ret}
		except Exception as e:
			return {'error': str(e)}

class GetServer(Resource):
	def post(self):
		try:
			conn = mysql.connect()
			cursor = conn.cursor()
			sql = "select * from server"
			cursor.execute(sql)
			data = cursor.fetchall()
			ret = []
			print 11111111
			if len(data) > 0:
				for r in data:
					tmp = {} 
					tmp['id'] = r[0]
					tmp['ip'] = r[1]
					tmp['name'] = r[2]
					tmp['source'] = r[3]
					ret.append(tmp)
			parser = reqparse.RequestParser()
			parser.add_argument('userid', type=str)
			args = parser.parse_args()
			userId = args['userid']
			print userId
			if userId is None:
				return {'error': 'no userid'}
			sql = "select * from radcheck where username = '%s'" % str(userId)
			cursor.execute(sql)
			data = cursor.fetchall()
			user = {}
			if len(data) > 0:
				for r in data:
					user['username'] = r[0]
					user['dsttime'] = r[5].strftime("%Y-%m-%d %H:%M")


			server = {'server':ret, 'user':user}
			
			return {'statusCode':200, 'data':server}
		except Exception as e:
			print str(e)
			return {'error': str(e)}

		
api.add_resource(CreateUser, '/adduser')
api.add_resource(GetUser, '/getuser')
api.add_resource(GetServer, '/getserver')
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)


