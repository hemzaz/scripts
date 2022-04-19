from terraform_external_data import terraform_external_data
import yaml
import itertools
import json

@terraform_external_data
def app(query):
    #if query.get('debug',"false") == "true":
    #    open('/tmp/a.yaml','w').write(query["stations"])
    stations = yaml.safe_load(query["stations"])
    return {
       "stations_names" : json.dumps(list(set([station['name'] for station in stations]))),
    }



if __name__ == '__main__':
    #debug()
    app()
