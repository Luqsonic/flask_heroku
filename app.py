#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, jsonify
import flask
from markupsafe import escape
import mysql.connector
import datetime
import aiohttp
import asyncio
import time
import pyrebase
import requests
import urllib
from bs4 import BeautifulSoup

path = "https://api.themoviedb.org/3/movie/popular?api_key=444475b4c1d215a09c24f515f81bc480&language=en-US"
'''
mydb = mysql.connector.connect(
  host="sql11.freesqldatabase.com",
  user="sql11448553",
  password="U6iE1naJxw",
  database="sql11448553"
)
mycursor = mydb.cursor(dictionary=True)
'''

firebaseConfig = {
"apiKey": "AIzaSyAIQGCuY3Ut3isKR8PJBUvhJSxNk9fBr0Y",
"authDomain": "blackbox-cinema.firebaseapp.com",
"databaseURL": "https://blackbox-cinema-default-rtdb.firebaseio.com",
"projectId": "blackbox-cinema",
"storageBucket": "blackbox-cinema.appspot.com",
"messagingSenderId": "745958747978",
"appId": "1:745958747978:web:355817289cd91ee6f29bb3",
"measurementId": "G-9JQ7K4NXPT"
};


db = pyrebase.initialize_app(firebaseConfig)

myDB = db.database()

def findAndDownload(movie,tmdb):
	encoded_movie = urllib.parse.quote(movie)
	link = f"https://www.uwatchfree.ph/?s={encoded_movie}&submit=Search"   		
	uw_search = requests.get(link).text
	uw_soup = BeautifulSoup(uw_search,'lxml')
	search_result = uw_soup.find("div", id="content")
	articles = search_result.find_all("article")
	magnet_link = ""
	for article in articles:		 
		 f_name = article.find("h2").a.get("title").replace("Watch ","")
		 f_name = f_name[0:-7]
		 #print(f_name)
		 f_link = article.find("h2").a.get("href")
		 if "Hindi" not in f_name and f_name == movie:
		  	f_scrap = requests.get(f_link).text
		  	f_soup = BeautifulSoup(f_scrap,'lxml')
		  	magnet_link = f_soup.find("div",class_="magnet-link").a.get("href")
		  	data = {"tmdb_id":tmdb,"Link":magnet_link}
		  	reqs = myDB.child("Movie_Requests").get().each()
		  	try:
		  		if len(reqs)>0:
		  			req_id = "Request_"+str(len(reqs)+1)
		  		else:
		  			req_id = "Request_0"
		  	except:
		  		req_id = "Request_0"
		  	myDB.child("Movie_Requests").child(req_id).set(data)	
		  	
		  	result = {"result":"Positive"}
		  	myJSON = jsonify(result)
		  	myJSON.headers["Content-Type"] = "application/json; charset=utf-8"
		  	#myJSON.headers["Transfer-Encoding"] = "chunked"
		  	myJSON.headers["Connection"] = "keep-alive"
		  	myJSON.headers["Access-Control-Allow-Origin"] = "*"
		  	myJSON.headers["Access-Control-Allow-Methods"] = "GET"
		  	myJSON.headers["Access-Control-Expose-Headers"] = "ETag, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After, Content-Length, Content-Range"
		  	myJSON.headers["Access-Control-Allow-Origin"] = "*"		
		  	
		  	return myJSON
		 else:
		  	result = {"result":"Negative"}
		  	myJSON = jsonify(result)
		  	myJSON.headers["Content-Type"] = "application/json; charset=utf-8"
		  	#myJSON.headers["Transfer-Encoding"] = "chunked"
		  	myJSON.headers["Connection"] = "keep-alive"
		  	myJSON.headers["Access-Control-Allow-Origin"] = "*"
		  	myJSON.headers["Access-Control-Allow-Methods"] = "GET"
		  	myJSON.headers["Access-Control-Expose-Headers"] = "ETag, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After, Content-Length, Content-Range"
		  	myJSON.headers["Access-Control-Allow-Origin"] = "*"		
		  	
		  	return myJSON
		 	
			
	 	 			

app = Flask(__name__)
@app.route('/')
def main_page():
    response = flask.Response()
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response
  
@app.route('/bbox/<page_number>')
def home_fetch(page_number):
    # show the user profile for that user
    #return f'User {escape(username)}'
    path1 = "https://api.telegram.org/bot1079071502:AAEkBVB1xvsy6TBSun0BLvHctY_hqrbhxOs"
    index = page_number-1 if isinstance(page_number, int) else int(page_number)-1
    
    #return('Boommsnsn')
    collect_rows = myDB.child("Movie_Storage").get().each()
    #mycursor.execute("SELECT * FROM `Movie_Storage` ORDER BY id DESC")
    #collect_rows = mycursor.fetchall()
    c = []
    if len(collect_rows)>0:
    	for r in collect_rows:
    		movie_id = r.val()["movie_id"]
    		poster = r.val()["poster"]
    		date = r.val()["date"]
    		
    		fulldate = datetime.datetime.now()
    		today = str(fulldate.year)+str(fulldate.month)+str(fulldate.day)
    		
    		if date==today:
    			timestamp="New"
    		else:
    			timestamp="Old"
    			
    		obj = {"id":movie_id,"poster":poster,"timestamp":timestamp}
    		c.append(obj)
    		
    		
    pages = []
    async def main():
    		  	async with aiohttp.ClientSession() as session:
    		  	   for number in range(1, 11):
    		  	   	tmdb_url = f'{path}&page={number}'
    		  	   	async with session.get(tmdb_url) as resp:
    		  	   	   page = await resp.json()
    		  	   	   pages.append(page)
    		  	   	   #print(page['page'])
    		  	   	   #print(pages)
    asyncio.run(main())
    		
    tmdb = []
    for page in pages:
    			for m in page["results"]:
    				m_id = m["id"]
    				poster_path = m["poster_path"]
    				poster = "https://www.themoviedb.org/t/p/w780/"+poster_path
    				obj = {"id":m_id,"poster":poster,"timestamp":"Old"}
    				
    				tmdb.append(obj)
    				
    
    	
    r = []
    ids = []
    for p in c:
    	r.append(p)
    	ids.append(p['id'])
    		
    for m in tmdb:
    	if m["id"] not in ids:
    		r.append(m)
    		    		
    def breakdown(lst):
   	 chunks = []
   	 for i in range(0, len(lst), 25):
    		chunks.append(lst[i:i + 25])
   	 return chunks
    		
    chunk = breakdown(r)
    
    final_res = chunk[index]
    tt_pages = len(chunk)
    tt_results = len(r)
    		
    result = {"page":page_number,
    		"results":final_res,
    		"total_pages":tt_pages,
    		"total_results":tt_results
    		};
    		
    myJSON = jsonify(result)
    myJSON.headers["Content-Type"] = "application/json; charset=utf-8"
    #myJSON.headers["Transfer-Encoding"] = "chunked"
    myJSON.headers["Connection"] = "keep-alive"
    myJSON.headers["Access-Control-Allow-Origin"] = "*"
    myJSON.headers["Access-Control-Allow-Methods"] = "GET"
    myJSON.headers["Access-Control-Expose-Headers"] = "ETag, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After, Content-Length, Content-Range"
    		
    myJSON.headers["Access-Control-Allow-Origin"] = "*"		
    return myJSON

@app.route('/fetchlinks/<movie>')
def link_fetch(movie):
    			  res = myDB.child("NewLinks").get().each()
    			  collect_rows = []
    			  for link in res:
    			  	if link.val()['movieId'].startswith(movie):
    			  		collect_rows = link.val()		  	
    			  
    			  #mycursor.execute(f"SELECT * FROM `NewLinks` WHERE movieId LIKE '{movie}%'")
    			  #collect_rows = mycursor.fetchall()
    			  c = []
    			  finalResult = []
    			  if len(collect_rows)>0:
    			  	
    			  	for a in collect_rows:
    			  		movieId = a['movieId']
    			  		link_name = a['link_name']
    			  		file_size = a['file_size']
    			  		link_url = a['link_url']
    			  		link_id = a['link_id']
    			  		
    			  		obj = {"id":movieId,"link_name":link_name,"file_size":file_size,"link_url":link_url,"link_id":link_id}
    			  		c.append(obj)
    			  	found = "positive"
    			  	finalResult = {"found":found,"result":c}
    			  else:
    			  	movieId = movie
    			  	link_name = 'Not Available'
    			  	file_size = 'Unknown'
    			  	link_url = '#'
    			  	fulldate = datetime.datetime.now()
    			  	link_id = str(fulldate.year)+str(fulldate.month)+str(fulldate.day)
    			  	
    			  	obj = {"id":movieId,"link_name":link_name,"file_size":file_size,"link_url":link_url,"link_id":link_id}
    			  	found = "negative"
    			  	finalResult = {"found":found,"result":{obj}}
    			  
    			  myJSON = jsonify(finalResult)
    			  myJSON.headers["Content-Type"] = "application/json; charset=utf-8"
    			  #myJSON.headers["Transfer-Encoding"] = "chunked"
    			  myJSON.headers["Connection"] = "keep-alive"
    			  myJSON.headers["Access-Control-Allow-Origin"] = "*"
    			  myJSON.headers["Access-Control-Allow-Methods"] = "GET"
    			  myJSON.headers["Access-Control-Expose-Headers"] = "ETag, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After, Content-Length, Content-Range"
    			  myJSON.headers["Access-Control-Allow-Origin"] = "*"		
    			    
    			  return myJSON

@app.route('/vlink/<link_id>')
def vlink(link_id):
    			  #mycursor.execute(f"SELECT * FROM `NewLinks` WHERE link_id='{link_id}'")
    			  #collect_rows = mycursor.fetchall()
    			  res = myDB.child("NewLinks").get().each()
    			  collect_rows = []
    			  for link in res:
    			  	if link.val()['link_id']==link_id:
    			  		collect_rows = link.val()
    			  
    			  if len(collect_rows)>0:
    			  	
    			  	for a in collect_rows:
    			  		movieId = a['movieId']
    			  		link_name = a['link_name']
    			  		file_size = a['file_size']
    			  		link_url = a['link_url']
    			  		link_id = a['link_id']
    			  		subs= a['subs']
    			  		
    			  		finalResult = {"movie_link":link_url,"subs":subs}
    			  else:
    			  	movieId = "movie"
    			  	link_name = 'Not Available'
    			  	file_size = 'Unknown'
    			  	link_url = '#'
    			  	fulldate = datetime.datetime.now()
    			  	link_id = str(fulldate.year)+str(fulldate.month)+str(fulldate.day)
    			  	subs = "none"
    			  	
    			  	finalResult = {"movie_link":link_url,"subs":subs}
    			  
    			  myJSON = jsonify(finalResult)
    			  myJSON.headers["Content-Type"] = "application/json; charset=utf-8"
    			  #myJSON.headers["Transfer-Encoding"] = "chunked"
    			  myJSON.headers["Connection"] = "keep-alive"
    			  myJSON.headers["Access-Control-Allow-Origin"] = "*"
    			  myJSON.headers["Access-Control-Allow-Methods"] = "GET"
    			  myJSON.headers["Access-Control-Expose-Headers"] = "ETag, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After, Content-Length, Content-Range"
    			  myJSON.headers["Access-Control-Allow-Origin"] = "*"		
    			    
    			  return myJSON
			
@app.route('/similar/<movie_id>')
def get_similar(movie_id):
	pages = []   
	async def main():
		async with aiohttp.ClientSession() as session:
    		  	   for number in range(1, 5):
    		  	   	tmdb_url = f'https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key=444475b4c1d215a09c24f515f81bc480&language=en-US&page={number}'
    		  	   	async with session.get(tmdb_url) as resp:
    		  	   	   ret = await resp.json()    		  	   	   
    		  	   	   
    		  	   	   for rt in ret['results']:
    		  	   	   	year = int(rt['release_date'][:4])
    		  	   	   	diff = 2021-year
    		  	   	   	if diff <13:    		  	   	   			   	   	
    		  	   	   		obj = {"id":rt['id'],"backdrop_path":rt['backdrop_path']}    		  	   	   	
    		  	   	   		pages.append(obj)
	asyncio.run(main())   		  	   	   	    		  	 
	
	myJSON = jsonify(pages[:15])
	myJSON.headers["Content-Type"] = "application/json; charset=utf-8"
	myJSON.headers["Connection"] = "keep-alive"
	myJSON.headers["Access-Control-Allow-Origin"] = "*"
	myJSON.headers["Access-Control-Allow-Methods"] = "GET"
	myJSON.headers["Access-Control-Expose-Headers"] = "ETag, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After, Content-Length, Content-Range"
	return myJSON

@app.route('/moviedata/<movieId>')
def getMovieData (movieId):
	collec = []
	async def main():
		API_URL = 'https://api.themoviedb.org/3/'
		API_KEY='444475b4c1d215a09c24f515f81bc480'
		a = f'{API_URL}movie/{movieId}?api_key={API_KEY}'
		b = f'{API_URL}movie/{movieId}/credits?api_key={API_KEY}'
		c = f'https://bbox-backend.herokuapp.com/similar/{movieId}'
		d = f'https://bbox-backend.herokuapp.com/fetchlinks/{movieId}'
		comb = [a,b,c,d]
		async with aiohttp.ClientSession() as session:
    		  	   for url in comb:
    		  	   	print(url)
    		  	   	#tmdb_url = f'https://api.themoviedb.org/3/movie/{movie_id}/similar?api_key=444475b4c1d215a09c24f515f81bc480&language=en-US&page={number}'
    		  	   	async with session.get(url) as resp:
    		  	   	   ret = await resp.json() 
    		  	   	   f_ret = [ret]   		  	   	      		  	   	    		  	   	   
    		  	   	   collec.append(f_ret)
    		  	   	   		  	   	       		  	   	 
	asyncio.run(main())  	
	myJSON = jsonify(collec)
	myJSON.headers["Content-Type"] = "application/json; charset=utf-8"
	myJSON.headers["Connection"] = "keep-alive"
	myJSON.headers["Access-Control-Allow-Origin"] = "*"
	myJSON.headers["Access-Control-Allow-Methods"] = "GET"
	myJSON.headers["Access-Control-Expose-Headers"] = "ETag, X-RateLimit-Limit, X-RateLimit-Remaining, X-RateLimit-Reset, Retry-After, Content-Length, Content-Range"
	return myJSON

				
@app.route('/movie_request/<tmdb_id>')
def requested(tmdb_id):
    	movie_tmdb_id = tmdb_id
    	path = "https://api.themoviedb.org/3/"
    	api_key = "444475b4c1d215a09c24f515f81bc480"
    	movie_data = json.loads(requests.get(f"{path}movie/{tmdb_id}?api_key={api_key}&language=en-US").text)   
    	
    	movie_name = movie_data['original_title']
    	
    	findAndDownload(movie_name,tmdb_id)
	
	
				
if __name__ == '__main__':
    app.run(debug=True)
