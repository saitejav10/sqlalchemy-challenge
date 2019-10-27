import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime
from flask import Flask, jsonify
import datetime as dt

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
        f"Available Routes:<br/>"
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
    """Return a list"""
    # Query all 
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    # Create a list of dicts with `date` and `prcp` as the keys and values
    all_prcp = []
    for date, prcp in results:
        measurement_dict = {}
        measurement_dict[date] = prcp

        all_prcp.append(measurement_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all stations"""
    # Query all 
    results = session.query(Station.station).all()
    session.close()

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

    session.close()

    lastyear_tobs = list(np.ravel(results))
    
    return jsonify(lastyear_tobs)

@app.route('/api/v1.0/<start>')
def start(start):
    session = Session(engine)

 # Min/Avg/Max temp   
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    temp_range = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()
    
    session.close()

    temp = list(np.ravel(temp_range))
    
    return jsonify(temp)

@app.route("/api/v1.0/<start>/<end>")
def range(start,end):
    session = Session(engine)
  # Min/Avg/Max temp     
    start_date= dt.datetime.strptime(start, '%Y-%m-%d')
    end_date= dt.datetime.strptime(end,'%Y-%m-%d')
    trip_data = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date.between(start_date, end_date)).all()
    
    session.close()
    
    trip = list(np.ravel(trip_data))
    return jsonify(trip)

if __name__ == '__main__':
    app.run(debug=True)