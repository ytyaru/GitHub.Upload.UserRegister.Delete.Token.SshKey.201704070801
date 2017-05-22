#!python3
#encoding:utf-8
import os.path
import dataset
#from tkinter import Tk
class RequestParam:
    def __init__(self, db, user):
#    def __init__(self, data):
#        self.data = data
#        self.__username = self.data.get_username()
        self.__db = db
        self.__user = user
        self.auth_param = RequestParam.AuthParam(self.__db, self.__user)
#        self.auth_param = RequestParam.AuthParam(self.data)
        self.params = None

#    def get_username(self):
#        return self.data.get_username()

    """
    デフォルトのHTTPヘッダを取得する。
    API用DBに問い合わせずに取得できる。
    @param {array} scopesはAPIに必要な権限。['repo',`delete_repo`]など。未設定ならScopeに関係なく適当なTokenを取得する。
    @return {dict} HTTPHeader。
    """
    def get_default(self, scopes=None):
        return {
            "Time-Zone": "Asia/Tokyo",
            "Authorization": "token {0}".format(self.__user.GetAccessToken(scopes)),
#            "Authorization": "token {0}".format(self.data.get_access_token(scopes)),
            "Accept": "application/vnd.github.v3+json",
        }

    """
    APIごとに適切なHttpHeaderを返す。
    * API毎に異なる認証方法(Basic,Token)(未実装:OAuth,TwoFactor)
    * API毎に異なる必要scope
    * API毎に異なる必要Accept(未実装)
    * アカウントと時刻ごとに異なるOTP(未実装)
    * 国ごとに異なるTimeZone(未実装)
    http_methodとendpointでAPIを一意に特定する。
    """
    def get(self, http_method=None, endpoint=None):
        params = self.auth_param.get(http_method, endpoint)
        if not("headers" in params.keys()):
            params['headers'] = {}
        params['headers'].update({"Time-Zone": "Asia/Tokyo"})
        if not("Accept" in params['headers'].keys()):
            params['headers'].update({"Accept": "application/vnd.github.v3+json"})
        self.params = params
        return self.params

    """
    一定時間ごとに変化するワンタイムパスワード(OTP)を取得してHttpHeaderに設定する（未実装）
    """
    def update_otp(self, params):
        secret = self.__user.TwoFactorSecret
        # SecretからOTPを算出する
        # X-GitHub-OTPヘッダキーにOTPを設定する
        """
        otp = self.auth_param.get_otp()
        if None is otp:
            return params
        if None is not params:
            if not('headers' in params):
                params['headers'] = {}
            params['headers']['X-GitHub-OTP'] = otp
        """
        return params
        
    class AuthParam:
        def __init__(self, db, user):
#        def __init__(self, data):
#            self.data = data
            self.__db = db
            self.__user = user
#            self.__username = self.data.get_username()

        """
        APIごとに適切なHttpHeaderを返す。
        * API毎に異なる認証方法(Basic,Token)(未実装:OAuth,TwoFactor)
        * API毎に異なる必要scope
        * アカウントと時刻ごとに異なるOTP(未実装)
        """
        def get(self, http_method, endpoint):
            params = {}
            account = self.__db.account['Accounts'].find_one(Username=self.__user.Name)
            api = self.__db.api['Apis'].find_one(HttpMethod=http_method.upper(), Endpoint=endpoint)
            if None is api:
                return __get_default_headers()
            print(api)
            print(api['Grants'])
            print("type(Grants)1: {0}".format(type(api['Grants'])))
            print("len(Grants)1: {0}".format(len(api['Grants'])))
            print("len(Grants)2: {0}".format(len(api['Grants'].split(","))))
            if ("Token" in api['AuthMethods']):
                grants = api['Grants'].split(",")
                if not(None is grants) and 0 == len(grants):
                    grants = None
                if not(None is grants) and 1 == len(grants) and '' == grants[0]:
                    grants = None
                token = self.__user.GetAccessToken(grants)
#                token = self.__get_access_token(account['Id'], api['Grants'].split(","))
                params['headers'] = {"Authorization": "token " + token}
            elif ("ClientId" in api['AuthMethods']):
                raise Exception('Not implemented clientId authorization.')
            elif ("Basic" in api['AuthMethods']):
#                params['auth'] = (self.__username, account['Password'])
#                two_factor = self.__db.account['TwoFactors'].find(AccountId=account['Id'])
                params['auth'] = (self.__user.Name, self.__user.Password)
                if None is not self.__user.Otp:
                    params['headers'] = {"X-GitHub-OTP": self.__user.Otp}
#                two_factor = self.__db.account['TwoFactors'].find(AccountId=account['Id'])
#                if not(None is two_factor):
#                    """
#                    t = Tk()
#                    otp = t.clipboard_get()
#                    t.destroy()
#                    """
#                    otp = "some_otp"
#                    params['headers'] = {"X-GitHub-OTP": otp}
            else:
                raise Exception('Not found AuthMethods: {0} {1}'.format(api['HttpMethod'], api['Endpoint']))
            return params

        """
        デフォルトのHTTPヘッダを取得する。
        @param {array} scopesはAPIに必要な権限。['repo',`delete_repo`]など。未設定ならScopeに関係なく適当なTokenを取得する。
        @return {dict} HTTPHeader。
        """
        def __get_default_headers(self, scopes=None):
            return {
                "Time-Zone": "Asia/Tokyo",
                "Authorization": "token {0}".format(self.data.get_access_token(scopes)),
                "Accept": "application/vnd.github.v3+json",
            }
        """
        def __get_access_token(self, account_id, scopes):
            sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(account_id)
            if (not(None is scopes) and (0 < len(scopes)) and (0 < len(scopes[0]))):
                sql = sql + " AND ("
                for s in scopes:
                    sql = sql + "(',' || Scopes || ',') LIKE '%,{0},%'".format(s) + " OR "
                sql = sql.rstrip(" OR ")
                sql = sql + ')'
            print(sql)
            tokens = self.__db.account.query(sql)
            token = None
            for t in tokens:
               token = t['AccessToken']
            return token
        """
        def get_otp(self):
            account = self.__db.account['Accounts'].find_one(Username=self.__user.Name)
#            two_factor = self.__db.account['TwoFactors'].find(AccountId=account['Id'])
            two_factor = self.__db.account['TwoFactors'].find_one(AccountId=account['Id'])
            print('------------------------------')
            print(two_factor)
            print('------------------------------')
            if None is two_factor:
                return None
            else:
                """
                t = Tk()
                otp = t.clipboard_get()
                t.destroy()
                """
                otp = '(未実装)'
                return otp
