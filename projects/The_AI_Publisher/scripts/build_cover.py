import sys
import os
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from PIL import Image

# Specs
total_width = 12.75 * inch
total_height = 9.25 * inch
spine_width = 0.5 * inch
trim_width = 6.0 * inch
bleed = 0.125 * inch

c = canvas.Canvas(r"C:\Users\user\Desktop\AI Joi\projects\The_AI_Publisher\master_cover.pdf", pagesize=(total_width, total_height))

# Setup PDF/X-1a
c.setCreator("Joi Master Publisher")
c.setTitle("The_AI_Publisher Cover")

# Front Cover Image (Right side)
front_x = (trim_width + spine_width + bleed) * inch
front_y = 0

front_img_path = r"C:\Users\user\Desktop\AI Joi\projects\The_AI_Publisher\assets\images\cover.png"
if os.path.exists(front_img_path):
    img = Image.open(front_img_path)
    if img.mode != 'CMYK':
        img = img.convert('CMYK')
        img.save(r"C:\Users\user\Desktop\AI Joi\projects\The_AI_Publisher\assets\images\cover_cmyk.jpg", "JPEG", quality=95)
        front_img_path = r"C:\Users\user\Desktop\AI Joi\projects\The_AI_Publisher\assets\images\cover_cmyk.jpg"
    c.drawImage(front_img_path, front_x, front_y, width=(trim_width + bleed)*inch, height=total_height)
else:
    c.drawString(front_x + 1*inch, 4*inch, "[Front Cover Image Missing]")

# Spine (Center)
spine_x = (trim_width + bleed) * inch
c.saveState()
c.translate(spine_x + (spine_width/2.0), total_height/2.0)
c.rotate(-90)
c.setFont("Helvetica-Bold", 14)
c.drawCentredString(0, 0, "The_AI_Publisher".upper())
c.restoreState()

# Back Cover (Left side)
back_x = 0
back_y = 0

# Draw White Barcode Box (Bottom Left of Back Cover)
barcode_x = back_x + 0.5*inch + bleed
barcode_y = back_y + 0.5*inch + bleed
c.setFillColorRGB(1,1,1)
c.rect(barcode_x, barcode_y, 1.75*inch, 1*inch, fill=1, stroke=0)

c.save()
print("Cover PDF generated successfully.")
