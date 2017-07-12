from flask import Flask, render_template, request
from twiter_db_interact import User, makeDB
from collections import Counter
from datetime import datetime, timedelta
import json



app = Flask(__name__)

@app.route('/')
def result():
   a1=[]
   a2=[]
   a=[]
   # connect('mydb')
   for post in User.objects(search="analytics"):
      dt = datetime.strptime(post.date.strftime('%Y-%m-%d'), '%Y-%m-%d')
      a.append((dt - timedelta(days=dt.weekday())).strftime('%Y-%m-%d'))
      a1.append(post.date.strftime('%Y-%m-%d'))

   a3=Counter(a1)
   aggregate_date=dict(Counter(a))

   for post in User.objects(search="analytics"):
      a2.append(post.location)
   x= Counter(a2)

   tot= sum(x.values())
   for y in x.keys():
      if y==None:
         x['Unknown']=x.pop(y)
         y='Unknown'
      x[y]=(x[y]/float(tot))*100


   a4=map(list,x.items())

   return render_template('page1.html', result = dict(a3), pie = a4, result2=aggregate_date)

@app.route('/page2',methods = ['POST'])
def result_twiter():
   if request.method == 'POST':
      word = request.form.get("word","")
      d = []
      if(word):
         makeDB(word)
         for entry in list(User.objects(search=word)):
            d.append({"name":entry.name,"text":entry.text,"date":entry.date.strftime('%Y-%m-%d'),"location":entry.location})
      return render_template("page2.html",data=json.dumps(d),data_keys=[{ "title": "Name" },{ "title": "Tweet"},{ "title": "Date"},{ "title": "Location"}])

if __name__ == '__main__':
   app.run(host='0.0.0.0',debug = True)
