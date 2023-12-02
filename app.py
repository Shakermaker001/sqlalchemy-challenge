# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import pandas as pd
import datetime as dt

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save reference to the table
station = Base.classes.station
measurement = Base.classes.measurement
date = dt.datetime(2016, 8, 23)

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """Welcome to the QueryZone"""
    return (
        f"Welcome to the QueryZone:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def rainfall():
     
    results = session.query(measurement.date,measurement.prcp).filter(measurement.date >= date).all()

    session.close()
    
    rainy_days = []
    
    for day, precipitaion in results:
        rainy_dict = {}
        rainy_dict[day] = precipitaion
        rainy_days.append(rainy_dict)
    
    return jsonify(rainy_days)

@app.route("/api/v1.0/stations")
def stations():

    stations = session.query(station.station).all()

    session.close()

    stations = [tuple(row) for row in stations]

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def USC00519523():
    'Most Active Station'

    temp_records = session.query(measurement.station,measurement.tobs)\
    .filter(measurement.date >= date, measurement.station == 'USC00519523').all()

    temp_records = [tuple(row) for row in temp_records]

    session.close()

    
    return jsonify(temp_records)

@app.route("/api/v1.0/start")
def start():

    start_date = dt.datetime(2016, 9, 17)
    temps = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

    temp_trends = session.query(*temps).filter(measurement.date >= start_date).all()

    temp_trends = [tuple(row) for row in temp_trends]
    
    session.close()

    return jsonify(temp_trends)

@app.route("/api/v1.0/start/end")
def start_end():
    
    
    start_date = dt.datetime(2016, 9, 17)
    end_date = dt.datetime(2017, 3, 17)
    temps = [func.min(measurement.tobs), func.max(measurement.tobs), func.avg(measurement.tobs)]

    temp_trends = session.query(*temps).filter(measurement.date >= start_date, measurement.date <= end_date).all()

    temp_trends = [tuple(row) for row in temp_trends]
    
    session.close()

    return jsonify(temp_trends)


    


if __name__ == '__main__':
    app.run(debug=True)
      