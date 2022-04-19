from terraform_external_data import terraform_external_data
import yaml
import subprocess
import sys
import csv
import os

def get_long_name(short_name):
    print(short_name,file=sys.stderr)
    total_names = []
    with open(os.path.join(os.path.split(__file__)[0],'mountpoints.csv'), newline='') as csvfile:
         reader = csv.DictReader(csvfile)
         for row in reader:
            total_names.append(row['Mountpoint'])
    return [full_name for full_name in total_names if full_name[:4].lower() == short_name.lower()][0]

@terraform_external_data
def get_cool_data(query):
    stations = yaml.load(query["receivers_yaml"])
    result = []
    for station in stations:
        result.append({'name':station[:4]})

    # Terraform requires the values you return be strings,
    # so terraform_external_data will error if they aren't.
    return {"result": yaml.dump(result,default_flow_style=False)}

if __name__ == '__main__':
    # Always protect Python scripts from import side effects with
    # a condition to check the __name__. Not specifically necessary
    # for terraform_external_data, but it's a best practice in general.
    get_cool_data()
    
