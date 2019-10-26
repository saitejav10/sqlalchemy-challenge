import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect, func
from flask import Flask, jsonify
import datetime as dt
import numpy as np


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def hawaii():
    """List all available api routes."""
    return (
         f"Avalable Routes:<br/>"
         f"/api/v1.0/precipitation<br/>"
         f"- Dates and Temperature for all dates<br/>"
         f"/api/v1.0/stations<br/>"
         f"- List of weather stations from the dataset<br/>"
         f"/api/v1.0/tobs<br/>"
         f"- List of temperature observations (tobs) for the previous year (8/23/2016 - 8/23/2017)<br/>"
         f"/api/v1.0/<start><br/>"
         f"- List of the minimum temperature, the average temperature, and the max temperature for a given start<br/>"
         f"/api/v1.0/<start>/<end><br/>"
         f"- List of the minimum temperature, the average temperature, and the max temperature for a given start-end range<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all measurement dates and precipitations"""
    # Query all 
    results = session.query(Measurement.date, Measurement.prcp).all()
    
     # Create a dictionary 
    all_prcp = []
    for result in results:
        measurement_dict = {}
        measurement_dict["date"] = result[0]
        measurement_dict["prcp"] = result[1]

        all_prcp.append(measurement_dict)

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all 
    results = session.query(Station.station).all()

    # Create a list 
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of measurement dates and tobs for last year"""
    # Query all 
    results = session.query(Measurement.date, Measurement.tobs).\
        group_by(Measurement.date).filter(Measurement.date <= '2017-8-23').filter(Measurement.date >= '2016-08-23').all()

    lastyear_tobs = list(np.ravel(results))
    
    return jsonify(lastyear_tobs)


@app.route("/api/v1.0/<start>")
def start(start):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """List of the minimum temperature, the average temperature, and the max temperature for a given start"""
    start_date = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    end_date =  dt.date(2017, 5, 10)
    temp_range = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    temp = list(np.ravel(temp_range))
    
    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def both_dates(start,end):

    """List of the minimum temperature, the average temperature, and the max temperature for a given start-end range"""     
    start_date = dt.date(2017, 5, 1)
    end_date =  dt.date(2017, 5, 10)
    temp_range = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
    
    temp = list(np.ravel(temp_range))
    
    return jsonify(temp)

if __name__ == '__main__':
    app.run(debug=True)
