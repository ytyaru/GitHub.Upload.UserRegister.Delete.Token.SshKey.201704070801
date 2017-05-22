import os.path
import re
from requests.structures import CaseInsensitiveDict

class SshConfigurator(object):
    def __init__(self):
        self.__re_host = re.compile('host ', re.IGNORECASE)
        self.__re_indent = re.compile('[ \t]+', re.IGNORECASE)
        self.__re_ext_pub = re.compile('.+\.pub$', re.IGNORECASE)
        self.__text = None
        self.__hosts = {}
        self.__path_file_config = None

    def __GetPathConfig(self):
        return self.__path_file_config
    ConfigFilePath = property(__GetPathConfig)

    def __GetHosts(self):
        return self.__hosts
    Hosts = property(__GetHosts)

    def Load(self, path=None):
        if None is path:
            path_dir_ssh = os.path.join(os.path.expanduser('~'), '.ssh/')
#            path_dir_ssh = "/tmp/.ssh/" # テスト用
            self.__path_file_config = os.path.join(path_dir_ssh, 'config')
        else:
            self.__path_file_config = path
        with open(self.__path_file_config) as f:
            self.__text = f.read()
            self.__Parse()

    def __Parse(self):
        nowHost = None
        for line in self.__text.split('\n'):
            # Host定義行なら
            if self.__re_host.match(line):
                nowHost = re.sub(self.__re_host, '', line).strip()
                # すでに存在する場合無視する（同一Host定義のうち、最初に見つかった定義を使う。後に見つかった定義は無視する）
                if nowHost in self.__hosts.keys():
                    nowHost = None
                    continue
                self.__hosts[nowHost] = CaseInsensitiveDict()
                self.__AppendHostStatus(nowHost, line)
            # 行頭がインデントされているならnowHost内の定義行と解釈する
            elif self.__re_indent.match(line):
                self.__AppendHostStatus(nowHost, line)
            else:
                # コメント行と空行は無視する
                if '#' == line[0:1] or 0 == len(line.strip()):
                    continue
                # Host外の設定ならHost内定義フラグを折る
                else:
                    nowHost = None

    def __AppendHostStatus(self, nowHost, line):
        # Host内定義行なら
        if None is not nowHost:
            elements = line.split()
            if 2 == len(elements):
                self.__hosts[nowHost].update({elements[0]: elements[1]})

    """
    指定したHostを追記する。~/.ssh/configファイルの末尾に。
    """
    def AppendHost(self, username, IdentityFile, Port=22):
        # ファイルが存在しないなら新規作成する
        if not(os.path.isfile(self.__path_file_config)):
            with open(self.__path_file_config, 'w') as f:
                pass        
        # configファイルの末尾に追記する
        with open(self.__path_file_config, 'a') as f:
            host = self.__GetConfigTextHost(username)
            f.write(self.__GetConfigTextNewHost(host, IdentityFile, Port=Port))
            return host

    def __GetConfigTextHost(self, username):
        if None is username or 0 == len(username.strip()):
            raise Exception('Host名をつくるためにユーザ名を指定してください。')
        return 'github.com.{username}'.format(username=username)

    """
    指定したHost設定のconfig文字列を作る。
    """
    def __GetConfigTextNewHost(self, Host, IdentityFile, Port=22):
        append = '''\
Host {Host}
  User git
  Port {Port}
  HostName github.com
  IdentityFile {IdentityFile}
  TCPKeepAlive yes
  IdentitiesOnly yes
'''

    """
    def DeleteHost(self, host):
        if hostname in self.Hosts:
            re.sub(self.CreateHost(), repl, string, flags=(re.MULTILINE | re.DOTALL))
    """
    """
    指定したHostの設定一式を削除する。
    """
    def DeleteHost(self, host):
        with open(self.__path_file_config, 'w') as f:
            self.__text = self.__GetConfigTextAfterDeletedHost(host)
            f.write(self.__text)
#            self.__Parse()
            del self.__hosts[host]

    """
    指定したHostの設定を削除した後のconfigファイル内容を返す。
    事前にLoad()しておくこと。
    """
    def __GetConfigTextAfterDeletedHost(self, targetHost):
        if None is targetHost or 0 == len(targetHost.strip()):
            return self.__text
        afterText = ""
        nowHost = None
        for line in self.__text.split('\n'):
            # Host定義行なら
            if self.__re_host.match(line):
                nowHost = re.sub(self.__re_host, '', line).strip()
                if nowHost != targetHost:
                    nowHost = None
                    continue
            elif None is not nowHost and nowHost == targetHost:
                # 行頭がインデントされているならnowHost内の定義行と解釈する
                if self.__re_indent.match(line):
                    continue
            else:
                afterText += line + '\n'
        return afterText
    
    """
    configファイルから指定Hostの秘密鍵ファイルパスを取得する。秘密鍵と公開鍵は同一ディレクトリにあると仮定する。
    """
    def GetPrivateKeyFilePath(self, host):
        if self.__re_ext_pub.match(self.Hosts[host]['IdentityFile']):
            return self.Hosts[host]['IdentityFile'][:-4]
        else:
            return self.Hosts[host]['IdentityFile']

    """
    configファイルから指定Hostの公開鍵ファイルパスを取得する。秘密鍵と公開鍵は同一ディレクトリにあると仮定する。
    """
    def GetPublicKeyFilePath(self, host):
        if self.__re_ext_pub.match(self.Hosts[host]['IdentityFile']):
            return self.Hosts[host]['IdentityFile']
        else:
            return self.Hosts[host]['IdentityFile'] + '.pub'

