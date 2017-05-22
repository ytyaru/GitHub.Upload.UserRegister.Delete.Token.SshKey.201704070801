#!python3
#encoding:utf-8
import os.path
import getpass
import database.src.repo.insert.command.repositories.Inserter
class Main:
    def __init__(self, db, client, user, repo):
#    def __init__(self, db, client):
#    def __init__(self, data, client):
#        self.data = data
        self.__db = db
        self.__client = client
        self.__user = user
        self.__repo = repo
        self.inserter = database.src.repo.insert.command.repositories.Inserter.Inserter(self.__db, self.__client, self.__user, self.__repo)
#        self.inserter = database.src.repo.insert.command.repositories.Inserter.Inserter(self.__db, self.__client)
#        self.inserter = database.src.repo.insert.command.repositories.Inserter.Inserter(self.data, self.__client)

    def Initialize(self):
        self.inserter.Insert()

    """
    def Initialize(self):
        path_this_dir = os.path.abspath(os.path.dirname(__file__))
        file_path = os.path.join(path_this_dir, "OtherRepositoryUrl.txt")
        with open(file_path, mode="r", encoding="utf-8") as f:
            url = True
            while url:
                url = f.readline().rstrip('\r\n')
                print(url)
                if len(url) == 0:
                    continue
                username = self.data.get_other_username(url)
                repo_name = self.data.get_other_repo_name(url)
                print("ユーザ名: " + username)
                print("リポジトリ名: " + repo_name)
                self.inserter.Insert(username, repo_name)
    """
    def Run(self):
        print('GitHubリポジトリ情報を取得します。')
        url = 'start'
        while '' != url:
            print('GitHubリポジトリのURLを入力してください。(未入力+Enterで終了)')
            print('サブコマンド    l:既存リポジトリ')
            url = input()
            if '' == url:
                break
            elif 'l' == url or 'L' == url:
                self.inserter.Show()
            else:
                username = self.data.get_other_username(url)
                repo_name = self.data.get_other_repo_name(url)
                print("ユーザ名: " + username)
                print("リポジトリ名: " + repo_name)
                # 未登録ならDBへ挿入する（GitHubAPIでリポジトリ情報、言語情報、ライセンス情報を取得して）
                self.inserter.Insert(username, repo_name)

