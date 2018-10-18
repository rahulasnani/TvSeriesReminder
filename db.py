import pymysql
import config

class Database:
	
	def __init__(self , email , series):

		try:
			#Open the connection To database.
			self.server = pymysql.connect(config.host , config.user , config.password , config.database)
			#insert into table..
			self.Insert(email , series)
		except:
			print("Connection To Database Failed")
						

	def Insert(self , email , series):
			
			#Sql Query..
			sql = "INSERT INTO Scraper ( email , shows ) VALUES ( '" + email + "' , '" + series + "'  )"

			#Cursor Object..
			cursor = self.server.cursor()

			try:
				#Execute The Sql Command
				cursor.execute(sql)
				self.server.commit()

			except:
				self.server.rollback()						