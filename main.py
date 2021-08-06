import qrcode, json, helper, csv
from PIL import Image, ImageDraw, ImageFont
from wanikani import Wanikani

JISHO_WORD = "https://www.jisho.org/word/{0}"
IMG_WIDTH = 1000
IMG_HEIGHT = 600
LEVEL = 8

def createQRCode(level, jp, eng, reading):
    # Make QR Code
    qrImg = qrcode.make(JISHO_WORD.format(jp))
    qrImg_w, qrImg_h = qrImg.size

    # Create new image and paste QR code onto it
    img = Image.new('RGBA', (IMG_WIDTH, IMG_HEIGHT), (255, 255, 255, 255))
    img_w, img_h = img.size
    offset = ((img_w - qrImg_w) // 2, (img_h - qrImg_h))
    img.paste(qrImg, offset)

    # Draw the vocabulary onto the image
    draw = ImageDraw.Draw(img)
    font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 130)
    draw_w, draw_h = draw.textsize(jp, font=font)
    draw.text((IMG_WIDTH / 2 - draw_w / 2, 10), jp, fill=(255,0,0), font=font)

    # Draw the reading onto the image
    if(reading != ""):
        pr = "({0})".format(reading)
        font = ImageFont.truetype("/Library/Fonts/Arial Unicode.ttf", 50)
        draw_w, draw_h = draw.textsize(pr, font=font)
        draw.text((IMG_WIDTH / 2 - draw_w / 2, 150), pr, fill=(255,0,0), font=font)

    # Save the file
    img.save('output/{0}/{0}-{1}-{2}.png'.format(level, eng, jp))


def loadFromWaniKani():
    # Setup WaniKani request and send for specified level
    wk = Wanikani()
    r = wk.getVocabForLevel(LEVEL)

    # Load response into json
    response = json.loads(r.content.decode('utf-8'))

    print("Total subjects: {0}".format(response["total_count"]))

    # Go through each vocab and create a QR code flashcard
    helper.printProgressBar(0, response["total_count"], prefix = 'Progress:', suffix = 'Complete', length = 50)
    for i in range(0, response["total_count"]):
        d = response["data"][i]["data"]
        helper.printProgressBar(i + 1, response["total_count"], prefix = 'Progress:', suffix = 'Complete', length = 50)
        createQRCode(LEVEL, d["characters"], d["meanings"][0]["meaning"], d["readings"][0]["reading"])

def loadFromCsv(filename):
    with open("data/{0}.csv".format(filename), newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        rows = list(reader)
        totalrows = len(rows)
        helper.printProgressBar(0, totalrows, prefix = 'Progress:', suffix = 'Complete', length = 50)
        for i, row in enumerate(rows):
            helper.printProgressBar(i + 1, totalrows, prefix = 'Progress:', suffix = 'Complete', length = 50)
            createQRCode(filename, row["Vocab"], row["Meaning"], row["Reading"])

if __name__ == "__main__":
    loadFromCsv("household")