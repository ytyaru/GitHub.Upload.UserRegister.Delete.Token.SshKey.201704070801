#!python3
#encoding:utf-8
import os.path
class CurrentRepository(object):
    def __init__(self, db, path, **params):
        self.__db = db
        self.__path = None
        self.__name = None
        self.__SetPath(path)
        self.__description = None
        self.__homepage = None
        print(params)
        if None is not params:
            if 'description' in params.keys():
                self.__description = params['description']
            if 'homepage' in params.keys():
                self.__homepage = params['homepage']

    def __GetPath(self):
        return self.__path
    def __SetPath(self, path):
        if os.path.isdir(path):
            self.__path = path
            if path.endswith('/'):
                path = os.path.basename(path[:-1])
            self.__name = os.path.basename(path)
    Path = property(__GetPath, __SetPath)

    def __GetName(self):
        return self.__name
    Name = property(__GetName)

    def __GetDescription(self):
        return self.__description
    Description = property(__GetDescription)

    def __GetHomepage(self):
        return self.__homepage
    Homepage = property(__GetHomepage)

    # 将来的には拡張する
    # * リモートリポジトリの状態(private,has_wiki)を変更する
    # * GitHubサーバとの連動(Sync()メソッドでAPIから取得しDBを更新する)
