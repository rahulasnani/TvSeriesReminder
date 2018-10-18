

*/Requirements:
1) Install Python 3 or newer
2) Install pip 
3) Install all the dependencies required.
4) User should create database "Scraper" in MySql before any queries. Name can be Changed in config file.
5) User should create table "Scraper" with feilds ( email Varchar(100) , shows Varchar(1000) ) to store email and series entered.
6) User should provide email id and password in config file to send email or it will throw error.
7) User should provide this app permission by going to security feild and give access to less security app.
/*

*/Description:
The program uses web-scrapping written in python.
Its finds out IMDB id of the TV series and scraps out the TV show site.
Its then scraps out the latest season of the given tv series and compares today's
date with list of dates.
And at last sends you the mail of the tv series provided and next episode date.
Email address and Shows entered by person is entered in Table..
/*
