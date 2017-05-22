#!python3
#encoding:utf-8
import dataset
class Inserter:
    def __init__(self, db_path):
#    def __init__(self, data):
#        self.data = data
        self.db_lang = dataset.connect('sqlite:///' + db_path)

    def Insert(self, y):
        self.db_lang.begin()
        count = 0
        for key in y.keys():
            print(key)
            print(y[key])
            if None is self.db_lang['Languages'].find_one(Key=key):
                self.db_lang['Languages'].insert(self.__CreateLanguages(key, y[key]))
                language_id = self.db_lang['Languages'].find_one(Key=key)['Id']
                self.__InsertAliases(language_id, y[key])
                self.__InsertExtensions(language_id, y[key])
                self.__InsertFileNames(language_id, y[key])
                self.__InsertInterpreters(language_id, y[key])
            else:
                count += 1
                print('重複レコード。')
                print(self.db_lang['Languages'].find_one(Key=key))
        self.db_lang.commit()
        print(count)

    def __CreateLanguages(self,key, y):
        return dict(
            LanguageId=y['language_id'],
            Key=key,
            Type=y['type'],
            Color=y.get('color', None),
            TextMateScope=y.get('tm_scope', 'text'),
            AceMode=y.get('ace_mode', None),
            CodeMirrorMode=y.get('codemirror_mode', None),
            CodeMirrorMimeType=y.get('codemirror_mime_type', None),
            GroupName=y.get('group', None),
            Wrap=y.get('wrap', 0),
            Searchable=y.get('searchable', 1)
        )
    def __InsertAliases(self, language_id, lang):
        if None is lang.get('aliase', None):
            return
        for aliase in lang['aliase']:
            self.db_lang['Aliases'].insert(dict(
                LanguageId=language_id,
                Aliase=aliase
            ))
    def __InsertExtensions(self, language_id, lang):
        if None is lang.get('extensions', None):
            return
        is_first = True
        for extension in lang['extensions']:
            self.db_lang['Extensions'].insert(dict(
                LanguageId=language_id,
                Extension=extension,
                IsPrimary=(1) if (is_first) else (0)
            ))
            is_first = False
    def __InsertFileNames(self, language_id, lang):
        if None is lang.get('filenames', None):
            return
        for filename in lang['filenames']:
            self.db_lang['FileNames'].insert(dict(
                LanguageId=language_id,
                FileName=filename
            ))
    def __InsertInterpreters(self, language_id, lang):
        if None is lang.get('interpreters', None):
            return
        for interpreter in lang['interpreters']:
            self.db_lang['Interpreters'].insert(dict(
                LanguageId=language_id,
                Interpreter=interpreter
            ))

