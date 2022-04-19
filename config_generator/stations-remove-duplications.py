from terraform_external_data import terraform_external_data
import yaml
import subprocess
import sys
import csv
import os
import io
import json
import more_itertools
import click


@click.command()
@click.option("--i")
@click.option("--o")
def app(i, o):
    with click.open_file(i, "r") as f:
        stationfile = f.read()
        statList = json.loads(stationfile)["stations"]
        empty_list = []
        # print(statList[0])
        # print(len(statList))
        for item in statList:
            if item not in empty_list:
                empty_list.append(item)
            else:
                pass
        # print(len(empty_list))
        with click.open_file(o, "w") as o:
            o.write(json.dumps(empty_list))
            # o.write(json.dumps(dict(stations=empty_list), indent=4))
            o.close()


if __name__ == "__main__":
    # check(yaml.safe_load(open('/tmp/a.yaml').read()))
    app()
