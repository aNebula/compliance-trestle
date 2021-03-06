# Copyright (c) 2020 IBM Corp. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for trestle import command."""
import argparse
import json
import os
import pathlib
import random
import string
import sys
import tempfile
from json.decoder import JSONDecodeError
from unittest.mock import patch

from tests import test_utils

import trestle.core.commands.import_ as importcmd
import trestle.core.err as err
import trestle.oscal
from trestle.cli import Trestle
from trestle.core import generators
from trestle.core.commands import create
from trestle.oscal.catalog import Catalog


def test_import_cmd(tmp_trestle_dir: pathlib.Path) -> None:
    """Happy path test at the cli level."""
    # 1. Input file, profile:
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    profile_file = f'{tmp_trestle_dir.parent}/{rand_str}.json'
    profile_data = generators.generate_sample_model(trestle.oscal.profile.Profile)
    profile_data.oscal_write(pathlib.Path(profile_file))
    # 2. Input file, target:
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    target_file = f'{tmp_trestle_dir.parent}/{rand_str}.json'
    target_data = generators.generate_sample_model(trestle.oscal.target.TargetDefinition)
    target_data.oscal_write(pathlib.Path(target_file))
    # Test 1
    test_args = f'trestle import -f {profile_file} -o imported'.split()
    with patch.object(sys, 'argv', test_args):
        rc = Trestle().run()
        assert rc == 0
    # Test 2
    test_args = f'trestle import -f {target_file} -o imported'.split()
    with patch.object(sys, 'argv', test_args):
        rc = Trestle().run()
        assert rc == 0


def test_import_run(tmp_trestle_dir: pathlib.Path) -> None:
    """Test successful _run() on valid and invalid."""
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    catalog_file = f'{tmp_trestle_dir.parent}/{rand_str}.json'
    catalog_data = generators.generate_sample_model(trestle.oscal.catalog.Catalog)
    catalog_data.oscal_write(pathlib.Path(catalog_file))
    i = importcmd.ImportCmd()
    args = argparse.Namespace(file=catalog_file, output='imported', verbose=True)
    rc = i._run(args)
    assert rc == 0


def test_import_clash_on_output(tmp_trestle_dir: pathlib.Path) -> None:
    """Test an attempt to import into an existing trestle file."""
    # 1. Create a sample catalog,
    args = argparse.Namespace(name='my-catalog', extension='json', verbose=True)
    create.CreateCmd.create_object('catalog', Catalog, args)
    # 2. Create a valid oscal object in tmp_trestle_dir.parent,
    sample_data = generators.generate_sample_model(trestle.oscal.catalog.Catalog)
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    sample_data.oscal_write(pathlib.Path(f'{tmp_trestle_dir.parent}/{rand_str}.json'))
    # 3. then attempt to import that out to the previously created catalog, forcing the clash:
    i = importcmd.ImportCmd()
    args = argparse.Namespace(file=f'{tmp_trestle_dir.parent}/{rand_str}.json', output='my-catalog', verbose=True)
    rc = i._run(args)
    assert rc == 1


def test_import_non_top_level_element(tmp_trestle_dir: pathlib.Path) -> None:
    """Test for expected fail to import non-top level element, e.g., groups."""
    # Input file, catalog:
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    groups_file = f'{tmp_trestle_dir.parent}/{rand_str}.json'
    groups_data = generators.generate_sample_model(trestle.oscal.catalog.Group)
    groups_data.oscal_write(pathlib.Path(groups_file))
    args = argparse.Namespace(file=groups_file, output='imported', verbose=True)
    i = importcmd.ImportCmd()
    rc = i._run(args)
    assert rc == 1


def test_import_missing_input_file(tmp_trestle_dir: pathlib.Path) -> None:
    """Test for missing input file."""
    # Test
    args = argparse.Namespace(file='random_named_file.json', output='catalog', verbose=True)
    i = importcmd.ImportCmd()
    rc = i._run(args)
    assert rc == 1


def test_import_bad_working_directory(tmp_path: pathlib.Path) -> None:
    """Test for working directory that is not a trestle initialized directory."""
    # Input file, catalog:
    catalog_file_path = pathlib.Path.joinpath(test_utils.JSON_TEST_DATA_PATH.absolute(), 'minimal_catalog.json')
    args = argparse.Namespace(file=str(catalog_file_path), output='catalog', verbose=True)
    i = importcmd.ImportCmd()
    with patch('trestle.utils.fs.get_trestle_project_root') as get_trestle_project_root_mock:
        get_trestle_project_root_mock.return_value = None
        rc = i._run(args)
        assert rc == 1


def test_import_from_inside_trestle_project_is_bad(tmp_trestle_dir: pathlib.Path) -> None:
    """Test for attempting import from a trestle project directory."""
    sample_file = open('infile.json', 'w+')
    sample_file.write('{}')
    sample_file.close()
    args = argparse.Namespace(file='infile.json', output='catalog', verbose=True)
    i = importcmd.ImportCmd()
    rc = i._run(args)
    assert rc == 1


def test_import_bad_input_extension(tmp_trestle_dir: pathlib.Path) -> None:
    """Test for bad input extension."""
    # Some input file with bad extension.
    temp_file = tempfile.NamedTemporaryFile(suffix='.txt')
    args = argparse.Namespace(file=temp_file.name, output='catalog', verbose=True)
    i = importcmd.ImportCmd()
    rc = i._run(args)
    assert rc == 1


def test_import_load_file_failure(tmp_trestle_dir: pathlib.Path) -> None:
    """Test model load failures."""
    # Create a file with bad json
    sample_data = '"star": {'
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    bad_file = pathlib.Path(f'{tmp_trestle_dir.parent}/{rand_str}.json').open('w+', encoding='utf8')
    bad_file.write(sample_data)
    bad_file.close()
    with patch('trestle.utils.fs.load_file') as load_file_mock:
        load_file_mock.side_effect = err.TrestleError('stuff')
        args = argparse.Namespace(file=bad_file.name, output='imported', verbose=True)
        i = importcmd.ImportCmd()
        rc = i._run(args)
        assert rc == 1
    # Force PermissionError:
    with patch('trestle.utils.fs.load_file') as load_file_mock:
        load_file_mock.side_effect = PermissionError
        args = argparse.Namespace(file=bad_file.name, output='imported', verbose=True)
        i = importcmd.ImportCmd()
        rc = i._run(args)
        assert rc == 1
    # Force JSONDecodeError:
    with patch('trestle.utils.fs.load_file') as load_file_mock:
        load_file_mock.side_effect = JSONDecodeError(msg='Extra data:', doc=bad_file.name, pos=0)
        args = argparse.Namespace(file=bad_file.name, output='imported', verbose=True)
        i = importcmd.ImportCmd()
        rc = i._run(args)
        assert rc == 1
    # This is in case the same tmp_trestle_dir.parent is used, as across succeeding scopes of one pytest
    os.chmod(bad_file.name, 0o600)
    os.remove(bad_file.name)


def test_import_root_key_failure(tmp_trestle_dir: pathlib.Path) -> None:
    """Test root key is not found."""
    sample_data = {'id': '0000', 'title': 'nothing'}
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    sample_file = pathlib.Path(f'{tmp_trestle_dir.parent}/{rand_str}.json').open('w+', encoding='utf8')
    sample_file.write(json.dumps(sample_data))
    sample_file.close()
    args = argparse.Namespace(file=sample_file.name, output='catalog', verbose=True)
    i = importcmd.ImportCmd()
    rc = i._run(args)
    assert rc == 1


def test_import_failure_parse_file(tmp_trestle_dir: pathlib.Path) -> None:
    """Test model failures throw errors and exit badly."""
    sample_data = {'id': '0000'}
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    sample_file = pathlib.Path(f'{tmp_trestle_dir.parent}/{rand_str}.json').open('w+', encoding='utf8')
    sample_file.write(json.dumps(sample_data))
    sample_file.close()
    with patch('trestle.core.parser.parse_file') as parse_file_mock:
        parse_file_mock.side_effect = err.TrestleError('stuff')
        args = argparse.Namespace(file=f'{tmp_trestle_dir.parent}/{rand_str}.json', output='catalog', verbose=True)
        i = importcmd.ImportCmd()
        rc = i._run(args)
        assert rc == 1


def test_import_root_key_found(tmp_trestle_dir: pathlib.Path) -> None:
    """Test root key is found."""
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    catalog_file = f'{tmp_trestle_dir.parent}/{rand_str}.json'
    catalog_data = generators.generate_sample_model(trestle.oscal.catalog.Catalog)
    catalog_data.oscal_write(pathlib.Path(catalog_file))
    args = argparse.Namespace(file=catalog_file, output='catalog', verbose=True)
    i = importcmd.ImportCmd()
    rc = i._run(args)
    assert rc == 0


def test_import_failure_simulate_plan(tmp_trestle_dir: pathlib.Path) -> None:
    """Test model failures throw errors and exit badly."""
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    catalog_file = f'{tmp_trestle_dir.parent}/{rand_str}.json'
    catalog_data = generators.generate_sample_model(trestle.oscal.catalog.Catalog)
    catalog_data.oscal_write(pathlib.Path(catalog_file))
    with patch('trestle.core.models.plans.Plan.simulate') as simulate_plan_mock:
        simulate_plan_mock.side_effect = err.TrestleError('stuff')
        args = argparse.Namespace(file=catalog_file, output='imported', verbose=True)
        i = importcmd.ImportCmd()
        rc = i._run(args)
        assert rc == 1


def test_import_failure_execute_plan(tmp_trestle_dir: pathlib.Path) -> None:
    """Test model failures throw errors and exit badly."""
    rand_str = ''.join(random.choice(string.ascii_letters) for x in range(16))
    catalog_file = f'{tmp_trestle_dir.parent}/{rand_str}.json'
    catalog_data = generators.generate_sample_model(trestle.oscal.catalog.Catalog)
    catalog_data.oscal_write(pathlib.Path(catalog_file))
    with patch('trestle.core.models.plans.Plan.simulate'):
        with patch('trestle.core.models.plans.Plan.execute') as execute_plan_mock:
            execute_plan_mock.side_effect = err.TrestleError('stuff')
            args = argparse.Namespace(file=catalog_file, output='imported', verbose=True)
            i = importcmd.ImportCmd()
            rc = i._run(args)
            assert rc == 1
