# import statements
from fastapi import FastAPI, HTTPException
import json
import numpy as np
import pickle
import datetime


# Opening arrival airport list



# Opening airport encodings
f = open('airport_encodings.json')
# returns JSON object as a dictionary
airports = json.load(f)




def create_airport_encoding(airport: str, airports: dict) -> np.array:
    """
    create_airport_encoding is a function that creates an array the length of all arrival airports from the chosen
    departure aiport.  The array consists of all zeros except for the specified arrival airport, which is a 1. Required
    as part of input to saved polynomial regression model.

    Parameters
    ----------
    airport : str
        The specified arrival airport code as a string.

    airports: dict
        A dictionary containing all of the arrival airport codes served from the chosen departure airport.

    Returns
    -------
    np.array
        A NumPy array the length of the number of arrival airports.  All zeros except for a single 1 
        denoting the arrival airport.  Returns None if arrival airport is not found in the input list.

    """
    temp = np.zeros(len(airports))
    if airport in airports:
        temp[airports.get(airport)] = 1
        temp = temp.T
        return temp
    else:
        return None


# In[ ]:


# TODO:  write the back-end logic to provide a prediction given the inputs
# requires finalized_model.pkl to be loaded
# the model must be passed a NumPy array consisting of the following:
# (polynomial order, encoded airport array, departure time as seconds since midnight, arrival time as seconds since midnight)
# the polynomial order is 1 unless you changed it during model training in Task 2
# YOUR CODE GOES HERE


# In[ ]:


# TODO:  write the API endpoints.  
# YOUR CODE GOES HERE


# In[5]:


with open("finalized_model.pkl", "rb") as model_file:
    model = pickle.load(model_file)




def predict_delay(departure_airport, arrival_airport, departure_time, arrival_time):
    encoded_airport = create_airport_encoding(arrival_airport, airports)
    if encoded_airport is None:
        raise HTTPException(status_code=404, detail="Arrival airport not found")
    
    try:
        dep_time_seconds = (datetime.datetime.strptime(departure_time, "%Y-%m-%dT%H:%M:%S") - datetime.datetime(1900, 1, 1)).total_seconds()
        arr_time_seconds = (datetime.datetime.strptime(arrival_time, "%Y-%m-%dT%H:%M:%S") - datetime.datetime(1900, 1, 1)).total_seconds()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Please use 'YYYY-MM-DDTHH:MM:SS'.")


    input_data = np.concatenate(([1], encoded_airport, [dep_time_seconds], [arr_time_seconds]))
    
    predicition = model.predict(input_data.reshape(1, -1))
    
    return predicition[0]




app = FastAPI()



@app.get("/")
async def root():
    return {"message": "API is functional!"}




@app.get("/predict/delays")
async def predict_delays(arrival_airport: str, departure_airport: str, departure_time: str, arrival_time: str):
    try:
        delay = predict_delay(departure_airport, arrival_airport, departure_time, arrival_time)
        return {"average_departure_delay": delay}
    except HTTPException as e:
        raise e






