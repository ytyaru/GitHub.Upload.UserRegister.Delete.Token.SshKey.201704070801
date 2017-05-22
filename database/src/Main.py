#!python3
#encoding:utf-8

# configで指定したディレクトリにDBがない場合、作成する
import configparser
import os.path
import Create
config = configparser.ConfigParser()
config.read('./config.ini')
print(config['Path']['DB'])
print(os.path.abspath(config['Path']['DB']))
creator = Create.InitializeMasterDbCreator(os.path.abspath(config['Path']['DB']))
creator.Run()

