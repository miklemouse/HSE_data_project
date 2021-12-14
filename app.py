from flask import Flask, render_template, send_file, request
import matplotlib.pyplot as plt

import pandas as pd

import time

app = Flask(__name__)

links = {"Download" : "/download",
         "View Raw Data" : "/view_data",
         "Survived" : "/survived"}


def render_index (image=None, html_string=None, filters=None,  errors=None, current_filter_value=""):
    return render_template("index.html", links=links, image=image, code=time.time(), html_string=html_string,
                           filters=filters, errors=errors, current_filter_value=current_filter_value)

@app.route('/', methods=['GET'])
def main_page():
    return render_index()

@app.route(links["Download"], methods=['GET'])
def download_data():
    return send_file("data/titanic_train.csv", as_attachment=True)

@app.route(links["View Raw Data"], methods=['GET', 'POST'])
def view_data():
    df = pd.read_csv("data/titanic_train.csv")
    errors = []
    current_filter_value = ""
    if request.method == "POST":
        current_filter = request.form.get('filters')
        current_filter_value = current_filter
        if current_filter:
            try:
                df = df.query(current_filter)
            except Exception as e:
                errors.append('<font color="red">Incorrect filter</font>')
                print(e)

    html_string = df.to_html()
    return render_index(html_string=html_string, filters=True, errors=errors, current_filter_value=current_filter_value)

@app.route(links["Survived"], methods=['GET'])
def survived():
    import plotly.express as px
    import pandas as pd
    data = pd.read_csv('data/titanic_train.csv')
    data["new"] = data["Sex"] + data["Survived"].astype(str)
    f = data["new"].value_counts()
    plot = px.pie(values=f.values, names=f.index)
    return render_index(html_string = plot.to_html(full_html=False, include_plotlyjs='cdn'))


if __name__ == '__main__':
    app.run()
