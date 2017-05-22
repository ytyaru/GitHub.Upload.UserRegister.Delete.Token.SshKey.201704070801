#!python3
#encoding:utf-8
import os.path
import configparser
import shlex
import subprocess
import dataset
import web.service.github.api.v3.CurrentUser
import web.service.github.api.v3.CurrentRepository
import web.service.github.api.v3.Client
import database.src.Database
import database.src.language.insert.Main
import database.src.api.Main
import database.src.gnu_license.create.Main
import database.src.gnu_license.insert.main
import database.src.license.Main
import database.src.license.insert.Main
import database.src.other_repo.insert.Main
import database.src.account.Main
import database.src.repo.insert.Main

class Database:
    def __init__(self):
        self.__path_dir_this = os.path.abspath(os.path.dirname(__file__))
        self.__files = {
            'lang': 'GitHub.Languages.sqlite3',
            'api': 'GitHub.Apis.sqlite3',
            'gnu_license': 'GNU.Licenses.sqlite3',
            'account': 'GitHub.Accounts.sqlite3',
            'license': 'GitHub.Licenses.sqlite3',
            'other_repo': 'GitHub.Repositories.__other__.sqlite3',
            'repo': 'GitHub.Repositories.{user}.sqlite3',
        }        
        self.lang = None
        self.api = None
        self.gnu_license = None
        self.account = None
        self.license = None
        self.other_repo = None
        self.repo = None
        self.repos = {}

    def __GetPaths(self):
        return self.__files
    Paths = property(__GetPaths)

    # 1. 全DBのファイルパス作成
    # 2. マスターDBファイルがないなら
    # 2-1. マスターDBファイル作成
    # 2-2. マスターDBデータ挿入
    # 3. アカウントDBがないなら
    # 3-1. アカウントDBファイル作成
    def Initialize(self):
        config = configparser.ConfigParser()
        config.read('./config.ini')
        print(config['Path']['DB'])
        print(os.path.abspath(config['Path']['DB']))
        self.dir_db = os.path.abspath(config['Path']['DB'])
        for key in self.__files.keys():
            self.__files[key] = os.path.join(self.dir_db, self.__files[key])
        """
        self.__files['lang'] = os.path.join(self.dir_db, self.__files['lang'])
        self.__files['api'] = os.path.join(self.dir_db, self.__files['api'])
        self.__files['gnu_license'] = os.path.join(self.dir_db, self.__files['gnu_license'])
        self.__files['account'] = os.path.join(self.dir_db, self.__files['account'])
        self.__files['license'] = os.path.join(self.dir_db, self.__files['license'])
        self.__files['other_repo'] = os.path.join(self.dir_db, self.__files['other_repo'])
        self.__files['repo'] = os.path.join(self.dir_db, self.__files['repo'])
        """
        self.__OpenDb()

    def __OpenDb(self):
        # マスターDB生成（ファイル、テーブル、データ挿入）
        if None is self.lang:
            if not os.path.isfile(self.__files['lang']):
                m = database.src.language.Main.Main(self.__files['lang'])
                m.Run()
            self.lang = dataset.connect('sqlite:///' + self.__files['lang'])
        if None is self.api:
            self.api = dataset.connect('sqlite:///' + self.__files['api'])
            if not os.path.isfile(self.__files['api']):
                m = database.src.api.Main.Main(self.__files['api'])
                m.Run()
            self.api = dataset.connect('sqlite:///' + self.__files['api'])
        if None is self.gnu_license:
            self.gnu_license = dataset.connect('sqlite:///' + self.__files['gnu_license'])
            if not os.path.isfile(self.__files['gnu_license']):
                m = database.src.gnu_license.Main.Main(self.__files['gnu_license'])
                m.Run()
            self.gnu_license = dataset.connect('sqlite:///' + self.__files['gnu_license'])

        # アカウントDB生成（ファイル、テーブル作成。データ挿入はCUIにて行う）
        if None is self.account:
            self.account = dataset.connect('sqlite:///' + self.__files['account'])
            if not os.path.isfile(self.__files['account']):
                m = database.src.account.Main.Main(self.__files['account'])
                m.Create()
            self.account = dataset.connect('sqlite:///' + self.__files['account'])

        # DB作成にTokenが必要なもの
        if 0 < self.account['Accounts'].count():
            # ライセンスDB生成（ファイル、テーブル作成。データ挿入）            
            if not(os.path.isfile(self.__files['license'])):
                print('lllllllllllllllllllllllllllllicense Create.')
                print(self.__files['license'])
                user = web.service.github.api.v3.CurrentUser.CurrentUser(self, self.account['Accounts'].find().next()['Username'])
                client = web.service.github.api.v3.Client.Client(self, user, None)
                l = database.src.license.Main.Main(self, client)
                l.Create()
                self.license = dataset.connect('sqlite:///' + self.__files['license'])
                l.Insert()
            self.license = dataset.connect('sqlite:///' + self.__files['license'])
            # 自分アカウントのリポジトリDB生成（ファイル、テーブル作成。データ挿入）
            for account in self.account['Accounts'].find():
                self.__OpenRepo(account['Username'])
            # 他者アカウントのリポジトリDB生成（ファイル、テーブル作成。データ挿入）

    def __OpenRepo(self, username):
        is_create = False
        path = self.__files['repo'].replace('{user}', username)
        if not(os.path.isfile(path)):
            # DBテーブル作成
            path_sh = os.path.join(self.__path_dir_this, 'repo/create/Create.sh')
            subprocess.call(shlex.split("bash \"{0}\" \"{1}\"".format(path_sh, path)))
            self.repos[username] = dataset.connect('sqlite:///' + path)
            # DBレコード挿入
            user = web.service.github.api.v3.CurrentUser.CurrentUser(self, username)
            # ダミー引数を渡す
            repo = web.service.github.api.v3.CurrentRepository.CurrentRepository(self, os.path.abspath(os.path.dirname(__file__)), description="args.description",  homepage="args.homepage")
            client = web.service.github.api.v3.Client.Client(self, user, repo)
            inserter = database.src.repo.insert.Main.Main(self, client, user, repo)
            inserter.Initialize()
        if not(username in self.repos.keys()):
            self.repos[username] = dataset.connect('sqlite:///' + path)           

