'''
    imgify.py
    born 2020-03-18
    n-ivan
    v1.1
    converts ascii art text to a .png
'''

from PIL import Image, ImageFont, ImageDraw

## filename DOES NOT include extension
def read_text(fileName: str):
    fle = open(fileName+".txt", 'r')
    contents = fle.read()
    fle.close()
    return contents

def get_dims(text):
    cols = 0
    rows = 0
    for ch in text:
        if rows == 0:
            cols += 1
        if ch == '\n':
            rows += 1
    return (cols - 1, rows)

def make_ascii_png(text,fileName):
    width, height = get_dims(text)
    print(width)
    print(height)
    img = Image.new('RGBA', (6* width, 13 * height), (255, 255, 255))
    fnt = ImageFont.truetype('cn.ttf')
    d = ImageDraw.Draw(img)
    d.text((0,0), text, font=fnt, fill=(0, 0, 0))
    img.save(f'{fileName}.png')

def main():
    print("Enter the name of the file...")
    fileName = input()
    text = read_text(fileName)
    print(f"Converting {fileName}...")
    make_ascii_png(text, fileName)
    print(f"Done converting {fileName}!")

if __name__ == '__main__':
    main()
