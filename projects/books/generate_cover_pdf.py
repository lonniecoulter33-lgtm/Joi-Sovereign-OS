from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

# Exact coordinates extracted from IngramSpark template: 9798295548253.pdf
# Page canvas: 15.0" x 12.0" (1080 x 864 pts)
# Artwork is NOT centered — it's positioned per IngramSpark's layout.

PAGE_WIDTH = 15.0 * inch
PAGE_HEIGHT = 12.0 * inch

# Template zone positions (in points, from PDF content stream)
BACK_X = 179.66       # 2.4953"
BACK_Y = 198.0        # 2.7500"
BACK_W = 441.099      # 6.1264"
BACK_H = 666.0        # 9.2500"

SPINE_X = 620.646     # 8.6201"
SPINE_Y = 197.972     # 2.7496"
SPINE_W = 18.368      # 0.2551"
SPINE_H = 666.028     # 9.2504"

FRONT_X = 638.986     # 8.8748"
FRONT_Y = 198.0       # 2.7500"
FRONT_W = 440.986     # 6.1248"
FRONT_H = 666.0       # 9.2500"


def generate_ingram_pdf():
    c = canvas.Canvas(
        "9798295548253_Print_Ready.pdf",
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
    )

    c.drawImage("back.png",  BACK_X,  BACK_Y,  width=BACK_W,  height=BACK_H)
    c.drawImage("spine.png", SPINE_X, SPINE_Y, width=SPINE_W, height=SPINE_H)
    c.drawImage("front.jpg", FRONT_X, FRONT_Y, width=FRONT_W, height=FRONT_H)

    c.showPage()
    c.save()

    print("PDF Created: 9798295548253_Print_Ready.pdf")
    print(f"  Page:  {PAGE_WIDTH/72:.3f} x {PAGE_HEIGHT/72:.3f} inches")
    print(f"  Back:  ({BACK_X/72:.4f}, {BACK_Y/72:.4f})  {BACK_W/72:.4f} x {BACK_H/72:.4f} in")
    print(f"  Spine: ({SPINE_X/72:.4f}, {SPINE_Y/72:.4f})  {SPINE_W/72:.4f} x {SPINE_H/72:.4f} in")
    print(f"  Front: ({FRONT_X/72:.4f}, {FRONT_Y/72:.4f})  {FRONT_W/72:.4f} x {FRONT_H/72:.4f} in")


if __name__ == "__main__":
    generate_ingram_pdf()
