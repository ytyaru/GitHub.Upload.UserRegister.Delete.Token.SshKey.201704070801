#!python3
#encoding:utf-8
import cui.register.command.Inserter
import cui.register.command.Deleter
class Main:
    def __init__(self, path_dir_db):
        self.path_dir_db = path_dir_db

    def Insert(self, args):
        inserter = cui.register.command.Inserter.Inserter()
        return inserter.Insert(args)

    def Update(self, args):
        print('Account.Update')
        print(args)
        print('-u: {0}'.format(args.username))
        print('-p: {0}'.format(args.password))
        print('-m: {0}'.format(args.mailaddress))
        print('-s: {0}'.format(args.ssh_host))
        print('-t: {0}'.format(args.two_factor_secret_key))
        print('-r: {0}'.format(args.two_factor_recovery_code_file_path))
        print('--auto: {0}'.format(args.auto))

    def Delete(self, args):
        deleter = cui.register.command.Deleter.Deleter()
        deleter.Delete(args)

    def Tsv(self, args):
        print('Account.Tsv')
        print(args)
        print('path_file_tsv: {0}'.format(args.path_file_tsv))
        print('--method: {0}'.format(args.method))

