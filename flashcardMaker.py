import qrcode
from PIL import Image, ImageDraw, ImageFont

JISHO_WORD = "https://www.jisho.org/word/{0}"
IMG_WIDTH = 826
IMG_HEIGHT = 438

class FlashcardMaker:
    def __init__(self):
        self.saveFlashcardToDisk = True

    def _drawText(self, draw, text : str, fontSize : int, posX : int, posY : int, pivot : int, color) -> None:
        font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", fontSize)
        draw_w, draw_h = draw.textsize(text, font=font)
        offset = ImagePivot.getOffset(pivot, draw_w)
        draw.text((posX + offset, posY), text, fill= color, font=font)

    def _drawBorder(self, draw):
        draw.rectangle(((0, 0), (IMG_WIDTH - 1, IMG_HEIGHT - 1)), outline = "black")

class QrCodeMaker(FlashcardMaker):
    def __createQRCode(self, jp):
        qrImg = qrcode.make(JISHO_WORD.format(jp))
        qrImg = qrImg.resize((IMG_HEIGHT // 2, IMG_HEIGHT // 2), Image.NEAREST)
        return qrImg
    
    
    def _createQRFlashcard(self, level, jp, eng, reading):
        qrImg = self.__createQRCode(jp)
        qrImg_w, qrImg_h = qrImg.size

        # Create new image and paste QR code onto it
        img = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT), (255, 255, 255, 255))
        img_w, img_h = img.size
        offset = ((img_w - qrImg_w) // 2, (img_h - qrImg_h))
        img.paste(qrImg, offset)

        # Draw the vocabulary onto the image
        draw = ImageDraw.Draw(img)
        self._drawText(draw, jp, 100, IMG_WIDTH / 2, 10, ImagePivot.centre, (255, 0, 0))
        self._drawText(draw, eng, 20, IMG_WIDTH / 2 - 5, IMG_HEIGHT - 25, ImagePivot.right, (0, 0, 0))

        # Draw the reading onto the image
        if(reading != ""):
            pr = "({0})".format(reading)
            self._drawText(draw, pr, 30, IMG_WIDTH / 2, 140, ImagePivot.centre, (255, 0, 0))

        self._drawBorder(draw)        

        # Save the file
        if(self.saveFlashcardToDisk):
            img.save('output/{0}/{0}-{1}-{2}.png'.format(level, eng, jp))

        return img

class ImagePivot:

    left = 0
    right = 1
    centre = 2

    # create addNumbers static method
    @staticmethod
    def getOffset(pivot : int, img_w : int) -> int:
        if (pivot == ImagePivot.left):
            return 0
        elif (pivot == ImagePivot.right):
            return - img_w
        
        return - img_w // 2