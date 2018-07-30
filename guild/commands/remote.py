# Copyright 2017-2018 TensorHub, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import absolute_import
from __future__ import division

import click

from guild import cli
from guild import click_util

from .remote_start import remote_start
from .remote_status import remote_status
from .remote_stop import remote_stop

@click.group(cls=click_util.Group)

def remote():
    """Manage remote status.
    """

remote.add_command(remote_start)
remote.add_command(remote_status)
remote.add_command(remote_stop)