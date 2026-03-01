import sys
import os
import glob
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch

doc = SimpleDocTemplate(r"C:\Users\user\Desktop\AI Joi\projects\The_AI_Publisher\master_interior.pdf", pagesize=(6*inch, 9*inch),
                        rightMargin=0.5*inch, leftMargin=0.75*inch, # Gutter
                        topMargin=0.5*inch, bottomMargin=0.5*inch)

styles = getSampleStyleSheet()
normal_style = styles["Normal"]
title_style = styles["Heading1"]

Story = []

# Title Page
Story.append(Spacer(1, 2*inch))
Story.append(Paragraph("<font size=24><b>The_AI_Publisher</b></font>", title_style))
Story.append(PageBreak())

# Read Chapters
chapter_files = sorted(glob.glob(r"C:\Users\user\Desktop\AI Joi\projects\The_AI_Publisher\manuscript\chapters\chapter_*.md"))
for f in chapter_files:
    with open(f, 'r', encoding='utf-8') as file:
        text = file.read()
        Story.append(Paragraph(os.path.basename(f).replace(".md", "").capitalize(), title_style))
        Story.append(Spacer(1, 0.2*inch))
        # Simple paragraph splitting
        for p in text.split("\n\n"):
            if p.strip():
                Story.append(Paragraph(p.strip().replace("\n", "<br/>"), normal_style))
                Story.append(Spacer(1, 0.1*inch))
        Story.append(PageBreak())

doc.build(Story)
print("Interior PDF generated successfully.")
