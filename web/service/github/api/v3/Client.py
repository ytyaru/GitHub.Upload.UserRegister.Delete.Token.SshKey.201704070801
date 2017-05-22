#!python3
#encoding:utf-8
import web.http.Response
import web.service.github.api.v3.Response
import web.service.github.api.v3.RequestParam
from web.service.github.api.v3.miscellaneous import Licenses
from web.service.github.api.v3.repositories import Repositories
class Client(object):
    def __init__(self, db, user, repo):
#    def __init__(self, data):
#        self.__data = data
#        self.__reqp = web.service.github.api.v3.RequestParam.RequestParam(self.__data)
        self.__db = db
        self.__user = user
        self.__repo = repo
        self.__reqp = web.service.github.api.v3.RequestParam.RequestParam(self.__db, self.__user)
        self.__response = web.service.github.api.v3.Response.Response()
#        self.license = Licenses.Licenses(self.__db, self.__user, self.__reqp, self.__response)
        self.license = Licenses.Licenses(self.__reqp, self.__response)
        self.repo = Repositories.Repositories(self.__reqp, self.__response, self.__user, self.__repo)
#        self.repo = Repositories.Repositories(self.__db, self.__user, self.__reqp, self.__response)
#        self.license = Licenses.Licenses(self.__data, self.__reqp, self.__response)
#        self.repo = Repositories.Repositories(self.__data, self.__reqp, self.__response)
