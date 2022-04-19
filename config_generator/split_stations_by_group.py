from terraform_external_data import terraform_external_data
import json
import sys
import itertools

def get_group(group_name,stations):
  if not all([station['extra_labels']==stations[0]['extra_labels']] for station in stations):
    raise Exception(F"not all extra_labels in {stations}, are equals")

  return dict(group=group_name,stations=stations ,extra_labels = stations[0]["extra_labels"])

@terraform_external_data
def split_by_group(query):
    stations = json.loads(query["stations"])
    groups = list( get_group(x,list(y))for x,y in itertools.groupby(stations,lambda x: x['group']))

    return {"groups":json.dumps(groups)}

if __name__ == '__main__':
    split_by_group()