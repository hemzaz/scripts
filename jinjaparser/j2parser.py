#!/usr/bin/env python
import json
import string
import jinja2
import jinja2_getenv_extension
import yaml
import sys
import argparse
import pprint
from argparse import ArgumentParser, FileType

# from urllib.parse import unquote
from yaml.loader import FullLoader, SafeLoader

# pp = pprint.PrettyPrinter()


def load_vars(filename):
    with open(filename) as fo:
        if filename.lower().endswith(".json"):
            return json.load(fo)
        elif filename.lower().endswith(".yml"):
            return yaml.load(fo, Loader=FullLoader)
        else:
            raise ValueError("unknown file type: {}".format(filename))


def parse_cmdline_vars(cmdline_vars):
    return dict(var.split("=", 1) for var in cmdline_vars)


def parse_nasty_entrypoint_args(entrypointarg):
    entrypointDict = {}
    # manuveur to get the string right
    dressed = str(entrypointarg).replace("[", "").replace("]", "").replace("'", "")
    entrypointDict["entrypoint"] = dressed.translate(
        {ord(c): None for c in string.whitespace}
    ).split(",")
    # print(entrypointDict)
    return entrypointDict


def main(argv=None):
    example = """example:
    j2parser.py -i template.vars.yml --var "local_build=no" --entrypoint "command" "path/to/config" -o manifest.yml template.yml
    """
    argv = argv or sys.argv
    parser = ArgumentParser(
        description="Parse jinja2 copilot templates",
        epilog=example,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "template",
        type=FileType("r"),
        nargs="?",
        default=sys.stdin,
        help="Ex: j2parser.py [various flags] path/to/template.yml",
    )
    parser.add_argument(
        "--var", "-v", action="append", help='Ex: --var "local_build=no"'
    )
    parser.add_argument(
        "--entrypoint",
        "-e",
        type=str,
        action="append",
        nargs=2,
        default=argparse.SUPPRESS,
        help='Ex: j2parser.py --entrypoint "command" "/path/to/config"',
    )
    parser.add_argument(
        "--output",
        "-o",
        type=FileType("w"),
        nargs="?",
        default=sys.stdout,
        help="Ex: j2parser.py --output path/to/manifest.yml",
    )
    parser.add_argument(
        "--vars-file",
        "-i",
        nargs="?",
        help="Ex: j2parser.py -i path/to/template.vars.(yml||json)",
    )
    args = parser.parse_args(argv[1:])

    # print(sys.argv)
    # sys.exit(0)

    tvars = {}
    if args.vars_file:
        tvars.update(load_vars(args.vars_file))
        tvars.update(parse_cmdline_vars(args.var or []))
        tvars.update(parse_nasty_entrypoint_args(args.entrypoint or []))
        # print(tvars)
        # sys.exit(0)

    env = jinja2.Environment(
        extensions=["jinja2_getenv_extension.GetenvExtension"],
        undefined=jinja2.StrictUndefined,
    )
    template = env.from_string(args.template.read())
    args.output.write(template.render(tvars))


if __name__ == "__main__":
    main()
