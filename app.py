# import necessary libraries
from sqlalchemy import func

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#CORS protective mechanism is on by default, guards against people stealing your API
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, func, inspect
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
import json

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

#app.config['SQLALCHEMY_DATABASE_URI'] = "postgres:092408Op@localhost:5432/Project 2"
#Connecting to the postgres db
connection_string = "postgres:092408Op@localhost:5432/Project 2"
engine = create_engine(f'postgresql://{connection_string}')
inspector = inspect(engine)
print(inspector.get_table_names())

Base = automap_base()
Base.prepare(engine,reflect=True)
print(Base.classes.keys())
IL_county = Base.classes.IL_county


# Homepage
@app.route("/")
def home():
    return render_template("SakiPlot/index.html")

@app.route("/county")
def local():
    return "County"

# create route that returns data for plotting
@app.route("/api")
@cross_origin()
def County():
 
    session = Session(engine)

    allResults = session.query(IL_county).all()

    session.close()
#Taking the County Objects to convert it to a Dictionary of key value pairs between the columns and their corresponding values for each county.
    countyList = (county.__dict__ for county in allResults)
    allDicts = []
    #for loop thorugh each county
    for county in countyList:
        #dictionary comprehension similar to list comprehension
        withoutInstanceState = { k:county[k]  for k in county if k != "_sa_instance_state" }
        allDicts.append(withoutInstanceState)

    return jsonify(allDicts)
   
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5002)
