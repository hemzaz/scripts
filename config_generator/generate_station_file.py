import click
import yaml
import itertools
import io
import csv
import json
from terraform_external_data import terraform_external_data
from deepmerge import always_merger
from more_itertools import flatten, last


def read_users_csv(users):
    f = io.StringIO(users)
    users = []
    for user_dict in csv.DictReader(
        f, delimiter=",", skipinitialspace=True, quoting=csv.QUOTE_NONE
    ):
        user = dict(user_dict)
        user["num"] = int(user["num"])
        users.append(user)
    return users


def find_user_for_station(users, station):
    selected_user = [
        user
        for user in users
        if user["caster"] == station["caster"] and user["num"] > 0
    ]
    if not selected_user:
        raise Exception(f"station: {station} didn't found user")
        exit(1)
    else:
        selected_user = selected_user[0]
    station["user"] = [selected_user["user"]]
    station["password"] = [selected_user["password"]]
    selected_user["num"] = selected_user["num"] - 1


def merge(base, station):
    return last(
        itertools.accumulate(
            [{}, base, dict(name=station["mountpoint"][:4]), station],
            lambda x, y: always_merger.merge(x, y),
        )
    )


def generate(files):
    files_yaml = [yaml.safe_load(file) for file in files]
    merged = [
        [merge(file_yaml["base"], station) for station in file_yaml["stations"]]
        for file_yaml in files_yaml
    ]
    flatten_data = list(flatten(merged))
    result = flatten_data
    return result


@click.command()
@click.option("--file", multiple=True)
@click.option("--outfile", nargs=1)
def cli(file, outfile):
    # print(type(file))
    files = [open(x).read() for x in file]
    result = generate(files=files)
    print(result)
    with click.open_file(outfile, "w") as f:
        # pass
        f.write(json.dumps(result, indent=4, sort_keys=True))
    # import pprint
    #
    # pprint.pprint(result)


@terraform_external_data
def data(query):
    import json

    result = {"data": json.dumps(generate(files=yaml.safe_load(query["files"])))}
    print(result)
    return result


if __name__ == "__main__":
    cli()
