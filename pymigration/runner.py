# -*- coding: utf-8 -*-

import sys
import os

from argparse import ArgumentParser
from pymigration.version import version
sys.path.insert(0, os.getcwd())
from pymigration.model import DiscovererMigration, Version
from views import TerminalMessages


def pymigration():

    parser = ArgumentParser(description="Parameters to migrate.")
    parser.add_argument("-u", "--up", dest="up", default=False, action="store_true",
                      help="Execute python methods to upgrade schema of system.")

    parser.add_argument("--no-exec", default=True, dest="execute", action="store_false",
                        help="If you want only see the list of migrantions command.")

    parser.add_argument("-d", "--down", dest="down", default=False, action="store_true",
                      help="Execute python methods to downgrade schema of system.")

    parser.add_argument("-c", "--current-version", dest="current_version", default=False,
                      help="Version of actual migration.", action="store_true")

    parser.add_argument("-v", "--version", dest="version", default=False,
                      help="Displays pymigration's version and exit.", action="store_true")

    parser.add_argument("-t", "--to", dest="version_to", default=None,
                    help="Migrate to specific version .")

    args = parser.parse_args()


    migrations = DiscovererMigration(**vars(args))
    terminal_message = TerminalMessages(migrations, **vars(args))

    if args.version:
        print version

    if args.down:
        migrations = list(migrations.down_migrations())
        try:
            if migrations:
                for migration in migrations:
                    migration.down()
                    terminal_message.make_message("down", migration)
            else:
                print "No migrations need to be executed, already in %s version." % Version().get_current()
        except Exception, e:
            terminal_message.error_message("down", migration, e)
            sys.exit()
        if args.execute:
            Version().set_current("0")

    if args.up:
        migrations = list(migrations.up_migrations())
        try:
            if migrations:
                for migration in migrations:
                    migration.up()
                    terminal_message.make_message("up", migration)
            else:
                print "No migrations need to be executed, already in %s version." % Version().get_current()
        except Exception, e:
            terminal_message.error_message("up", migration, e)

    if args.current_version:
        terminal_message.current_version()

    if args.version_to:
        for migration in migrations.to_migrations():
            if migrations.is_up():
                try:
                    migration.up()
                    terminal_message.make_message("up", migration)
                except Exception, e:
                    terminal_message.error_message("up", migration, e)
                    sys.exit()

            elif migrations.is_down():
                try:
                    migration.down()
                    terminal_message.make_message("down", migration)
                except Exception, e:
                    terminal_message.error_message("down", migration, e)
                    sys.exit()
        if args.execute:
            Version().set_current(args.version_to)
