import requests
import json
import pickle
import pandas as pd
import time
from git import Repo
import os

columns = ['updated_at', 'status']
deelgebieden = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Golf', 'Hotel', 'Oscar']
sleeptime = 2
t = 0

cwd = os.getcwd()
repo = Repo(cwd)
o = repo.remotes.origin

with open('data.pickle', 'rb') as handle:
    dict1 = pickle.load(handle)

i = 0
while True:
    # Try fetching the API data
    try:
        response = json.loads(requests.get("https://jotihunt.nl/api/2.0/areas").text)
    except:
        # Sleep and try again on fail
        print("Failed parsing")
        time.sleep(sleeptime)
        t += sleeptime
        i += 1
        continue
    # Process the data to different dicts
    data = response['data']
    for dg_data in data:
        dict1[dg_data["name"]][dg_data['updated_at']] = dg_data['status']
    time.sleep(sleeptime)
    t += sleeptime
    i += 1
    # Each 15 cycles save pickle and write to csv
    if i % 15 == 0:
        # Fetch git stuff
        o.fetch()
        repo.heads.main.set_tracking_branch(o.refs.main)
        repo.heads.main.checkout()
        o.pull()
        # Read pickle
        with open('data.pickle', 'rb') as handle:
            dict2 = pickle.load(handle)
        # Merge data
        combined_dict = dict2 | dict1
        #
        with open('data.pickle', 'wb') as handle:
            pickle.dump(combined_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)
        for dg in deelgebieden:
            df = pd.Series(combined_dict[dg], index=combined_dict[dg].keys(), name=f'{dg} status')
            df.to_csv(f"status/{dg}_data.csv", index_label='Time')

# Create first pickles
def first_pickles():
    dict1 = dict.fromkeys(deelgebieden)
    dict1 = {key: {} for key in dict1.keys()}
    with open('data.pickle', 'wb') as handle:
        pickle.dump(dict1, handle, protocol=pickle.HIGHEST_PROTOCOL)

# first_pickles()
