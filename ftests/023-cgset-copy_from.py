#!/usr/bin/env python3
#
# Advanced cgset functionality test - test the '--copy-from' option
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
SRC_CGNAME = '023cgsetsrc'
DST_CGNAME = '023cgsetdst'

SETTINGS = ['memory.limit_in_bytes',
            'memory.soft_limit_in_bytes',
            'memory.swappiness']
VALUES = ['122880', '40960', '42']

def prereqs(config):
    result = consts.TEST_PASSED
    cause = None

    if CgroupVersion.get_version('memory') != CgroupVersion.CGROUP_V1:
        result = consts.TEST_SKIPPED
        cause = "This test requires the cgroup v1 memory controller"
        return result, cause

    return result, cause

def setup(config):
    Cgroup.create(config, CONTROLLER, SRC_CGNAME)
    Cgroup.create(config, CONTROLLER, DST_CGNAME)
    Cgroup.set(config, cgname=SRC_CGNAME, setting=SETTINGS, value=VALUES)

def test(config):
    result = consts.TEST_PASSED
    cause = None

    Cgroup.set(config, cgname=DST_CGNAME, copy_from=SRC_CGNAME)

    for i, setting in enumerate(SETTINGS):
        value = Cgroup.get(config, cgname=DST_CGNAME, setting=setting,
                           print_headers=False, values_only=True)

        if value != VALUES[i]:
            result = consts.TEST_FAILED
            cause = "Expected {} to be set to {}, but received {}".format(
                    setting, VALUES[i], value)
            return result, cause

    return result, cause

def teardown(config):
    Cgroup.delete(config, CONTROLLER, SRC_CGNAME)
    Cgroup.delete(config, CONTROLLER, DST_CGNAME)

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
