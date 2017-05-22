#!python3
#encoding:utf-8
import os.path
import dataset
import database.src.Database
import cui.register.github.api.v3.authorizations.Authorizations
import cui.register.github.api.v3.users.SshKeys
import cui.register.github.api.v3.users.Emails
import cui.register.SshConfigurator
class Deleter:
    def __init__(self):
        self.__db = None

    def Delete(self, args):
        print('Account.Delete')
        print(args)
        print('-u: {0}'.format(args.username))
        print('--auto: {0}'.format(args.auto))
        
        self.__db = database.src.Database.Database()
        self.__db.Initialize()
        
        account = self.__db.account['Accounts'].find_one(Username=args.username)
        print(account)
        if None is account:
            print('指定したユーザ {0} がDBに存在しません。削除を中止します。'.format(args.username))
            return
        else:
            # 1. 指定ユーザの全Tokenを削除する（SSHKey設定したTokenのはずなのでSSHKeyも削除される
            self.__DeleteToken(account)
            # 2. SSHのconfigファイル設定の削除と鍵ファイルの削除
            self.__DeleteSshFile(self.__db.account['SshConfigures'].find_one(AccountId=account['Id'])['HostName'])
            # 3. DB設定値(Account, Repository)
            self.__DeleteDatabase(account)
            # * GitHubアカウントの退会はサイトから行うこと
        
        # 作成したアカウントのリポジトリDB作成や、作成にTokenが必要なライセンスDBの作成
        self.__db.Initialize()
        return self.__db

    def __DeleteToken(self, account):
        # 1. Tokenの新規作成
        auth = cui.register.github.api.v3.authorizations.Authorizations.Authorizations(account['Username'], account['Password'])
        for token in self.__db.account['AccessTokens'].find(AccountId=account['Id']):
            auth.Delete(token['IdOnGitHub'], account['Username'], account['Password'])

    def __DeleteSshFile(self, hostname):
        sshconf = cui.register.SshConfigurator.SshConfigurator()
        sshconf.Load()
        # SSH鍵ファイル削除
        path_private = sshconf.GetPrivateKeyFilePath(hostname)
        path_public = sshconf.GetPublicKeyFilePath(hostname)
        if os.path.isfile(path_private):
            os.remove(path_private)
        if os.path.isfile(path_public):
            os.remove(path_public)
        # SSHconfigファイルの指定Host設定削除
        if hostname in sshconf.Hosts:
            sshconf.DeleteHost(hostname)
    
    def __DeleteDatabase(self, account):
        path = self.__db.Paths['repo'].format(user=account['Username'])
        if os.path.isfile(path):
            os.remove(path)
        self.__db.account['SshConfigures'].delete(AccountId=account['Id'])
        self.__db.account['SshKeys'].delete(AccountId=account['Id'])
        self.__db.account['TwoFactors'].delete(AccountId=account['Id'])
        self.__db.account['AccessTokens'].delete(AccountId=account['Id'])
        self.__db.account['Accounts'].delete(Id=account['Id'])

