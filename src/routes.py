from flask import Flask, render_template
app = Flask(__name__)
app.debug = True

@app.route("/")
def home():
    return render_template('home.html')

@app.route("/ranking")
def ranking():
    return render_template('ranking.html')

if __name__ == "__main__":
    app.run(host = '0.0.0.0')
