#!python3
#encoding:utf-8
import os.path
import subprocess
import shlex
import re
import datetime
import dataset
import database.src.Database
import cui.register.github.api.v3.authorizations.Authorizations
import cui.register.github.api.v3.users.SshKeys
import cui.register.github.api.v3.users.Emails
import web.sqlite.Json2Sqlite
import cui.register.SshConfigurator
class Inserter:
    def __init__(self):
        self.__j2s = web.sqlite.Json2Sqlite.Json2Sqlite()
        self.__db = None

    def Insert(self, args):
        print('Account.Insert')
        print(args)
        print('-u: {0}'.format(args.username))
        print('-p: {0}'.format(args.password))
        print('-s: {0}'.format(args.ssh_host))
        print('-t: {0}'.format(args.two_factor_secret_key))
        print('-r: {0}'.format(args.two_factor_recovery_code_file_path))
        print('--auto: {0}'.format(args.auto))

        self.__db = database.src.Database.Database()
        self.__db.Initialize()
        
        account = self.__db.account['Accounts'].find_one(Username=args.username)
        print(account)
        
        if None is account:
            # 1. Tokenの新規作成
            auth = cui.register.github.api.v3.authorizations.Authorizations.Authorizations(args.username, args.password)
            token = auth.Create(args.username, args.password, scopes=['repo', 'delete_repo', 'user', 'admin:public_key'], note='GitHubUserRegister.py {0}'.format('{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())))
            # 2. APIでメールアドレスを習得する。https://developer.github.com/v3/users/emails/
            mailaddress = self.__GetPrimaryMail(token['token'])
            # 3. SSHの生成と設定
            # 起動引数`-s`がないなら
            if None is args.ssh_host:
                # 3A-1. SSH鍵の新規作成
                ssh_key_gen_params = self.__SshKeyGen(args.username, mailaddress)
#                host = self.__SshConfig(args.username, ssh_key_gen_params['path_file_key_private'])
                sshconf = cui.register.SshConfigurator.SshConfigurator()
                sshconf.Load()
                host = sshconf.AppendHost(args.username, ssh_key_gen_params['path_file_key_private'])
                # 3A-2. SSH鍵をGitHubに登録してDBに挿入する
                api_ssh = cui.register.github.api.v3.users.SshKeys.SshKeys()
                j_ssh = api_ssh.Create(token['token'], mailaddress, ssh_key_gen_params['public_key'])
                # 3A-3. SSH接続確認
                self.__SshConnectCheck(host, 'git', ssh_key_gen_params['path_file_key_private'])
            else:
                # 3B-1. ~/.ssh/configから指定されたHostデータを取得する
                sshconf = cui.register.SshConfigurator.SshConfigurator()
                sshconf.Load()
                if not(args.ssh_host in sshconf.Hosts.keys()):
                    raise Exception('存在しないSSH Host名が指定されました。-s引数を指定しなければSSH鍵を新規作成して設定します。既存のSSH鍵を使用するなら~/.ssh/configファイルに設定すると自動で読み取ります。configファイルに設定済みのHost名は次の通りです。 {0}'.format(sshconf.Hosts.keys()))
                host = args.ssh_host
                ssh_key_gen_params = self.__LoadSshKeyFile(args, sshconf)                
                # 3B-2.GitHubのSSHにすでに設定されているか確認する
                j_ssh = self.__GetGitHubSsh(args.username, token['token'], mailaddress, ssh_key_gen_params['public_key'])
            # 4. 全部成功したらDBにアカウントを登録する
            self.__db.account['Accounts'].insert(self.__CreateRecordAccount(args, mailaddress))
            account = self.__db.account['Accounts'].find_one(Username=args.username)
            if None is not args.two_factor_secret_key:
                self.__db.account['AccessTokens'].insert(self.__CreateRecordTwoFactor(account['Id'], args))
            self.__db.account['AccessTokens'].insert(self.__CreateRecordToken(account['Id'], token, j_ssh['id']))
            self.__db.account['SshConfigures'].insert(self.__CreateRecordSshConfigures(account['Id'], host, ssh_key_gen_params))
            self.__db.account['SshKeys'].insert(self.__CreateRecordSshKeys(account['Id'], ssh_key_gen_params['private_key'], ssh_key_gen_params['public_key'], j_ssh))
        # 作成したアカウントのリポジトリDB作成や、作成にTokenが必要なライセンスDBの作成
        self.__db.Initialize()
        return self.__db

    def __GetPrimaryMail(self, token):
        emails = cui.register.github.api.v3.users.Emails.Emails()
        mails = emails.Gets(token)
        print(mails)
        for mail in mails:
            if mail['primary']:
                return mail['email']
                
    def __LoadSshKeyFile(self, args, sshconf):
        ssh_key_gen_params = {
            'type': None,
            'bits': None,
            'passphrase': None,
            'path_file_key_private': None,
            'path_file_key_public': None,
            'private_key': None,
            'public_key': None,
        }
        path_file_key_private = sshconf.GetPrivateKeyFilePath(args.ssh_host)
        path_file_key_public = sshconf.GetPublicKeyFilePath(args.ssh_host)
        ssh_key_gen_params.update({'path_file_key_public': path_file_key_public})
        ssh_key_gen_params.update({'path_file_key_private': path_file_key_private})
        print(ssh_key_gen_params['path_file_key_private'])
        print(ssh_key_gen_params['path_file_key_public'])
        """
        # SSH configファイルから設定値を読み取る
        if re.compile('.+\.pub$', re.IGNORECASE).match(sshconf.Hosts[args.ssh_host]['IdentityFile']):
            ssh_key_gen_params.update({'path_file_key_public': sshconf.Hosts[args.ssh_host]['IdentityFile']})
            ssh_key_gen_params.update({'path_file_key_private': sshconf.Hosts[args.ssh_host]['IdentityFile'][:-4]})
        else:
            ssh_key_gen_params.update({'path_file_key_private': sshconf.Hosts[args.ssh_host]['IdentityFile']})
            ssh_key_gen_params.update({'path_file_key_public': sshconf.Hosts[args.ssh_host]['IdentityFile'] + '.pub'})
        print(ssh_key_gen_params['path_file_key_private'])
        print(ssh_key_gen_params['path_file_key_public'])
        """
        # キーファイルから内容を読み取る
        with open(ssh_key_gen_params['path_file_key_private']) as f:
            ssh_key_gen_params['private_key'] = f.read()
        with open(ssh_key_gen_params['path_file_key_public']) as f:
            # 公開鍵ファイルはスペース区切りで`{ssh-rsa} {公開鍵} {コメント}`の形式になっている。
            # GitHubではコメント値は保持しない。よって`{ssh-rsa} {公開鍵}`の部分だけ渡す
            pub_keys = f.read().split()
            ssh_key_gen_params['public_key'] = pub_keys[0] + ' ' + pub_keys[1]
        
        # 暗号化強度の情報を取得する
        ssh_key_gen_params = self.__GetSshKeyGenList(ssh_key_gen_params)
        print(ssh_key_gen_params)
        return ssh_key_gen_params

    """
    SSH鍵ファイルの暗号化強度を取得する。
    ssh-keygen -l -f {秘密鍵ファイルパス}
    {bits} {AA:BB:CC...}  {comment} ({type})
    {bits}=`2048`, comment=`メアド@mail.com`, {type}=`(RSA)`
    """
    def __GetSshKeyGenList(self, ssh_key_gen_params):
        # 暗号化強度の情報を取得する
        cmd = 'ssh-keygen -l -f "{0}"'.format(ssh_key_gen_params['path_file_key_public'])
        print(cmd)
        p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout_data, stderr_data = p.communicate()
        stdout_utf8 = stdout_data.decode('utf-8')
        print(stdout_utf8)
        elements = stdout_utf8.split()
        print(elements)
        ssh_key_gen_params['bits'] = elements[0]
        elements[3] = elements[3][1:] # '(' 削除
        elements[3] = elements[3][:-1] # ')' 削除
        ssh_key_gen_params['type'] = elements[3].lower()
        return ssh_key_gen_params

    """
    GitHubにしたSSH設定を取得する。まだ無いなら設定する。
    """
    def __GetGitHubSsh(self, username, token, mailaddress, public_key):
        # GitHubのSSHにすでに設定されているか確認する
        api_ssh = cui.register.github.api.v3.users.SshKeys.SshKeys()
        j_sshs = api_ssh.Gets(username, token)
        print(j_sshs)
        j_sshkey = None
        for j in j_sshs:
            if j['key'] == public_key:
                j_sshkey = j
                print('一致一致一致一致一致一致一致一致一致一致一致一致一致')
                break
        j_ssh = None
        if None is j_sshkey:
            # 新規作成
            print('新規作成新規作成新規作成新規作成新規作成新規作成新規作成新規作成新規作成新規作成')
            j_ssh = api_ssh.Create(token, mailaddress, public_key)
        else:
            # 詳細情報取得
            print('詳細情報取得詳細情報取得詳細情報取得詳細情報取得詳細情報取得詳細情報取得')
            j_ssh = api_ssh.Get(token, j_sshkey['id'])
        return j_ssh

    def __SshKeyGen(self, username, mailaddress):
        # SSH鍵の生成
        path_dir_ssh = os.path.join(os.path.expanduser('~'), '.ssh/')
#        path_dir_ssh = "/tmp/.ssh/" # テスト用
        path_dir_ssh_keys = os.path.join(path_dir_ssh, 'github/')
        if not(os.path.isdir(path_dir_ssh_keys)):
            os.makedirs(path_dir_ssh_keys)
        protocol_type = "rsa" # ["rsa", "dsa", "ecdsa", "ed25519"]
        bits = 4096 # 2048以上推奨
        passphrase = '' # パスフレーズはあったほうが安全らしい。忘れるだろうから今回はパスフレーズなし。
        path_file_key_private = os.path.join(path_dir_ssh_keys, 'rsa_{0}_{1}'.format(bits, username))
        print(path_dir_ssh)
        print(path_dir_ssh_keys)
        print(path_file_key_private)
        command = 'ssh-keygen -t {p_type} -b {bits} -P "{passphrase}" -C "{mail}" -f "{path}"'.format(p_type=protocol_type, bits=bits, passphrase=passphrase, mail=mailaddress, path=path_file_key_private)
        print(command)
        subprocess.call(shlex.split(command))
        
        private_key = None
        with open(path_file_key_private, 'r') as f:
            private_key = f.read()
        public_key = None
        with open(path_file_key_private + '.pub', 'r') as f:
            public_key = f.read()
        
        ssh_key_gen_params = {
            'type': protocol_type,
            'bits': bits,
            'passphrase': passphrase,
            'path_file_key_private': path_file_key_private,
            'path_file_key_public': path_file_key_private + '.pub',
            'private_key': private_key,
            'public_key': public_key,
        }
        return ssh_key_gen_params

    """
    def __SshConfig(self, username, IdentityFile, Port=22):
        host = 'github.com.{username}'.format(username=username)
        append = '''\
Host {Host}
  User git
  Port {Port}
  HostName github.com
  IdentityFile {IdentityFile}
  TCPKeepAlive yes
  IdentitiesOnly yes
'''
        append = append.format(Host=host, Port=Port, IdentityFile=IdentityFile)
        print(append)
        path_dir_ssh = os.path.join(os.path.expanduser('~'), '.ssh/')
#        path_dir_ssh = "/tmp/.ssh/" # テスト用
        path_file_config = os.path.join(path_dir_ssh, 'config')
        if not(os.path.isfile(path_file_config)):
            with open(path_file_config, 'w') as f:
                pass        
        # configファイルの末尾に追記する
        with open(path_file_config, 'a') as f:
            f.write(append)
        
        return host
    """
    
    def __SshConnectCheck(self, host, config_user, path_file_key_private):
        command = "ssh -T git@{host}".format(host=host)
        print(command)
        # check_output()だと例外発生する
        # subprocess.CalledProcessError: Command 'ssh -T git@github.com.{user}' returned non-zero exit status 1
#        subprocess.check_output(command, shell=True, universal_newlines=True)
        subprocess.call(command, shell=True, universal_newlines=True)
        # Hi {user}! You've successfully authenticated, but GitHub does not provide shell access.

    def __CreateRecordAccount(self, args, mailaddress):
        return dict(
            Username=args.username,
            MailAddress=mailaddress,
            Password=args.password,
            CreateAt="1970-01-01T00:00:00Z"
        )
        # 作成日時はAPIのuser情報取得によって得られる。
        
    def __CreateRecordToken(self, account_id, j, ssh_key_id):
        return dict(
            AccountId=account_id,
            IdOnGitHub=j['id'],
            Note=j['note'],
            AccessToken=j['token'],
            Scopes=self.__j2s.ArrayToString(j['scopes']),
            SshKeyId=ssh_key_id
        )

    def __CreateRecordTwoFactor(self, account_id, args):
        return dict(
            AccountId=account_id,
            Secret=args.args.two_factor_secret_key
        )        

    def __CreateRecordSshConfigures(self, account_id, host, ssh_key_gen_params):
        return dict(
            AccountId=account_id,
            HostName=host,
            PrivateKeyFilePath=ssh_key_gen_params['path_file_key_private'],
            PublicKeyFilePath=ssh_key_gen_params['path_file_key_public'],
            Type=ssh_key_gen_params['type'],
            Bits=ssh_key_gen_params['bits'],
            Passphrase=ssh_key_gen_params['passphrase'],
        )

    def __CreateRecordSshKeys(self, account_id, private_key, public_key, j):
        return dict(
            AccountId=account_id,
            IdOnGitHub=j['id'],
            Title=j['title'],
            Key=j['key'],
            PrivateKey=private_key,
            PublicKey=public_key,
            Verified=self.__j2s.BoolToInt(j['verified']),
            ReadOnly=self.__j2s.BoolToInt(j['read_only']),
            CreatedAt=j['created_at'],
        )

