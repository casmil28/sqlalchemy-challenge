# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
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

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )



@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all daily precipitation totals for the last 12 months of data"""
    # Query and summarize most recent 12 months of data
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days = 366)
    prcp_list = []
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= one_year_ago).all()
    for date, prcp in prcp_results:
        prcp_dict= {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)
        
    
    session.close()

    return jsonify(prcp_list)

#station list
@app.route("/api/v1.0/stations")
def stations():

    # Create our session (link) from Python to the DB
    session = Session(engine)
    """List of the stations"""
    #gather all stations
    station_activity = session.query(Measurement.station, func.count(Measurement.date)).group_by(Measurement.station).order_by(func.count(Measurement.date).desc()).all()
    active_station_list = []
    for station, count in station_activity:
        activity_dict = {}
        activity_dict["Active Stations"] = station
        active_station_list.append(activity_dict)


    session.close()

    return jsonify(active_station_list)

#activity of most active station
@app.route("/api/v1.0/tobs")
def tobs():
      
    session = Session(engine)

    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    one_year_ago = dt.datetime(2017, 8, 23) - dt.timedelta(days = 366)
    tobs_results = session.query(Measurement.date , Measurement.tobs).filter(Measurement.date >= one_year_ago).filter(Measurement.station == "USC00519281").all()
    tobs_results_list = []
    for date, tobs in tobs_results:
        tobs_dict = {}
        tobs_dict["Date"] = date
        tobs_dict["Temp"] = tobs
        tobs_results_list.append(tobs_dict)
    
    session.close()

    return jsonify(tobs_results_list)


@app.route("/api/v1.0/<start>")
def start(start):

    session = Session(engine)
    
    start_date_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).all()
    start_list = []
    for min, max, avg in start_date_stats:
        start_dict = {}
        start_dict["Minimum"] = min
        start_dict["Maximum"] = max
        start_dict["Average"] = avg
        start_list.append(start_dict)

    session.close()

    return jsonify(start_list)


@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):

    session = Session(engine)

    start_end_stats = session.query(func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    start_end_list =[]
    for min, max, avg in start_end_stats:
        start_end_dict = {}
        start_end_dict["Minimum"] = min
        start_end_dict["Maximum"] = max
        start_end_dict["Average"] = avg
        start_end_list.append(start_end_dict)

    session.close()
    return jsonify(start_end_list
                   













if __name__ == '__main__':
    app.run(debug=True)