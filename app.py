#import data base / query created 
import numpy as np
import pandas as pd
import datetime as dt
​
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
​
#Import Flask
from flask import Flask, jsonify
​
#Database setup
engine = create_engine("sqlite:///hawaii.sqlite")
​
#Reflect an existing database into a new model
Base = automap_base()
​
#Reflect the tables
Base.prepare(engine, reflect=True)
​
#Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station
session = Session(engine)
​
#Create an app 
app = Flask(__name__)
​
# 3. Define static routes 
#  List all routes that are available.
@app.route("/")
def Home():
    "List all available routes"
    
    return (        
        f"List all available routes:<br/>"
​
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
    )
        
@app.route('/api/v1.0/precipitation/')
def Precipitation():
    
    last_12_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
   
    # Calculate the date 1 year ago from the last data point in the database
    calculate_date = dt.datetime.strptime(last_12_date, '%Y-%m-%d') - dt.timedelta(days=365)
​
    # Perform a query to retrieve the data and precipitation scores
    data_prep_scr = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= calculate_date).\
    order_by(Measurement.date).all()
    
    #Create dictionary
    prcp_dictionary = dict(data_prep_scr)
   
    return jsonify(prcp_dictionary)
​
    
@app.route('/api/v1.0/stations')
def Stations():
  
    #List the stations
    list_stations = session.query(Station.station).\
    order_by(Station.station).all() 
          
    return jsonify(list_stations)
​
​
@app.route('/api/v1.0/tobs')
def Tobs():
    
    #Define again for tobs some variables for the calculate
    last_12_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
   
    # Calculate the date 1 year ago from the last data point in the database
    calculate_date = dt.datetime.strptime(last_12_date, '%Y-%m-%d') - dt.timedelta(days=365)
        
    #Query the dates and temperature observations of the most active station for the last year of data
    temperature_observation = session.query(Measurement.tobs, Measurement.date).\
    filter(Measurement.date >= calculate_date).all()
    
    return jsonify(temperature_observation)
​
@app.route('/api/v1.0/<start>') 
 
def calc_temps(start):
    
    sel = [func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)]
​
​
    temp_list_start = session.query(*sel).\
        filter(Measurement.date >= start).all()
                
    return jsonify(temp_list_start)
​
​
@app.route("/api/v1.0/<start>/<end>")  
def cal_temps_start_end(start, end):
​
    sel = [func.min(Measurement.tobs), 
        func.avg(Measurement.tobs), 
        func.max(Measurement.tobs)]
​
    result = session.query(*sel).\
        filter(Measurement.date >= start).filter(Measurement.date <= end_date).all()
                
    return jsonify(result)
​
# 4. Define main behavior
if __name__ == "__main__":
    app.run(debug=True)