import os, helper
from PIL import Image
from datetime import datetime

class FlashcardBookCreator:
    def __init__(self):
        self.WIDTH = 2480
        self.HEIGHT = 3508
        self.currentX = 0
        self.currentY = 0
        self.pageIndex = 0
        self.padding = 0

    def createPages(self, images):
        directory = "output/flashcard-books/book-{0}".format(datetime.now().strftime("%d-%m-%Y-%H-%M-%S"))
        os.makedirs(directory)

        # Create a page
        page = self.__createPage()

        # Loop through all images
        helper.printProgressBar(0, len(images), prefix = 'Pages:', suffix = 'Complete - {0} Pages Created'.format(self.pageIndex), length = 50)
        for i in range(0, len(images)):
            img = images[i]
            helper.printProgressBar(i + 1, len(images), prefix = 'Pages:', suffix = 'Complete - {0} Pages Created'.format(self.pageIndex), length = 50)

            img_w, img_h = img.size

            # Check if image is out of bounds
            # If so, then correct (Create page or move down)
            if(self.currentY + img_h + self.padding >= self.HEIGHT):
                page.save("{1}/page-{0}.png".format(self.pageIndex, directory))
                page = self.__createPage()
            elif(self.currentX + img_w + self.padding >= self.WIDTH):
                self.currentX = 0
                self.currentY += img_h + self.padding
                if(self.currentY + img_h + self.padding >= self.HEIGHT):
                    page.save("{1}/page-{0}.png".format(self.pageIndex, directory))
                    page = self.__createPage()
            
            # Paste images onto page
            page.paste(img, (self.currentX, self.currentY))

            # Move along to the next position
            self.currentX += img_w + self.padding

        # Save the page
        page.save("{1}/page-{0}.png".format(self.pageIndex, directory))

    def __createPage(self):
        self.currentX = 0
        self.currentY = 0
        self.pageIndex += 1
        return Image.new('RGBA', (self.WIDTH, self.HEIGHT), (255, 255, 255, 255))