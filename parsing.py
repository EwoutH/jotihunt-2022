import requests
import json
import pickle
import pandas as pd
import time

columns = ['updated_at', 'status']
deelgebieden = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot']
sleeptime = 20
t = 0


try:
    with open('data.pickle', 'rb') as handle:
        dict1 = pickle.load(handle)
except:
    # Create dict with deelgebieden as keys
    dict1 = dict.fromkeys(deelgebieden)
    for key in dict1.keys():
        dict1[key] = {}

while True:
    # Try fetching the API data
    try:
        response = json.loads(requests.get("https://jotihunt.nl/api/2.0/areas").text)
    except:
        # Sleep and try again on fail
        print("Failed parsing")
        time.sleep(sleeptime)
        t += sleeptime
        continue
    # Process the data to different dicts
    data = response['data']
    for dg_data in data:
        dict1[dg_data["name"]][dg_data['updated_at']] = dg_data['status']
    time.sleep(sleeptime)
    t += sleeptime
    # At the end of the run, save pickle and write to csv
    if t > 875:
        with open('data.pickle', 'wb') as handle:
            pickle.dump(dict1, handle, protocol=pickle.HIGHEST_PROTOCOL)
        for dg in deelgebieden:
            df = pd.Series(dict1[dg], index=dict1[dg].keys(), name=f'{dg} status')
            df.to_csv(f"status/{dg}_data.csv", index_label='Time')
        break


# Create first pickles
def first_pickles():
    dict1 = dict.fromkeys(deelgebieden)
    dict1 = {key: {} for key in dict1.keys()}
    with open('data.pickle', 'wb') as handle:
        pickle.dump(dict1, handle, protocol=pickle.HIGHEST_PROTOCOL)

# first_pickles()
