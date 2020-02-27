# -*- coding: utf-8 -*-
"""User Config Mangement Tool

Usage:
    ucmt add (<target>...)
    ucmt relocate
    ucmt del (<target>...)

Options:
    -h, --help  Show help.
"""

from os.path import expanduser

from docopt import docopt

from .cmt import CMT
from .database import ConfigDB
from .locate import Collecter, ReLocater, Undo
from .path_translator import DBFilter


def main():
    args = docopt(__doc__)

    home = expanduser("~")
    filter_ = DBFilter(home)
    db_json = home + "/.ucmt/var/db.json"
    db = ConfigDB(db_json, filter_)
    collect_dir = home + "/.ucmt/configs"
    cmt = CMT(db, collect_dir)

    if args["add"]:
        for config_path in args["<target>"]:
            cmt.add(config_path, Collecter())

    elif args["relocate"]:
        cmt.relocate(ReLocater())

    elif args["del"]:
        for config_path in args["<target>"]:
            cmt.delete(config_path, Undo())


if __name__ == "__main__":
    main()
