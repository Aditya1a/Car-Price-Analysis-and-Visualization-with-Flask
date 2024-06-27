from flask import Flask, render_template,request
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


app = Flask(__name__)
data = pd.read_csv("car_prices.csv")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/search", methods=["GET","POST"])
def search():
    if request.method == "POST":
        yea = request.form.get("year")
        make = request.form.get("company")
        model = request.form.get("model")
        body = request.form.get("body")
        color = request.form.get("color")
        transmission = request.form.get("transmission")
        # return f"{year},{make}, {model}"
        dt = data.copy()


        # if yea == None or " ":
        #     condition1 = True
        # else:
        #     condition1 = dt["year"] == eval(yea)
        # if make == None or " ":
        #     condition2 = True
        # else:
        #     condition2 = dt["make"].apply(lambda x: True if (make).lower() in str(x).lower() else False)

        # if model == " " or None:
        #     condition3 = True
        # else:
        #     condition3 = dt["model"].apply(lambda x:True if (make).lower() in str(x).lower() else False)


        # new_d =  dt[(condition1) & (condition2) & (condition3) ]
        # return new_d.to_html()
        if yea:
            
            dt = dt[dt["year"] ==eval(yea)]
        if make:
            # global dt
            dt = dt[dt["make"].apply(lambda x:True if (make).lower() in str(x).lower() else False)]
        if model:
            # global dt
            dt = dt[dt["model"].apply(lambda x:True if (model).lower() in x.lower() else False)]
        if body:
            dt = dt[dt["body"].apply(lambda x:True if (body).lower() in str(x).lower() else False)]
        if color:
            dt = dt[dt["color"].apply(lambda x:True if (color).lower() in str(x).lower() else False)]
        if transmission:
            dt = dt[dt["transmission"].apply(lambda x:True if (transmission).lower() in str(x).lower() else False)]

        new_d = dt.to_dict(orient="records")

        # return dt.to_html()
        # return render_template("portfolio-details.html", data= new_d)
        return render_template("portfolio-details.html", data = new_d)

@app.route("/plots", methods= ["GET","POST"])
def plots():
    if request.method == "POST":
        plot = request.form.get("plot")
        value = request.form.get("value")
        print(plot, value)
        
        # return f"{plot}, {value}"
    
        if plot == "bar":
            i = data[value].value_counts()[:10].index
            v = data[value].value_counts()[:10].values
            file_name = f"static/assets/img/{value}_{plot}.jpg"
            plt.figure()
            sns.barplot(x = i, y=v)
            plt.xticks(rotation=90)
            plt.title(f"Top 10 {value} barplot")
            plt.xlabel(f"{value}")
            plt.ylabel("Count")
            plt.savefig(file_name, bbox_inches = 'tight')

            return render_template("index.html", img = "../"+file_name)
        elif plot == "pie":
            i = data[value].value_counts()[:10].index
            v = data[value].value_counts()[:10].values
            file_name = f"static/assets/img/{value}_{plot}.jpg"
            plt.figure()
            plt.pie(x = v, labels=i, autopct="%0.1f")
            plt.title(f"Top 10 {value} pieplot")
            plt.savefig(file_name, bbox_inches = 'tight')
            print("exit pie")
            return render_template("index.html", img = "../"+file_name)
        elif plot == "hist":
            plt.figure()
            sns.histplot(data[value])
            file_name = f"static/assets/img/{value}_{plot}.jpg"
            plt.title(f"Distribution of {value}")
            plt.savefig(file_name, bbox_inches = 'tight')

            return render_template("index.html", img = "../"+file_name)
        elif plot == "line":
            plt.figure()
            sns.lineplot(x = data[value].value_counts()[:20].index , y = data[value].value_counts()[:20].values)
            file_name = f"static/assets/img/{value}_{plot}.jpg"
            plt.title(f"Top 20  {value} lineplot")
            plt.xticks(rotation=90)
            plt.savefig(file_name, bbox_inches = 'tight')

            return render_template("index.html", img = "../"+file_name)
        
        elif plot == "scatter":
            plt.figure()
            i = data[value].value_counts()[:20].index
            v = data[value].value_counts()[:20].values
            file_name = f"static/assets/img/{value}_{plot}.jpg"
            sns.scatterplot(x= i, y =v)
            plt.xticks(rotation=90)
            plt.title(f"Top 20 {value} scatter plot")
            plt.savefig(file_name, bbox_inches = 'tight')

            return render_template("index.html", img = "../"+file_name)


@app.route("/blog")
def blog():
    return render_template("portfolio-details.html")      


            

if __name__ =="__main__":
    app.run(debug=True)