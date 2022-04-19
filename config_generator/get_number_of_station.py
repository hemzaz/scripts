from terraform_external_data import terraform_external_data
import yaml
import itertools
import json

@terraform_external_data
def app(query):
    #if query.get('debug',"false") == "true":
    #    open('/tmp/a.yaml','w').write(query["stations"])
    stations = yaml.safe_load(query["stations"])
    return check(stations)


def check(stations):
    stations.sort(key=lambda m: m['name'] )
    count_per_station = [(x,len([w  for w in y])) for x,y in itertools.groupby(stations,key=lambda m: m['name'])] 
    return {
       "count_per_station" : json.dumps(count_per_station),
       "total_number_of_station" : json.dumps(len(count_per_station)),
    }



if __name__ == '__main__':
    #debug()
    app()
