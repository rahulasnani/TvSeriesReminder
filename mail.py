import smtplib
import config
import datetime

class Mail:


	def __init__(self , series , dates , email , year):

		self.mail = smtplib.SMTP("smtp.gmail.com",587)
		self.mail.ehlo()
		self.mail.starttls()

		#Login now..
		try:
			self.mail.login(config.email_address , config.email_password )
			self.myMessage(series , dates , year)
			# self._sendEmail = self.send(self.answer , email)

		except:
			print("Please Enter the valid username and password")

		self.send(email)
	
	def myMessage( self , tv_series , dates , years ):
		
		self.answer = "\n"

		for i , show in enumerate(tv_series):
			self.answer += "TV series : " + show + "\n"

			#If this is invalid series..
			if(dates[i] == '-1'):
				self.answer += "Wrong TV series \n\n"
				continue
			
			#If we dont have latest date on next episode..
			if(dates [i] == '0'):
				if( len(years[i]) < 6 ):
					self.answer += "The Last season ended recently. No information on upcoming episodes.\n\n"
				else:
					if( (years[5:]) == str(datetime.datetime.now().year) ):
						self.answer += "The Last season ended recently. No information on upcoming episodes.\n\n"
					else:		
						self.answer += "The show has finished streaming all its episodes.\n\n"
				continue		

			#We have the date..
			if(len(dates[i]) < 5):
				self.answer += "The next season begins in "	+ dates[i] + "\n\n"
			else:
				self.answer += "The next episode airs on " + dates[i] + "\n\n"

	
	def send(self , email ):

		try:
			self.mail.sendmail(config.email_address , email , self.answer)
			print("Plese Check your email")
		except:
			print("Please Provide a Valid Email-id")	

		self.mail.close()
