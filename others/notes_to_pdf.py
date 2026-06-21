import os
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import letter
pdfmetrics.registerFont(TTFont("Arial", "arial.ttf"))
styles = getSampleStyleSheet()
styles["Normal"].fontName = "Arial"
scrip_dir = os.path.dirname(__file__)
notes_path = os.path.join(scrip_dir, "notes.txt")
with open(notes_path, "r", encoding="utf-8") as file:
    text = file.read()
    lines = text.split("\n")
story = []
for line in lines:
    if line == "":
        story.append(Spacer(1, 10))
    else:
        p = Paragraph(line, styles["Normal"])
        story.append(p)
pdf_path = os.path.join(scrip_dir, "notes_backup.pdf")
doc = SimpleDocTemplate(pdf_path, pagesize=letter)
doc.build(story)