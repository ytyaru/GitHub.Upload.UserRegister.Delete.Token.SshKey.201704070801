#!python3
#encoding:utf-8
import json
import time
from urllib.parse import urlparse
import re
from PIL import Image
from io import BytesIO
class Response(object):
    def __init__(self):
        self.Headers = Response.Headers()
    def Get(self, r, sleep_time=2, is_show=True):
        if is_show:
            print('Response.start---------------------')
            print("HTTP Status Code: {0} {1}".format(r.status_code, r.reason))
            print(r.text)
            print('Response.end---------------------')
        time.sleep(sleep_time)
        r.raise_for_status()
        
        self.Headers.ContentType.Split(r)
        if None is self.Headers.ContentType.mime_type:
            return None
        elif 'application/json' == self.Headers.ContentType.mime_type:
            return r.json()
        elif ('image/gif' == self.Headers.ContentType.mime_type or
            'image/jpeg' == self.Headers.ContentType.mime_type or
            'image/png' == self.Headers.ContentType.mime_type
        ):
            return Image.open(BytesIO(r.content))
#        elif r.request.stream:
#            return r.raw
        else:
            return r.text
            
    class Headers:
        def __init__(self):
            self.ContentType = Response.Headers.ContentType()
            self.Link = Response.Headers.Link()

        class Link:
            def __init__(self):
                pass        
            def Get(self, r, rel='next'):
                if None is r.links:
                    return None
                if 'next' == rel or 'prev' == rel or 'first' == rel or 'last' == rel:
                    return r.links[rel]['url']
            def Next(self, r):
                return self.__get_page(r, 'next')
            def Prev(self, r):
                return self.__get_page(r, 'prev')
            def First(self, r):
                return self.__get_page(r, 'first')
            def Last(self, r):
                return self.__get_page(r, 'last')
            def __get_page(self, r, rel='next'):
                if None is r:
                    return None
                print(r.links)
                if rel in r.links.keys():
                    url = urlparse(r.links[rel]['url'])
                    print('page=' + url.query['page'])
                    return url.query['page']
                else:
                    return None

        class ContentType:
            def __init__(self):
                self.__re_charset = re.compile(r'charset=', re.IGNORECASE)
                self.mime_type = None # 例: application/json
                self.char_set = None # 例: utf8
                # トップレベルタイプ名/サブタイプ名 [;パラメータ]
                # トップレベルタイプ名/[ツリー.]サブタイプ名[+サフィックス] [;パラメータ1] [;パラメータ2] ...
                self.top_level_type = None
                self.sub_type = None
                self.suffix = None
                self.parameters = None

            def Split(self, r):
                self.mime_type = None
                self.char_set = None
                self.top_level_type = None
                self.sub_type = None
                self.suffix = None
                self.parameters = None
                if not('Content-Type' in r.headers) or (None is r.headers['Content-Type']) or ('' == r.headers['Content-Type']):
                    pass
                else:
                    content_types = r.headers['Content-Type'].split(';')
                    self.mime_type = content_types[0]
                    if 1 < len(content_types):
                        parameters = content_types[1:]
                        self.parameters = {}
                        for p in parameters:
                            key, value = p.split('=')
                            self.parameters.update({key.strip(): value.strip()})
                    if None is not self.mime_type:
                        self.mime_type = self.mime_type.strip()
                        self.top_level_type, self.sub_type = self.mime_type.split('/')
                        if self.sub_type.endswith('+'):
                            self.suffix = self.sub_type.split('+')[1]
                    if None is not self.parameters:
                        # 'charset='に一致するならcharsetに設定する
                        for key in self.parameters.keys():
                            if 'charset' == key.lower():
                                self.char_set = self.parameters[key]
#                        if self.__re_charset.match(self.parameters):
#                            self.char_set = re.sub(self.__re_charset, '', self.parameters).strip()
                print('mime_type: {0}'.format(self.mime_type))
                print('top_level_type: {0}'.format(self.top_level_type))
                print('sub_type: {0}'.format(self.sub_type))
                print('suffix: {0}'.format(self.suffix))
                print('parameters: {0}'.format(self.parameters))
                print('char_set: {0}'.format(self.char_set))

