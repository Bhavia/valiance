from TwitterAPI import TwitterAPI, TwitterOAuth, TwitterRestPager
from mongoengine import *
from datetime import datetime
import calendar
connect('mydb')
class User(Document):
    U_id = DecimalField()
    name = StringField(max_length=50)
    text = StringField()
    date = DateTimeField()
    location = StringField(max_length=100)
    search = StringField()

def makeDB(word='analytics'):
    o = TwitterOAuth.read_file()
    api = TwitterAPI(o.consumer_key,o.consumer_secret,o.access_token_key,o.access_token_secret)
    r = TwitterRestPager(api, 'search/tweets', {'q': word,'count':100})



    d=dict((v,k) for k,v in enumerate(calendar.month_abbr))
    try:
        flag = 0
        for item in r.get_iterator():
            if flag ==100:
                break
            flag+=1
            obj = User(U_id = item['user']['id'])
            obj.name = item['user']['screen_name']
            obj.location = item['user']['time_zone']
            x=list(map(str,item['user']['created_at'].split(' ')))
            obj.date = datetime.strptime(x[2] + str(d[x[1]]) + x[-1], "%d%m%Y").date()
            obj.text = item['text']
            obj.search = word
            obj.save()
    except:
        print "Request cannot be served due to the application's rate limit having been exhausted for the resource"

if __name__ == '__main__':
    makeDB()

