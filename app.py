#!/usr/bin/env python
# encoding: utf-8
import json
from flask import Flask, jsonify
from markupsafe import escape
import mysql.connector
import datetime
import aiohttp
import asyncio
import time

mydb = mysql.connector.connect(
  host="sql11.freesqldatabase.com",
  user="sql11448553",
  password="U6iE1naJxw",
  database="sql11448553"
)
mycursor = mydb.cursor(dictionary=True)

#mycursor.execute("SELECT * FROM New_Movies")
'''
myresult = mycursor.fetchall()
print(len(myresult))
j = []
for x in myresult:
    		movie_id = x['id']
    		poster = x["movie"]
    		date = x["link"]
    		
    		fulldate = datetime.datetime.now()
    		today = str(fulldate.year)+str(fulldate.month)+str(fulldate.day)
    		
    		if date==today:
    			timestamp="New"
    		else:
    			timestamp="Old"
    			
    		obj = {"id":movie_id,"poster":poster,"timestamp":"timestamp"}
    		j.append(obj)
print(j)
print(j[0]["poster"])
'''
app = Flask(__name__)
@app.route('/')
def main_page():
    return jsonify({'name': 'alice',
                    'email': 'alice@outlook.com'})

@app.route('/bbox/<page_number>')
def show_user_profile(page_number):
    # show the user profile for that user
    #return f'User {escape(username)}'
    path = "https://api.themoviedb.org/3/movie/popular?api_key=444475b4c1d215a09c24f515f81bc480&language=en-US"
    path1 = "https://api.telegram.org/bot1079071502:AAEkBVB1xvsy6TBSun0BLvHctY_hqrbhxOs"
    index = page_number-1 if isinstance(page_number, int) else int(page_number)-1
    
    #return('Boommsnsn')
    
    mycursor.execute("SELECT * FROM `Movie_Storage` ORDER BY id DESC")
    collect_rows = mycursor.fetchall()
    c = []
    if len(collect_rows)>0:
    	for r in collect_rows:
    		movie_id = r["movie_id"]
    		poster = r["poster"]
    		date = r["date"]
    		
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
    		
    return myJSON

 
    			
if __name__ == '__main__':
    app.run(debug=True)
