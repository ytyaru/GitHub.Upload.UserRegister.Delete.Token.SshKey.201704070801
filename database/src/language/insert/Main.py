import database.src.language.insert.LanguageSource
import database.src.language.insert.Inserter
class Main(object):
    def __init__(self, data, client):
        self.data = data
        self.client = client
        self.source = database.src.language.insert.LanguageSource.LanguageSource()
        self.inserter = database.src.language.insert.Inserter.Inserter(self.data)
    def Run(self):
        self.inserter.Insert(self.source.Get())


if __name__ == "__main__":    
    m = Main()
    m.Run()

