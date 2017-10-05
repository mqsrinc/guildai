import imp
import logging
import os
import sys

import guild.plugin

def main():
    _init_logging()
    logging.debug("sys.path: %s", os.path.pathsep.join(sys.path))
    module_name, rest_args = _parse_args()
    module_info = imp.find_module(module_name)
    _shift_argv(module_info, rest_args)
    _init_plugins()
    _apply_plugins()
    _load_module_as_main(module_info)

def _init_logging():
    level = int(os.getenv("LOG_LEVEL", logging.WARN))
    format = os.getenv("LOG_FORMAT", "%(levelname)s: %(message)s")
    logging.basicConfig(level=level, format=format)

def _parse_args():
    if len(sys.argv) < 2:
        sys.stderr.write("missing required arg\n")
        sys.exit(1)
    return sys.argv[1], sys.argv[2:]

def _shift_argv(module_info, rest_args):
    _, path, _ = module_info
    sys.argv = [os.path.abspath(path)] + rest_args

def _init_plugins():
    guild.plugin.init_plugins()

def _apply_plugins():
    env = os.getenv("GUILD_PLUGINS")
    if env:
        for name in env.split(","):
            _apply_plugin(name)

def _apply_plugin(name):
    plugin = guild.plugin.for_name(name)
    plugin.patch_env()

def _load_module_as_main(module_info):
    f, path, desc = module_info
    imp.load_module("__main__", f, path, desc)

if __name__ == "__main__":
    main()
