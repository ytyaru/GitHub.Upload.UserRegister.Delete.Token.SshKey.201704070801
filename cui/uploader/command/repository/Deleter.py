#!python3
#encoding:utf-8
import os
import subprocess
import shlex
import shutil
import time
import pytz
import requests
import json
import datetime

class Deleter:
    def __init__(self, db, client, user, repo):
#    def __init__(self, db, client):
#    def __init__(self, data, client):
#        self.__db = data
        self.__db = db
        self.__client = client
        self.__user = user
        self.__repo = repo

    def ShowDeleteRecords(self):
        repo = self.__user.RepoDb['Repositories'].find_one(Name=self.__repo.Name)
        print(repo)
        print(self.__user.RepoDb['Counts'].find_one(RepositoryId=repo['Id']))
        for record in self.__user.RepoDb['Languages'].find(RepositoryId=repo['Id']):
            print(record)

    def Delete(self):
        self.__DeleteLocalRepository()
        self.__client.repo.delete()
        self.__DeleteDb()

    def __DeleteLocalRepository(self):
        shutil.rmtree('.git')

    def __DeleteDb(self):
        repo = self.__user.RepoDb['Repositories'].find_one(Name=self.__repo.Name)
        self.__user.RepoDb.begin()
        self.__user.RepoDb['Repositories'].delete(Id=repo['Id'])
        self.__user.RepoDb['Counts'].delete(RepositoryId=repo['Id'])
        self.__user.RepoDb['Languages'].delete(RepositoryId=repo['Id'])
        self.__user.RepoDb.commit()

