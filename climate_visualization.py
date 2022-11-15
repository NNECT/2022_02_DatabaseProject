from flask import Flask, render_template, request, escape
from flask_cors import cross_origin
import pandas as pd
from datetime import datetime

app = Flask(__name__)


@app.route("/")
@app.route("/home")
def page_main():
    return render_template('index.html')


def main():
    app.run()
    # app.run(debug=True)
    # app.run(host="0.0.0.0", debug=True)


if __name__ == "__main__":
    main()
