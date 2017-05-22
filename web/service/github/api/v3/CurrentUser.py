#!python3
#encoding:utf-8
class CurrentUser(object):
    def __init__(self, db, username):
        self.__db = db
        self.__username = None
        self.Change(username)
        self.__password = None
        self.__ssh_host = None
        self.__mail = None

    def __GetRepoDb(self):
        try:
            return self.__db.repos[self.Name]
        finally:
            print(self.__db.repos.keys())
    RepoDb = property(__GetRepoDb)

    def __GetSelectableUsernames(self):
        names = []
        for a in self.__db.account['Accounts'].find():
            names.append(a['Username'])
        return names
    SelectableUsernames = property(__GetSelectableUsernames)
    
    def __GetName(self):
        return self.__username
    def Change(self, username):
        if None is not self.__db.account['Accounts'].find_one(Username=username):
            self.__username = username        
    Name = property(__GetName, Change)
    
    def __GetPassword(self):
        return self.__db.account['Accounts'].find_one(Username=self.Name)['Password']
    Password = property(__GetPassword)
    
    def __GetMailAddress(self):
        return self.__db.account['Accounts'].find_one(Username=self.Name)['MailAddress']
    MailAddress = property(__GetMailAddress)
    
    def __GetSshHost(self):
        return "github.com.{0}".format(self.Name)
    SshHost = property(__GetSshHost)
    
#    def __GetOtp(self):
#        # 2FA-Secretから算出する
#        return self.__otp
#    Otp = property(__GetOtp)

    def __GetTwoFactorSecret(self):
        account_id = self.__db.account['Accounts'].find_one(Username=self.Name)['Id']
        print(account_id)
        two_fac = self.__db.account['TwoFactors'].find_one(AccountId=account_id)
        if None is two_fac:
            return None
        else:
            return two_fac['Secret']
#        return self.__db.account['TwoFactors'].find_one(AccountId=account_id)['Secret']
    TwoFactorSecret = property(__GetTwoFactorSecret)
    
    def GetAccessToken(self, scopes=None):
        sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(self.__db.account['Accounts'].find_one(Username=self.Name)['Id'])
        if not(None is scopes) and isinstance(scopes, list) and 0 < len(scopes):
            sql = sql + " AND ("
            for s in scopes:
                sql = sql + "(',' || Scopes || ',') LIKE '%,{0},%'".format(s) + " OR "
            sql = sql.rstrip(" OR ")
            sql = sql + ')'
        print(scopes)
        print(sql)
        res = self.__db.account.query(sql)
        ret = None
        for r in res:
            print(r)
            ret = r
        return ret['AccessToken']
#        return self.__db.account.query(sql).next()['AccessToken']

    # 将来的には拡張したい
    # * OTP対応
    # * プロフィールなどユーザ情報の設定
    # * GitHubサーバとの連動(Sync()メソッドでAPIから取得しDBを更新する)
