# -*- coding: utf-8 -*-

from textwrap import dedent
import sys

class FormatterMessage(object):

    def __init__(self, submodule):
        self.doc_migration = self.ident(submodule.header())
        self.doc_up = self.ident(submodule.doc_up(), 23).strip()
        self.doc_down = self.ident(submodule.doc_down(), 23).strip()
        self.version_migrate = "{:<15}".format(str(submodule.version))
        self.archive_name = submodule.filename()

    def message_up(self):
        output = """
{self.version_migrate} - {self.archive_name}
{self.doc_migration}
                  up - {self.doc_up}
""".format(self=self)
        return output

    def message_down(self):
        output = """
{self.version_migrate} - {self.archive_name}
{self.doc_migration}
                  down - {self.doc_down}
""".format(self=self)
        return output


    def ident(self, text, space=18):
        text = dedent(text)
        lines = text.split("\n")
        text_ident = " "*space
        text = text_ident + ("\n" + text_ident).join(lines)
        return text


class TerminalMessages(object):

    def __init__(self, migrations, **kwargs):
        self.migrations = migrations
        print "Running command: pymigration %s" % " ".join(sys.argv[1:])

    def current_version(self):
        print self.migrations.get_current_version()

    def up_message(self, migration):
        print FormatterMessage(migration).message_up()

    def down_message(self, migration):
        print FormatterMessage(migration).message_down()
