#!python3
#encoding:utf-8
import dataset
from bs4 import BeautifulSoup
import time
import os.path
import requests

class GnuSite(object):
    def __init__(self, path_gnu_licenses_sqlite3):
        self.db_license = dataset.connect('sqlite:///' + path_gnu_licenses_sqlite3)

    def GetAll(self):
        for lang in self.__GetAllLanguages():
            self.processing_language_code = lang
            soup = BeautifulSoup(self.__GetHtmlString(lang), 'html.parser')
            for div in soup.select('div.big-section'):
                typeName = self.__GetSection(div)
                print(typeName)

    def __GetAllLanguages(self):
        langs = []
        soup = BeautifulSoup(self.__GetHtmlString('en'), 'html.parser')
        for span in soup.find('div', id='translations').find('p').find_all('span'):
            langs.append(span.find('a').get('lang'))
            print(span.find('a').get('lang'))
        return langs

    def __GetHtmlString(self, lang):
        url = 'https://www.gnu.org/licenses/license-list.{0}.html'.format(lang)
        path_this_dir = os.path.abspath(os.path.dirname(__file__))
        file_name = os.path.basename(url)
        file_path = os.path.join(path_this_dir, file_name)
        if os.path.isfile(file_path):
            print('ファイル読み込み-----------------------')
            with open(file_path, 'rb') as f:
                html_str = f.read()
        else:
            print('HTTPリクエスト-----------------------')
            time.sleep(2)
            r = requests.get(url)
            html_str = r.content
            with open(file_path, 'wb') as f:
                f.write(html_str)
        return html_str

    def __GetSection(self, div):
        h3Id = div.find('h3').get('id')
        print('{0},{1}'.format(h3Id, div.find('h3').string.strip()))
        if 'SoftwareLicenses' == h3Id:
            for sub in div.find_all_next('div', class_='big-subsection'):
                h4Id = sub.find('h4').get('id')
                if 'GPLCompatibleLicenses' == h4Id:
                    self.__GetDl(sub, 'software')
                elif 'GPLIncompatibleLicenses' == h4Id:
                    self.__GetDl(sub, 'software')
                elif 'NonFreeSoftwareLicenses' == h4Id:
                    self.__GetDl(sub, 'software')
                else:
                    break
        elif 'DocumentationLicenses' == h3Id:
            for sub in div.find_all_next('div', class_='big-subsection'):
                h4Id = sub.find('h4').get('id')
                if 'FreeDocumentationLicenses' == h4Id:
                    self.__GetDl(sub, 'document')
                elif 'NonFreeDocumentationLicenses' == h4Id:
                    self.__GetDl(sub, 'document')
                else:
                    break
        elif 'OtherLicenses' == h3Id:
            for sub in div.find_all_next('div', class_='big-subsection'):
                h4Id = sub.find('span').find('a').get('href')
                if None is not sub.find('h4').string:
                    print('{0},{1}'.format(h4Id, sub.find('h4').string.strip()))
                else:
                    print('{0},{1}'.format(h4Id, sub.find('h4').string))
                if '#OtherLicenses' == h4Id:
                    print(h4Id + '---------------')
                    dl = self.__GetDl(sub, 'other')
                    dl = self.__GetDl(dl, 'other')
                    dl = self.__GetDl(dl, 'other')
                    dl = self.__GetDl(dl, 'other')
                elif '#Fonts' == h4Id:
                    print(h4Id + '---------------')
                    dl = self.__GetDl(sub, 'other.font')
                    dl = self.__GetDl(dl, 'other.font')
                elif '#OpinionLicenses' == h4Id:
                    print(h4Id + '---------------')
                    self.__GetDl(sub, 'other.opinion')
                elif '#Designs' == h4Id:
                    print(h4Id + '---------------')
                    self.__GetDl(sub, 'other.design')
            
    def __GetDl(self, div, targetValue):
        dl = div.find_next('dl')
        if None is dl:
            return
        print("dtの数={0}".format(len(dl.find_all('dt'))))
        print("ddの数={0}".format(len(dl.find_all('dd'))))
        for dt in dl.find_all('dt'):
            for a in dt.find_all('a'):
                if None is not a.string:
                    name = a.string.strip().replace('\n', '')
                    try:
                        if 'en' == self.processing_language_code:
                            self.db_license['Licenses'].insert(self.__CreateLicense(dl, dt, targetValue))
                        license = self.db_license['Licenses'].find_one(HeaderId=self.__GetHeaderId(dt))
                        if None is self.db_license['Multilingual'].find_one(LicenseId=license['Id'], LanguageCode=self.processing_language_code):
                            self.db_license['Multilingual'].insert(self.__CreateMultilingual(dt, name, self.db_license['Licenses'].find_one(HeaderId=self.__GetHeaderId(dt))['Id']))
                    except Exception as e:
                        print('%r' % e)
        return dl
    
    def __CreateLicense(self, dl, dt, targetValue):
        print(self.__GetHeaderId(dt))
        record = dict(
            HeaderId=self.__GetHeaderId(dt),
            ColorId=self.db_license['Colors'].find_one(Key=dl.get('class'))['Id'],
            Target=targetValue,
            Url=dt.find('a').get('href')
        )
        print(record)
        return record

    def __CreateMultilingual(self, dt, name, license_id):
        record = dict(
            LicenseId=license_id,
            LanguageCode=self.processing_language_code,
            Name=name,
            Description=dt.find_next('dd').decode_contents(formatter="html").strip(),
        )
        print(record)
        return record

    def __GetHeaderId(self, dt):
        headerId = ''
        if None is dt.find('span'):
            return None
        for a in dt.find('span').find_all('a'):
            headerId += a.string + ','
        return headerId[:-1]


if __name__ == '__main__':
    gnu = GnuSite(
        path_gnu_licenses_sqlite3 = './GNU.Licenses.sqlite3'
    )
    gnu.GetAll()

