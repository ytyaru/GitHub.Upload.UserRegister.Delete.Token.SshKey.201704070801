#!python3
#encoding:utf-8
import requests
import urllib.parse
import json
import web.service.github.api.v3.Response
class Repositories:
    def __init__(self, reqp, response, user, repo):
#    def __init__(self, repo, user, reqp, response):
#    def __init__(self, db, user, reqp, response):
#    def __init__(self, data, reqp, response):
#        self.data = data
#        self.db = db
        self.repo = repo
        self.user = user
        self.reqp = reqp
        self.response = response

    def create(self, name, description=None, homepage=None):
        method = 'POST'
        endpoint = 'user/repos'
        params = self.reqp.get(method, endpoint)
        params['data'] = json.dumps({"name": name, "description": description, "homepage": homepage})
        print(params)
        r = requests.post(urllib.parse.urljoin("https://api.github.com", endpoint), headers=params['headers'], data=params['data'])
        return self.response.Get(r)
        
    def gets(self, visibility=None, affiliation=None, type=None, sort='full_name', direction=None, per_page=30):
        if (visibility is None) and (affiliation is None) and (type is None):
            type = 'all'
        self.__raise_param_error(visibility, ['all', 'public', 'private'], 'visibility')
        if not(None is affiliation):
            for a in affiliation.split(','):
                self.__raise_param_error(a, ['owner', 'collaborator', 'organization_member'], 'affiliation')
        self.__raise_param_error(type, ['all', 'owner', 'public', 'private', 'member'], 'type')
        self.__raise_param_error(sort, ['created', 'updated', 'pushed', 'full_name'], 'sort')
        if direction is None:
            if sort == 'full_name':
                direction = 'asc'
            else:
                direction = 'desc'
        else:
            self.__raise_param_error(direction, ['asc', 'desc'], 'direction')

        method = 'GET'
        endpoint = 'user/repos'
        params = self.reqp.get(method, endpoint)
        params['headers']['Accept'] = 'application/vnd.github.drax-preview+json'
        params['params'] = {}
        if not(None is visibility):
            params['params']["visibility"] = visibility
        if not(None is affiliation):
            params['params']["affiliation"] = affiliation
        if not(None is type):
            params['params']["type"] = type
        if not(None is sort):
            params['params']["sort"] = sort
        if not(None is direction):
            params['params']["direction"] = direction
        if not(None is per_page):
            params['params']["per_page"] = per_page
        print(params)

        repos = []
        url = urllib.parse.urljoin("https://api.github.com", endpoint)
        while (None is not url):
            print(url)
            params = self.reqp.update_otp(params)
            print(params)
            r = requests.get(url, headers=params['headers'], params=json.dumps(params['params']))
            repos += self.response.Get(r)
            url = self.response.Headers.Link.Next(r)
        return repos

    def __raise_param_error(self, target, check_list, target_name):
        if not(target is None) and not(target in check_list):
            raise Exception("Parameter Error: [{0}] should be one of the following values. : {1}".format(target_name, check_list))

    """
    公開リポジトリの一覧を取得する。
    @param [int] since is repository id on github.
    """
    def list_public_repos(self, since, per_page=30):
        method = 'GET'
        endpoint = 'repositories'
        params = self.reqp.get(method, endpoint)
        params['params'] = json.dumps({"since": since, "per_page": per_page})
        print(params)
        r = requests.get(urllib.parse.urljoin("https://api.github.com", endpoint), headers=params['headers'])
        return self.response.Get(r)

    """
    リポジトリを削除する。
    引数を指定しなければ、デフォルトユーザのカレントディレクトリ名リポジトリを対象とする。
    """
    def delete(self, username=None, repo_name=None):
        if None is username:
#            username = self.data.get_username()
            username = self.user.Name
        if None is repo_name:
            repo_name = self.repo.Name
#            repo_name = self.data.get_repo_name()
        endpoint = 'repos/:owner/:repo'
        params = self.reqp.get('DELETE', endpoint)
        endpoint = endpoint.replace(':owner', username)
        endpoint = endpoint.replace(':repo', repo_name)
        r = requests.delete(urllib.parse.urljoin("https://api.github.com", endpoint), headers=params['headers'])
        return self.response.Get(r)

    """
    リポジトリを編集する。
    リポジトリ名、説明文、homepageを変更する。
    指定せずNoneのままなら変更しない。
    """
    def edit(self, name=None, description=None, homepage=None):
        if None is name:
#            name = self.data.get_repo_name()
            name = self.user.Name
        if None is description:
#            description = self.data.get_repo_description()
            description = self.repo.Description
        if None is homepage:
#            homepage = self.data.get_repo_homepage()
            homepage = self.repo.Homepage

        endpoint = 'repos/:owner/:repo'
        
        
        #params = self.reqp.get('PATCH', endpoint)
        params = {}
        params['headers'] = self.reqp.get_default(scopes=['repo'])
        
#        endpoint = endpoint.replace(':owner', self.data.get_username())
#        endpoint = endpoint.replace(':repo', self.data.get_repo_name())
        endpoint = endpoint.replace(':owner', self.user.Name)
        endpoint = endpoint.replace(':repo', self.repo.Name)
        params['data'] = {}
        params['data']['name'] = name
        if not(None is description or '' == description):
            params['data']['description'] = description
        if not(None is homepage or '' == homepage):
            params['data']['homepage'] = homepage
        url = urllib.parse.urljoin("https://api.github.com", endpoint)
        print(url)
        print(params['headers'])
        print(json.dumps(params['data']))
        r = requests.patch(url, headers=params['headers'], data=json.dumps(params['data']))
        return self.response.Get(r)
        
    """
    リポジトリのプログラミング言語とそのファイルサイズを取得する。
    @param  {string} usernameはユーザ名
    @param  {string} repo_nameは対象リポジトリ名
    @return {dict}   結果(JSON形式)
    """
    def list_languages(self, username=None, repo_name=None):
        if None is username:
#            username = self.data.get_username()
            username = self.user.Name
        if None is repo_name:
#            repo_name = self.data.get_repo_name()
            repo_name = self.repo.Name

        endpoint = 'repos/:owner/:repo/languages'
        params = self.reqp.get('GET', endpoint)
        endpoint = endpoint.replace(':owner', username)
        endpoint = endpoint.replace(':repo', repo_name)
        r = requests.get(urllib.parse.urljoin("https://api.github.com", endpoint), headers=params['headers'])
        print(endpoint)
        return self.response.Get(r)

