from terraform_external_data import terraform_external_data
import yaml
import subprocess
import sys
import csv
import os
import json
from io import StringIO
import requests

@terraform_external_data
def app(query):
    stations = yaml.safe_load(query["stations"])
    check(stations)
    return { }

def get_current():
    locations = "https://bitbucket.org/lear-raanan/gps-location/raw/master/result.json"
    response = requests.get(locations)
    response.raise_for_status()
    return json.loads(response.content)

def check(stations):
    avalible_stations = set([x['key']for x in get_current()]) 
    not_found = []
    for station in stations:
        if not station['name'] in avalible_stations:
            not_found.append(station['name'])
    if not_found:
        raise Exception(F"Stations: {not_found} is not avalible_stations")
if __name__ == '__main__':
    app()
