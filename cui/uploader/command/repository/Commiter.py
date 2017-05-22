#!python3
#encoding:utf-8
import subprocess
import shlex
import time
import requests
import json

class Commiter:
    def __init__(self, db, client, user, repo):
#    def __init__(self, db, client):
#    def __init__(self, data, client):
#        self.data = data
        self.__db = db
        self.__client = client
        self.__user = user
        self.__repo = repo

    def ShowCommitFiles(self):
        subprocess.call(shlex.split("git add -n ."))

    def AddCommitPush(self, commit_message):
        subprocess.call(shlex.split("git add ."))
        subprocess.call(shlex.split("git commit -m '{0}'".format(commit_message)))
        subprocess.call(shlex.split("git push origin master"))
        time.sleep(3)
        self.__InsertLanguages(self.__client.repo.list_languages())

    def __InsertLanguages(self, j):
        self.__user.RepoDb.begin()
        repo_id = self.__user.RepoDb['Repositories'].find_one(Name=self.__repo.Name)['Id']
        self.__user.RepoDb['Languages'].delete(RepositoryId=repo_id)
        for key in j.keys():
            self.__user.RepoDb['Languages'].insert(dict(
                RepositoryId=repo_id,
                Language=key,
                Size=j[key]
            ))
        self.__user.RepoDb.commit()

