from typing import Union
import urllib.request
import json

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/predict")
def predict(dt, num, melt_temp, motorspeed, melt_weight, insp):
    data =  {
                "Inputs": {
                    "data": [
                    {
                        "STD_DT": "2000-01-01T00:00:00.000Z",
                        "NUM": num,
                        "MELT_TEMP": melt_temp,
                        "MOTORSPEED": motorspeed,
                        "MELT_WEIGHT": melt_weight,
                        "INSP": insp
                    }
                    ]
                },
                "GlobalParameters": {
                    "method": "predict"
                }
            }
    
    body = str.encode(json.dumps(data))

    url = 'http://9683db50-9df2-4548-8f13-811accf8a3b1.koreacentral.azurecontainer.io/score'
    # Replace this with the primary/secondary key or AMLToken for the endpoint
    api_key = 'VvlgQdN5kUFEsYAwSH1EHd4ztohNZNsd'
    if not api_key:
        raise Exception("A key should be provided to invoke the endpoint")


    headers = {'Content-Type':'application/json', 'Authorization':('Bearer '+ api_key)}

    req = urllib.request.Request(url, body, headers)

    try:
        response = urllib.request.urlopen(req)

        result = response.read().decode('utf-8')
        result = json.loads(result)["Results"][0]
        return {"Result": result}
    
    except urllib.error.HTTPError as error:
        print("The request failed with status code: " + str(error.code))

        # Print the headers - they include the requert ID and the timestamp, which are useful for debugging the failure
        print(error.info())
        print(error.read().decode("utf8", 'ignore'))

