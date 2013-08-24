from flask import Flask, render_template
app = Flask(__name__)
app.debug = True

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/ranking")
def ranking():
    top_hour = {"Mikey Mouse" : 100, "Aloha!": 50, "Random Process":30}
    return render_template('ranking.html', top_hour = top_hour)

if __name__ == "__main__":
    #app.run(host = '0.0.0.0')
    app.run(host = 'localhost')
