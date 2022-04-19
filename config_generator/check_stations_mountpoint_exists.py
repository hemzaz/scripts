from terraform_external_data import terraform_external_data
import yaml
import subprocess
import sys
import csv
import os
import json
from io import StringIO
import exo.utilities.fetcher.read_stations_from_caster

@terraform_external_data
def app(query):
    stations = yaml.safe_load(query["stations"])
    check(stations)
    return { }

def get_current_by_caster(caster):
    return exo.utilities.fetcher.read_stations_from_caster.get_stations_info_from_site(caster)
    

def check(stations):
    missing = []
    caster_info = dict()
    for station in stations:
        caster_path = F"{station['caster']}:{station['port']}"  
        if 'secure' in station and station['secure']:
            caster_path = F"https://{caster_path}"
        if not caster_path in caster_info:
            caster_info[caster_path] = get_current_by_caster(caster_path)
        if not any([ data['mountpoint'] == station['mountpoint'] for data in  caster_info[caster_path] ]):
            missing.append(F"Mountpoint {station['mountpoint']} doesn't exists in {caster_path}")
    if len(missing) > 20:
        raise Exception("\n".join(missing))

if __name__ == '__main__':
    #check(yaml.safe_load(open('/tmp/a.yaml').read()))
    app()
