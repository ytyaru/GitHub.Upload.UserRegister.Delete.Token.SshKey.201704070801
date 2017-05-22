#!python3
#encoding:utf-8
import time
import pytz
import requests
import json
import datetime
class Inserter:
    def __init__(self, db, client, user, repo):
#    def __init__(self, db, client):
#    def __init__(self, data, client):
#        self.data = data
        self.__db = db
        self.__client = client
        self.__user = user
        self.__repo = repo
        self.__now = datetime.datetime.now()

    def Show(self, username=None):
        self.__user.RepoDb['Repositories'].find(order_by=['Name'])
        print("{0},{1},{2}".format('Owner','RepoName','License'))
        for repo in db_repo.query('select Repositories.Owner,Repositories.Name,Licenses.LicenseId from Repositories left join Licenses on Repositories.Id=Licenses.RepositoryId;'):
            print("{0},{1},{2}".format(repo['Owner'],repo['Name'],self.__db.license['Licenses'].find_one(Id=repo['LicenseId'])['Key']))

    def Insert(self, username=None):
        jsons = self.__client.repo.gets(sort='created', direction='asc', per_page=100)
        print("json数={0}".format(len(jsons)))
        for j in jsons:
            if 0 == self.__user.RepoDb['Repositories'].count(Name=j['name']):
                self.__user.RepoDb['Repositories'].insert(self.__CreateRecordRepository(j))
                r = self.__user.RepoDb['Repositories'].find_one(Name=j['name'])
                print(r)
                self.__user.RepoDb['Counts'].insert(self.__CreateRecordCount(r['Id'], j))
                self.__InsertLanguages(r['Id'], self.__user.Name, j['name'])
                
                # リポジトリにライセンスがないなら
                if None is j['license']:
                    self.__user.RepoDb['Licenses'].insert(self.__CreateRecordRepositoryLicenses(r['Id'], None))
                    continue
                # ライセンスのkeyが`other`なら
                if ('other' == j['license']['key']):
                    self.__InsertOtherLicense(j['license'])
                else:
                    # 対象リポジトリのライセンスがマスターテーブルに存在しないなら、APIで取得してDBへ挿入する
                    if None is self.__db.license['Licenses'].find_one(Key=j['license']['key']):
#                        self.__db.license['Licenses'].insert(self.__CreateRecordLicense(self.license.License(j['license']['key'])))
                        self.__db.license['Licenses'].insert(self.__CreateRecordLicense(self.__client.license.GetLicense(j['license']['key'])))
                print(j['license']['key'])
                print(self.__db.license['Licenses'].count())
                print(self.__db.license['Licenses'].find_one(Key=j['license']['key']))
                print(self.__db.license['Licenses'].find_one(Key=j['license']['key'])['Id'])
                print(r['Id'])
                self.__user.RepoDb['Licenses'].insert(self.__CreateRecordRepositoryLicenses(r['Id'], self.__db.license['Licenses'].find_one(Key=j['license']['key'])['Id']))

    def __CreateRecordLicense(self, j):
        return dict(
            Key=j['key'],
            Name=j['name'],
            SpdxId=j['spdx_id'],
            Url=j['url'],
            HtmlUrl=j['html_url'],
            Featured=self.__BoolToInt(j['featured']),
            Description=j['description'],
            Implementation=j['implementation'],
            Permissions=self.__ArrayToString(j['permissions']),
            Conditions=self.__ArrayToString(j['conditions']),
            Limitations=self.__ArrayToString(j['limitations']),
            Body=j['body']
        )
    def __CreateRecordRepository(self, j):
        return dict(
            IdOnGitHub=j['id'],
#            Owner=j['owner']['login'],
            Name=j['name'],
            Description=j['description'],
            Homepage=j['homepage'],
            CreatedAt=j['created_at'],
            PushedAt=j['pushed_at'],
            UpdatedAt=j['updated_at'],
            CheckedAt="{0:%Y-%m-%dT%H:%M:%SZ}".format(self.__now)
        )
    def __CreateRecordCount(self, repo_id, j):
        return dict(
            RepositoryId=repo_id,
            Forks=j['forks_count'],
            Stargazers=j['stargazers_count'],
            Watchers=j['watchers_count'],
            Issues=j['open_issues_count']
        )
    def __CreateRecordRepositoryLicenses(self, repo_id, license_id):
        return dict(
            RepositoryId = repo_id,
            LicenseId = license_id
        )
    def __InsertLanguages(self, repo_id, username, repo_name):
        # 対象リポジトリの言語レコードがDBに存在しないとき、APIで取得しDBへ挿入する
        if (self.__user.RepoDb['Languages'].count(RepositoryId=repo_id) == 0):
#            j = self.license.Languages(username, repo_name)
#            j = self.__client.repo.list_languages(repo_name, username=username)
            j = self.__client.repo.list_languages(username=username, repo_name=repo_name)
            for key in j.keys():
                self.__user.RepoDb['Languages'].insert(dict(
                    RepositoryId=repo_id, 
                    Language=key, 
                    Size=j[key]))

    # リポジトリのライセンスkeyが`other`の場合
    # "license":{"key":"other","name":"Other","spdx_id":null,"url":null,"featured":false}
    # https://github.com/kennethreitz/requests
    # LICENSEには`Apache License, Version 2.0`とあるがGitHubAPIの結果はkey:`other`である謎。
    def __InsertOtherLicense(self,j):
        if None is self.__db.license['Licenses'].find_one(Key=j['key']):
            print('otherライセンス追加。')
            self.__db.license['Licenses'].insert(dict(
                Key=j['key'],
                Name=j['name'],
                SpdxId=j['spdx_id'],
                Url=j['url'],
                HtmlUrl=None,
                Featured=self.__BoolToInt(j['featured']),
                Description=None,
                Implementation=None,
                Permissions=None,
                Conditions=None,
                Limitations=None,
                Body=None
            ))

    def __BoolToInt(self, bool_value):
        if True == bool_value:
            return 1
        else:
            return 0

    def __ArrayToString(self, array):
        ret = ""
        for v in array:
            ret = v + ','
        return ret[:-1]
