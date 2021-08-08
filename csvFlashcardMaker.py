import csv, helper
from flashcardMaker import QrCodeMaker
from flashcardBookCreator import FlashcardBookCreator

class CsvFlashcardMaker(QrCodeMaker):
    def createFlashcards(self, filename : str):
        images = []
        flashcardCreator = FlashcardBookCreator()
    
        with open("data/{0}.csv".format(filename), newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            rows = list(reader)
            totalrows = len(rows)
            helper.printProgressBar(0, totalrows, prefix = 'Images:', suffix = 'Complete', length = 50)
            for i, row in enumerate(rows):
                helper.printProgressBar(i + 1, totalrows, prefix = 'Images:', suffix = 'Complete', length = 50)
                images.append(self._createQRFlashcard(filename, row["Vocab"], row["Meaning"], row["Reading"]))
            
            flashcardCreator.createPages(images)