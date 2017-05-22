#!/usr/bin/python3
#!python3
#encoding:utf-8
import os.path
import subprocess
import cui.uploader.command.repository.Creator
import cui.uploader.command.repository.Commiter
import cui.uploader.command.repository.Deleter
import cui.uploader.command.repository.Editor
import cui.uploader.command.aggregate.Aggregate

class Main:
    def __init__(self, db, client, user, repo):
#    def __init__(self, data, client):
#        self.__db = data
        self.__db = db
        self.__client = client
        self.__user = user
        self.__repo = repo
        self.creator = cui.uploader.command.repository.Creator.Creator(self.__db, self.__client, self.__user, self.__repo)
        self.commiter = cui.uploader.command.repository.Commiter.Commiter(self.__db, self.__client, self.__user, self.__repo)
        self.deleter = cui.uploader.command.repository.Deleter.Deleter(self.__db, self.__client, self.__user, self.__repo)
        self.editor = cui.uploader.command.repository.Editor.Editor(self.__db, self.__client, self.__user, self.__repo)
        self.agg = cui.uploader.command.aggregate.Aggregate.Aggregate(self.__db, self.__user, self.__repo)

    def Run(self):
        if -1 != self.__Create():
            self.__Commit()

    def __CreateInfo(self):
        print('ユーザ名: {0}'.format(self.__user.Name))
        print('メアド: {0}'.format(self.__user.MailAddress))
        print('SSH HOST: {0}'.format(self.__user.SshHost))
        print('リポジトリ名: {0}'.format(self.__repo.Name))
        print('説明: {0}'.format(self.__repo.Description))
        print('URL: {0}'.format(self.__repo.Homepage))
        print('リポジトリ情報は上記のとおりで間違いありませんか？[y/n]')

    def __Create(self):
        if os.path.exists(".git"):
            return 0
        answer = ''
        while '' == answer:
            self.__CreateInfo()
            answer = input()
            if 'y' == answer or 'Y' == answer:
                self.creator.Create()
                return 0
            elif 'n' == answer or 'N' == answer:
                print('call.shを編集して再度やり直してください。')
                return -1
            else:
                answer = ''

    def __CommitInfo(self):
        print('リポジトリ名： {0}/{1}'.format(self.__user.Name, self.__repo.Name))
        print('説明: {0}'.format(self.__repo.Description))
        print('URL: {0}'.format(self.__repo.Homepage))
        print('----------------------------------------')
        self.commiter.ShowCommitFiles()
        print('commit,pushするならメッセージを入力してください。Enterかnで終了します。')
        print('サブコマンド    n:終了 a:集計 e:編集 d:削除 i:Issue作成')

    def __Commit(self):
        while (True):
            self.__CommitInfo()
            answer = input()
            if '' == answer or 'n' == answer or 'N' == answer:
                print('終了します。')
                break
            elif 'a' == answer or 'A' == answer:
                self.agg.Show()
            elif 'e' == answer or 'E' == answer:
                self.__ConfirmEdit()
            elif 'd' == answer or 'D' == answer:
                self.__ConfirmDelete()
                break
            elif 'i' == answer or 'I' == answer:
                print('(Issue作成する。(未実装))')
            else:
                self.commiter.AddCommitPush(answer)
                self.agg.Show()

    def __ConfirmDelete(self):
        print('.gitディレクトリ、対象リモートリポジトリ、対象DBレコードを削除します。')
        print('リポジトリ名： {0}/{1}'.format(self.__user.Name, self.__repo.Name))
        self.deleter.ShowDeleteRecords()
        print('削除すると復元できません。本当に削除してよろしいですか？[y/n]')
        answer = input()
        if 'y' == answer or 'Y' == answer:
            self.deleter.Delete()
            print('削除しました。')
            return True
        else:
            print('削除を中止しました。')
            return False

    def __ConfirmEdit(self):
        print('編集したくない項目は無記入のままEnterキー押下してください。')

        print('リポジトリ名を入力してください。')
        name = input()
        if None is name or '' == name:
            # 名前は必須項目。変更しないなら現在の名前をセットする
            name = self.__repo.Name
        print('説明文を入力してください。')
        description = input()
        print('Homepageを入力してください。')
        homepage = input()
        
        if '' == description and '' == homepage and self.__repo.Name == name:
            print('編集する項目がないため中止します。')
        else:
            self.editor.Edit(name, description, homepage)
            print('編集しました。')
