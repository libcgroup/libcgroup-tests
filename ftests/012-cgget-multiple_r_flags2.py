#!/usr/bin/env python3
#
# Advanced cgget functionality test - multiple '-r' flags and multiple cgroups
#
# Copyright (c) 2021 Oracle and/or its affiliates.
# Author: Tom Hromatka <tom.hromatka@oracle.com>
#

#
# This library is free software; you can redistribute it and/or modify it
# under the terms of version 2.1 of the GNU Lesser General Public License as
# published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License
# for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this library; if not, see <http://www.gnu.org/licenses>.
#

from cgroup import Cgroup, CgroupVersion
import consts
import ftests
import os
import sys

CONTROLLER = 'memory'
CGNAME1 = '012cgget1'
CGNAME2 = '012cgget2'

SETTING1 = 'memory.limit_in_bytes'
VALUE1 = '4194304'

SETTING2 = 'memory.soft_limit_in_bytes'
VALUE2 = '4096000'

EXPECTED_OUT = '''{}:
{}
{}

{}:
{}
{}
'''.format(CGNAME1, VALUE1, VALUE2, CGNAME2, VALUE1, VALUE2)

def prereqs(config):
    result = consts.TEST_PASSED
    cause = None

    return result, cause

def setup(config):
    Cgroup.create(config, CONTROLLER, CGNAME1)
    Cgroup.create(config, CONTROLLER, CGNAME2)
    Cgroup.set(config, CGNAME1, SETTING1, VALUE1)
    Cgroup.set(config, CGNAME1, SETTING2, VALUE2)
    Cgroup.set(config, CGNAME2, SETTING1, VALUE1)
    Cgroup.set(config, CGNAME2, SETTING2, VALUE2)

def test(config):
    result = consts.TEST_PASSED
    cause = None

    out = Cgroup.get(config, controller=None, cgname=[CGNAME1, CGNAME2],
                     setting=[SETTING1, SETTING2], values_only=True)

    for line_num, line in enumerate(out.splitlines()):
        if line.strip() != EXPECTED_OUT.splitlines()[line_num].strip():
            result = consts.TEST_FAILED
            cause = "Expected line:\n\t{}\nbut received line:\n\t{}".format(
                    EXPECTED_OUT.splitlines()[line_num].strip(), line.strip())
            return result, cause

    return result, cause

def teardown(config):
    Cgroup.delete(config, CONTROLLER, CGNAME1)
    Cgroup.delete(config, CONTROLLER, CGNAME2)

def main(config):
    [result, cause] = prereqs(config)
    if result != consts.TEST_PASSED:
        return [result, cause]

    setup(config)
    [result, cause] = test(config)
    teardown(config)

    return [result, cause]

if __name__ == '__main__':
    config = ftests.parse_args()
    # this test was invoked directly.  run only it
    config.args.num = int(os.path.basename(__file__).split('-')[0])
    sys.exit(ftests.main(config))
