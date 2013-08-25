from flask import Flask, render_template, Markup
import redis
import urllib2

redis_name_dest = "wiki:hourly_page_view"
app = Flask(__name__)
app.debug = True

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/ranking")
def ranking():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
    r = redis.Redis(connection_pool = pool)
    redis_dest = r.lpop(redis_name_dest)
    r.lpush(redis_name_dest, redis_dest)
    print r.zcard(redis_dest)
    tmp = r.zrange(redis_dest, 9950, 10000,  withscores=1)
    #for x in tmp:
    #    print urllib2.unquote(x[0])
    top_list = [(x[0], int(x[1])) for x in reversed(tmp)]
    return render_template('ranking.html', top_hour = top_list)

if __name__ == "__main__":
    app.run(host = '0.0.0.0')
    #app.run(host = 'localhost')
