#!python3
#encoding:utf-8
import time
import pytz
import requests
import json
import datetime
class Inserter:
    def __init__(self, data, client):
        self.data = data
        self.client = client
        self.now = datetime.datetime.now()        

    def Show(self):
        self.data.db_other_repo['Repositories'].find(order_by=['Name'])
        print("{0},{1},{2}".format('Owner','RepoName','License'))
        for repo in self.data.db_other_repo.query('select Repositories.Owner,Repositories.Name,Licenses.LicenseId from Repositories left join Licenses on Repositories.Id=Licenses.RepositoryId;'):
            print("{0},{1},{2}".format(repo['Owner'],repo['Name'],self.data.db_license['Licenses'].find_one(Id=repo['LicenseId'])['Key']))
        
    def Insert(self, username, repo_name):
        # 対象リポジトリがDBに存在しないなら、APIで取得してDBへ挿入する
        repo = self.data.db_other_repo['Repositories'].find_one(Owner=username, Name=repo_name)
        if None is repo:
            j = self.client.license.GetRepositoryLicense(username, repo_name)
            # リポジトリにライセンスがないなら
            if None is j['license']:
                self.data.db_other_repo['Repositories'].insert(self.__CreateRecordRepository(j))
                repo = self.data.db_other_repo['Repositories'].find_one(Owner=username, Name=repo_name)
                self.data.db_other_repo['Counts'].insert(self.__CreateRecordCount(repo['Id'], j))
                self.data.db_other_repo['Licenses'].insert(self.__CreateRecordRepositoryLicenses(repo['Id'], None))
                self.__InsertLanguages(repo['Id'], username, repo_name)
                return 
                
            # ライセンスのkeyが`other`なら
            if ('other' == j['license']['key']):
                self.__InsertOtherLicense(j['license'])
            else:
                # 対象リポジトリのライセンスがマスターテーブルに存在しないなら、APIで取得してDBへ挿入する
                if None is self.data.db_license['Licenses'].find_one(Key=j['license']['key']):
                    self.data.db_license['Licenses'].insert(self.__CreateRecordLicense(self.client.license.GetLicense(j['license']['key'])))
            self.data.db_other_repo['Repositories'].insert(self.__CreateRecordRepository(j))
            repo = self.data.db_other_repo['Repositories'].find_one(Owner=username, Name=repo_name)
            self.data.db_other_repo['Counts'].insert(self.__CreateRecordCount(repo['Id'], j))
            print(j['license']['key'])
            print(self.data.db_license['Licenses'].find_one(Key=j['license']['key']))
            print(self.data.db_license['Licenses'].find_one(Key=j['license']['key'])['Id'])
            self.data.db_other_repo['Licenses'].insert(self.__CreateRecordRepositoryLicenses(repo['Id'], self.data.db_license['Licenses'].find_one(Key=j['license']['key'])['Id']))
            self.__InsertLanguages(repo['Id'], username, repo_name)

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
            Owner=j['owner']['login'],
            Name=j['name'],
            Description=j['description'],
            Homepage=j['homepage'],
            CreatedAt=j['created_at'],
            PushedAt=j['pushed_at'],
            UpdatedAt=j['updated_at'],
            CheckedAt="{0:%Y-%m-%dT%H:%M:%SZ}".format(self.now)
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
        if (self.data.db_other_repo['Languages'].count(RepositoryId=repo_id) == 0):
            j = self.client.repo.list_languages(username=username, repo_name=repo_name)
            for key in j.keys():
                self.data.db_other_repo['Languages'].insert(dict(
                    RepositoryId=repo_id, 
                    Language=key, 
                    Size=j[key]))

    # リポジトリのライセンスkeyが`other`の場合
    # "license":{"key":"other","name":"Other","spdx_id":null,"url":null,"featured":false}
    # https://github.com/kennethreitz/requests
    # LICENSEには`Apache License, Version 2.0`とあるがGitHubAPIの結果はkey:`other`である謎。
    def __InsertOtherLicense(self,j):
        if None is self.data.db_license['Licenses'].find_one(Key=j['key']):
            print('otherライセンス追加。')
            self.data.db_license['Licenses'].insert(dict(
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
