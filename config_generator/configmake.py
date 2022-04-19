import click
import yaml
import itertools
import io
import csv
import json
from deepmerge import always_merger
from more_itertools import flatten, last


def app(users, stations, outfile):
    with click.open_file(stations, "r") as stf:
        stations = yaml.safe_load(stf)
    with click.open_file(users, "r") as usrs:
        usrsfile = csv.DictReader(
            usrs, delimiter=",", skipinitialspace=True, quoting=csv.QUOTE_NONE
        )
        users = []
        for user_dict in usrsfile:
            user = dict(user_dict)
            user["num"] = int(user["num"])
            users.append(user)
    for station in stations:
        selected_user = [
            user
            for user in users
            if user["caster"] == station["caster"] and int(user["num"]) > 0
        ]
        if not selected_user:
            raise Exception(f"station: {station} didn't found user")
            exit(1)
        else:
            selected_user = selected_user[0]
        station["user"] = [selected_user["user"]]
        station["password"] = [selected_user["password"]]
        selected_user["num"] = selected_user["num"] - 1
    csv_columns = users[0].keys()
    remaining_users_csv_file = StringIO()
    writer = csv.DictWriter(remaining_users_csv_file, fieldnames=csv_columns)
    writer.writeheader()
    for user in users:
        writer.writerow(user)
    remaining_users_csv_file.seek(0)
    with click.open_file(outfile, "w") as outf:
        outf.write(json.dumps(dict(stations=stations)))
        outf.close()
    return {
        "result": json.dumps(stations),
        "remaining_users_csv": remaining_users_csv_file.read(),
    }


def merge(base, station):
    return last(
        itertools.accumulate(
            [{}, base, dict(name=station["mountpoint"][:4]), station],
            lambda x, y: always_merger.merge(x, y),
        )
    )


def generate(obs):
    obs_yaml = [yaml.safe_load(file) for file in obs]
    merged = [
        [merge(file_yaml["base"], station) for station in file_yaml["stations"]]
        for file_yaml in obs_yaml
    ]
    flatten_data = list(flatten(merged))
    result = flatten_data
    return result

def json_formatter(obs, navs):
    obs_json = generate(obs=obs)
    nav_json = json.loads(json.dumps(yaml.unsafe_load(navs), indent=4, sort_keys=True))
    return [obs_json, nav_json]

def obs_nav_merger():


    input_jsons = [navs_json, obs_json]
    stations = []
    for json in input_jsons:
        stations.extend(json)


@click.command()
@click.option("-O", multiple=True)
@click.option("-N", multiple=True)
@click.option("-out", nargs=1)
def cli(O, N, out):
    obs = [open(x).read() for x in O]
    navs = open(N, "r")
    # print(type(result))
    with click.open_file(out, "w") as f:
        f.write(json.dumps(result, indent=4, sort_keys=True))

if __name__ == "__main__":
    cli()
