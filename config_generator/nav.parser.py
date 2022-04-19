import json
import yaml
import click

@click.command()
@click.option("--nfile", nargs=1)
@click.option("--sfile", nargs=1)
@click.option("--outfile", nargs=1)
def cli(nfile,sfile, outfile):
    infile = json.loads(json.dumps(yaml.unsafe_load(open(nfile, 'r')), indent=4, sort_keys=True))
    stfile = json.loads(json.dumps(json.load(open(sfile, 'r')), indent=4, sort_keys=True))
    merged = []
    print(infile)
    files = [infile, stfile]
    for file in files:
        merged.extend(file)
    with click.open_file(outfile, "w") as f:
        f.write(json.dumps(merged, indent=4, sort_keys=True))

if __name__ == "__main__":
    cli()
