#!python3
#encoding:utf-8
import json
import time
from urllib.parse import urlparse
import re
import web.http.Response
class Response(web.http.Response.Response):
    def __init__(self):
        super().__init__()
        self.re_content_type_raw = re.compile('application/vnd.github.*.raw')

    """
    HTTP応答データを返す
    @param {requests.response} 応答データを作成するため。
    @return {?} Content-Typeなどにより任意のデータ型を返す。
    """
    def Get(self, r, sleep_time=2, is_show=True):
        res = super().Get(r, sleep_time, is_show)
        if None is self.Headers.ContentType.mime_type:
            return None
        elif 'json' == self.Headers.ContentType.suffix:
            return r.json()
        elif self.re_content_type_raw.match(self.Headers.ContentType.mime_type):
            return r.content
        else:
            return res

