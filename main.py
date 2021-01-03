import numpy as np
import cv2
import math
from PIL import ImageFont, ImageDraw, Image  
import datetime

width = 1366
height = 768
center = (width//2, height//2)
font = cv2.FONT_HERSHEY_SIMPLEX
white = (255, 255, 255)
bg = 0x12
background = (bg, bg, bg)

img = np.full((height, width, 3), bg, dtype=np.uint8)

# add text by pillow

font_bold_name = 'Quicksand-Bold.ttf'
font_regular_name = 'Quicksand-Regular.ttf'

pil_im = Image.fromarray(img)  
draw = ImageDraw.Draw(pil_im)

# init
text_spacing = 10

def draw_text_with_spacing(text, pos, font, spacing = 0):
  next_pos = 0
  for c in text:
    draw.text((pos[0] + next_pos, pos[1]), c, font=font)
    c_size = font.getsize(c)
    next_pos += c_size[0] + spacing
  return (next_pos - spacing if next_pos != 0 else 0, font.getsize(text)[1])

# init slogan text
slogan_spacing = 5
slogan_text = 'Knowledge/Cute/Contribution'
slogan_fsize = 24
slogan_font = ImageFont.truetype(font_regular_name, slogan_fsize) 
slogan_size = slogan_font.getsize(slogan_text)
slogan_size = (slogan_size[0] + slogan_spacing * len(slogan_text), slogan_size[1])

# init year text
year_spacing = 7
year_text = '2021'
year_fsize = int(slogan_fsize * 1.5)
year_font = ImageFont.truetype(font_bold_name, year_fsize) 
year_size = year_font.getsize(year_text)
year_size = (year_size[0] + year_spacing * len(year_text), year_size[1])

# remain days of year
doy = datetime.datetime.now().timetuple().tm_yday
days_pos = (center[0] - slogan_size[0]//2 + year_size[0] + text_spacing, center[1] - text_spacing//2)
days_width = slogan_size[0] - year_size[0] - text_spacing * 2
days_end = (days_pos[0] + days_width, days_pos[1])
days_current = doy/365
days_thick = 2

# time of day
now = datetime.datetime.now()
hour = now.hour
sun = Image.open('sun.png') if hour >= 6 and hour < 18 else Image.open('moon.png')
sun_pos = days_pos
sun_width = days_width - sun.width
sun_end = (days_end[0] - sun.width, days_end[1])
sun_current = (hour-6)%12/12
space_height = 80
pil_im.paste(sun, (sun_pos[0] + int(sun_current * sun_width), sun_pos[1] - sun.width//2 - int(math.sin(math.pi * sun_current) * space_height)), sun.convert('RGBA'))
draw.rectangle([days_pos, (days_end[0], days_end[1] + sun.height)], fill=background)

# draw
draw_text_with_spacing(year_text, (center[0] - slogan_size[0] // 2, center[1] - year_size[1] - text_spacing//2), year_font, year_spacing)
draw_text_with_spacing(slogan_text, (center[0] - slogan_size[0] // 2, center[1] + text_spacing//2), slogan_font, slogan_spacing)

# draw
draw.line([days_pos, days_end], fill=(64, 64, 64))
draw.line((days_pos[0] - days_thick//2, days_pos[1], days_pos[0] + int(days_width  * days_current) - days_thick//2, days_pos[1]), fill=(255, 255, 255), width=days_thick)

# pillow to cv2
img = cv2.cvtColor(np.array(pil_im), cv2.COLOR_RGB2BGR)  

# ft2 = cv2.freetype.createFreeType2()
# print(dir(cv2))

# img = cv2.putText(img, '2021', center, font, 1.1, white, 2, cv2.LINE_AA)

# cv2.imshow("My drawing", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

cv2.imwrite('wallpaper.png', img)