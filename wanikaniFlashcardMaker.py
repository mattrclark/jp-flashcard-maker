import json, helper
from flashcardMaker import QrCodeMaker
from wanikani import Wanikani
from flashcardBookCreator import FlashcardBookCreator

class WaniKaniFlashcardMaker(QrCodeMaker):
    def __init__(self):
        self.wk = Wanikani()

    def createFlashcardsForLevel(self, level : int):
        images = []
        flashcardCreator = FlashcardBookCreator()

        r = self.wk.getVocabForLevel(level)

        # Load response into json
        response = json.loads(r.content.decode('utf-8'))

        helper.printProgressBar(0, response["total_count"], prefix = 'Images:', suffix = 'Complete', length = 50)
        for i in range(0, response["total_count"]):
            d = response["data"][i]["data"]
            helper.printProgressBar(i + 1, response["total_count"], prefix = 'Images:', suffix = 'Complete', length = 50)
            images.append(self._createQRFlashcard(level, d["characters"], d["meanings"][0]["meaning"], d["readings"][0]["reading"]))

        flashcardCreator.createPages(images)