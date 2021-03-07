from flask import Flask, jsonify
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import numpy as np

engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

# Create FLask 
app = Flask(__name__)

# list of app routes
@app.route("/")
def Welcome():
        """list all available API routes"""
        return(
            f"Available Routes:<br/>"
            f"/api/precipitation<br/>"
            f"/api/stations<br/>"
            f"/api/tobs<br/>"
            f"/api/datesearch_startdate/<start><br/>" 
            f"/api/datesearch_startdate_enddate/<start>/<end><br/>"
        )

    
#APP Route- PRECIPITATION

@app.route("/api/precipitation")
def precipitation():
    """Return the JSON representation of the dictionary result from the query"""
  
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()
    one_year = last_date - dt.timedelta(days=365)
    
    results = session.query(Measurement.date,Measurement.prcp).\
    filter(Measurement.date >= one_year).all()

    dictreturn = dict(results)

    return jsonify(dictreturn)

#APP Route-Stations

@app.route("/api/stations")
def stations():
    """Return the JSON list of stations"""

    results = session.query(Station.name).all()
    
    return jsonify(results)


#APP Route- Temperature

@app.route("/api/tobs")
def temperature():
    """Return the JSON representation of the dictionary result from the query"""
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = dt.datetime.strptime(last_date[0], '%Y-%m-%d').date()
    one_year = last_date - dt.timedelta(days=365)
    
    
    results = session.query(Measurement.tobs,Measurement.date).\
    filter(Measurement.date >= one_year).all()

    dictreturn = dict(results)

    return jsonify(dictreturn)

#APP Route- search start date
@app.route("/api/datesearch_startdate/<start>")
def start(startDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= startDate).group_by(Measurement.date).all())

    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)

# APP Route- end date
@app.route("/api/datesearch_startdate_enddate/<start>/<end>")
def startEnd(startDate, endDate):
    sel = [Measurement.date, func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

    results =  (session.query(*sel).filter(func.strftime("%Y-%m-%d", Measurement.date) >= startDate).filter(func.strftime("%Y-%m-%d", Measurement.date) <= endDate).group_by(Measurement.date).all())

    dates = []                       
    for result in results:
        date_dict = {}
        date_dict["Date"] = result[0]
        date_dict["Low Temp"] = result[1]
        date_dict["Avg Temp"] = result[2]
        date_dict["High Temp"] = result[3]
        dates.append(date_dict)
    return jsonify(dates)

if __name__ == "__main__":
    app.run(debug=True)