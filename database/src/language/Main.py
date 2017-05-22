#!python3
#encoding:utf-8
import sys
import subprocess
import shlex
import os.path
import getpass
import dataset
import database.src.TsvLoader
class Main:
    def __init__(self, db_path):
        self.db_path = db_path
        self.path_this_dir = os.path.abspath(os.path.dirname(__file__))

    def Run(self):
        self.__Create()
        self.__Insert()
#        self.__Check() # Check.shで正常に文字列結合できずパスを作成できない。

    def __Create(self):
        subprocess.call(shlex.split("bash \"{0}\" \"{1}\"".format(os.path.join(self.path_this_dir, "create/Create.sh"), self.db_path)))

    def __Insert(self):
        source = database.src.language.insert.LanguageSource.LanguageSource()
#        inserter = database.src.language.insert.Inserter.Inserter(self.data)
        inserter = database.src.language.insert.Inserter.Inserter(self.db_path)
        inserter.Insert(self.source.Get())

    def __Check(self):
        pass
