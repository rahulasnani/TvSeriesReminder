# Please all the instructions in Readme file.

import json
import requests
import bs4
import string
import datetime
import config
import db
from dateutil.parser import parse
import dateutil.parser as parser
import mail

class Scraper:
	
	tv_series = []
	original_series = []
	running_year = []
	email_id  = ""
	imdbID    = []
	currentSeason = []
	dates = []
	dates_to_send = []

	"""docstring for Tracker"""

	def __init__(self , email_id , series):

		self.getSeriesName(series)

		self.getimdbIDs() 

		self.getSeason()

		self.Dates()

		self.datesToSend()

		mail.Mail( self.original_series , self.dates_to_send , email_id , self.running_year )

		db.Database(email_id , series )


	#Fucntion To get Array of Series
	def getSeriesName(self , series):
		show = ""
		for i in series:
			if( i != ',' ):
				if(show == "" and i == " " ):
					continue
				show += i	
			else:
				if(show != ""):
					self.tv_series.append(show)
				show = ""

		#Append the last show..
		if(show != ""):
			self.tv_series.append(show)

		# print(self.tv_series)

#Function to get the imdbIDs for given series..
	def getimdbIDs(self):	

		for show in self.tv_series:

			link = "http://www.omdbapi.com/?apikey="+config.apikey+"&type=series&t="+show
			
			try:
				#Request JSON object from the OMDB API..
				res = requests.get(link).json() 

				if(res["Response"] == "False" ):
					self.imdbID.append("-1")
					self.running_year.append("-1")
					self.original_series.append(show)
				else:					
					self.original_series.append(res["Title"])
					self.running_year.append(res["Year"])
					self.imdbID.append(res["imdbID"])
				

			except:
				#If connections fails..
				print("Error !!")
				exit()

		# print(self.imdbID)	



	#Function to get all the Current Season of the Series..
	def getSeason(self):

		for ids in self.imdbID:

			if( ids == "-1" ):
				self.currentSeason.append("-1")
				continue
		
			try:
				res = requests.get("https://www.imdb.com/title/"+ids)

				soup = bs4.BeautifulSoup(res.text , "lxml")				
				season = soup.select(".seasons-and-year-nav a")
				self.currentSeason.append(season[0].getText())
			
			except:
				self.currentSeason.append("-1")

		# print("Seasons")
		# print(self.currentSeason)


	#Function To Scrap the Latest Dates of Latest Season..
	def Dates(self):

		for show , latest_season in enumerate(self.currentSeason):

			try:
				currentseason = int(latest_season)
				latest_season = currentseason
				old_season_date = ""

				# If Show doesn't exists..
				if(latest_season == -1):
					self.dates.append("-1")
					continue					

				# Looping through lastest season to season 1...
				while(currentseason > 0):

					res = requests.get("https://www.imdb.com/title/"+self.imdbID[show]+"/episodes?season="+str(currentseason))
					
					soup = bs4.BeautifulSoup(res.text , "lxml" )
					# #Airdates of this season..
					airdates = soup.select(".airdate")

					#Remove the newlines and newlines string 
					modified_dates = self.modify(airdates)

					if (modified_dates):

						modified_dates.reverse()

						# print(modified_dates)

						date = self.getFinalDate(modified_dates)
						# print(date)
						#Check the season..
						if( latest_season == currentseason ):
							# Series has ended..
							if( date == "0" ):
								self.dates.append("0")
								break
							else:
								if(len(date) > 4 ):
									self.dates.append(date) 
									break
								else:
									#Series is showing its in next year..
									old_season_date = date

						# Season has changed..
						else:
							if(date == "0"):
								self.dates.append(old_season_date)
								break
							else:
								if( len(date) > 4 ):
									self.dates.append(date)
									break
								else:
									old_season_date = date
						

					currentseason = currentseason - 1
			except:
				self.dates.append("0")		



	def modify(self , airdates):
		dates = []

		for i in airdates:
			text_date = i.text
			text_date = text_date.strip(' \n ')

			if(text_date != ''):
				dates.append(text_date)

		return dates


	def getFinalDate(self , dates ):

		flag = 0
		now = datetime.datetime.now()

		for i,date in enumerate(dates):

			if(len(date) <= 4):
				year = int(date)
				if(now.year == year - 1):
					flag = 1				
			else:
				temp_date = parse(date).strftime("%Y-%m-%d")
				temp_date = datetime.datetime.strptime( temp_date , "%Y-%m-%d")

				if( temp_date <= now ):
					if (i != 0):
						return dates[i-1]
					else:
						return "0"

		if(flag == 1):
			return dates[0]
		else:
			return "0"	


	def datesToSend(self):

		for date in self.dates:
			if( len(date) < 5 ):
				self.dates_to_send.append(str(date) )
			else:
				self.dates_to_send.append( str( parse(date).strftime("%Y-%m-%d") ) )


################################################################################################
################################################################################################	
################################################################################################
#Driver For the Program

print("Hello User Enter Your Email Id :")
email_id = input()
#TV Series 
print("Please Enter The TV Series (separated by Commas) : ")
series = input()

query = Scraper(email_id,series)
