import pytest
from unittest.mock import MagicMock, patch, Mock
from io import StringIO
from contextlib import redirect_stdout
import argparse
from argparse import ArgumentParser, FileType
import os,sys
import yaml
from yaml import FullLoader

j2 = os.path.abspath('.')
sys.path.insert(1, j2)
import j2parser


YMLVARS = "test/template.vars.yml"
JSONVARS = "test/template.vars.json"
CMDLINEVARS = [line.lstrip().rstrip() for line in open("test/cmdline.vars.list")]
ENTRYPOINT = ["command", "path/to/config"]
TESTARGS = [
    "",
    "-i",
    "test/template.vars.yml",
    "--var",
    "local_docker_path=momo/choko/docker",
    "--entrypoint",
    "command",
    "path/to/config",
    "-o",
    "manifest.yml",
    "test/template.yml",
]


class TestJ2parserLoadVars:
    def test_load_vars_1(self):
        result = {}
        result.update(j2parser.load_vars(YMLVARS))
        assert result['local_docker_path'] == 'container/ntrip_docker/Dockerfile'
        return result

    def test_load_vars_2(self):
        result = {}
        result.update(j2parser.load_vars(JSONVARS))
        assert result['sidecar_service'] == 'sidecar'
        return result


#
class TestJ2parserParseCmdlineVars:
    def test_parse_cmdline_vars(self):
        result = {}
        result.update(j2parser.parse_cmdline_vars(CMDLINEVARS))
        assert result['remote_docker_path'] == 'aws_uri'
        return result


class Test_J2parser_Parse_nasty_entrypoint_args:
    def test_parse_nasty_entrypoint_args_1(self):
        result = {}
        result.update(j2parser.parse_nasty_entrypoint_args(ENTRYPOINT))
        assert result == {'entrypoint': ['command', 'path/to/config']}
        return result


class Test_J2parser_Main:
    def test_main_1(self):
        with patch.object(sys, "argv", new=TESTARGS):
            f1 = StringIO()
            with redirect_stdout(f1):
                j2parser.main(sys.argv)
            with open('manifest.yml', 'r') as fo:
                generatedfile = {}
                generatedfile = yaml.load(fo, Loader=FullLoader)
                image = str(TESTARGS[4].split("=", 1)[1])
                assert image == generatedfile["image"]['build']


