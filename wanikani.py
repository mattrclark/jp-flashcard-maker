import requests, details

class Wanikani:
    def __init__(self):
        self.__apiToken = details.API_TOKEN

    def __createRequest(self, endPoint):
        return requests.get("https://api.wanikani.com/v2/{0}".format(endPoint), headers={
            "Authorization": "Bearer {0}".format(self.__apiToken)})

    def getVocabForLevel(self, level):
        return self.__createRequest("subjects?levels={0}&types=vocabulary".format(level))

    