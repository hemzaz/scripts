from terraform_external_data import terraform_external_data
import yaml
import subprocess
import sys
import csv
import os
import json
from io import StringIO
import click
from more_itertools import flatten
import pprint
pp = pprint.PrettyPrinter(indent=4)

def tobool(value):
    return value.lower() in ['1',"true","t"]

@click.command()
@click.option('--users')
@click.option('--stations')
@click.option('--outfile')
def app(users,stations,outfile):
    with click.open_file(stations, 'r') as stf:
        stations = yaml.safe_load(stf)
    with click.open_file(users, 'r') as usrs:
        usrsfile = csv.DictReader(usrs, delimiter=',', skipinitialspace=True, quoting=csv.QUOTE_NONE)
        users = []
        for user_dict in usrsfile:
            user = dict(user_dict)
            user['num'] = int(user['num'])
            users.append(user)
    for station in stations:
        selected_user = [user for user in users if user['caster'] == station['caster'] and int(user['num'])>0]
        if not selected_user:
            raise Exception(F"station: {station} didn't found user")
            exit(1)
        else:
            selected_user= selected_user[0]
        station['user'] = [selected_user['user']]
        station['password'] = [selected_user['password']]
        selected_user['num'] = selected_user['num'] - 1
    csv_columns = users[0].keys()
    remaining_users_csv_file = StringIO()
    writer = csv.DictWriter(remaining_users_csv_file, fieldnames=csv_columns)
    writer.writeheader()
    for user in users:
        writer.writerow(user)
    remaining_users_csv_file.seek(0)
    with click.open_file(outfile, 'w') as outf:
        outf.write(json.dumps(dict(stations=stations)))
        outf.close()
    return {"result": json.dumps(stations), "remaining_users_csv": remaining_users_csv_file.read() }

if __name__ == '__main__':
    # Always protect Python scripts from import side effects with
    # a condition to check the __name__. Not specifically necessary
    # for terraform_external_data, but it's a best practice in general.
    app()
    