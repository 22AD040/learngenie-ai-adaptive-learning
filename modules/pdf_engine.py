from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import uuid

def create_pdf(text):

    filename = f"study_material_{uuid.uuid4().hex}.pdf"

    c = canvas.Canvas(filename, pagesize=letter)

    width,height = letter

    y = height - 50

    for line in text.split("\n"):

        c.drawString(50,y,line)

        y -= 20

        if y < 50:
            c.showPage()
            y = height - 50

    c.save()

    return filename