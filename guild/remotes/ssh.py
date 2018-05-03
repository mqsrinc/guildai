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

import logging
import subprocess

import guild.remote

log = logging.getLogger("guild.remotes.ssh")

class SSHRemote(guild.remote.Remote):

    def __init__(self, config):
        self.host = config["host"]
        self.user = config.get("user")
        self.guild_home = config.get("guild-home", ".guild")

    def push(self, runs, verbose=False):
        for run in runs:
            self._push_run(run, verbose)

    def push_dest(self):
        return "{}:{}".format(self.host, self.guild_home)

    def _push_run(self, run, verbose):
        opts = "-al"
        if verbose:
            opts += "v"
        cmd = ["rsync", opts, self._run_src(run), self._run_dest(run)]
        log.info("Copying %s" % run.id)
        log.debug("rsync cmd: %r", cmd)
        subprocess.check_call(cmd)

    @staticmethod
    def _run_src(run):
        return run.path + "/"

    def _run_dest(self, run):
        return "{}:{}/runs/{}/".format(
            self.host,
            self.guild_home,
            run.id)