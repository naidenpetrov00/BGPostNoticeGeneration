from io import BytesIO
from typing import Any
from pandas import Series
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from readData import caseNumberProp


def drawString(packet: BytesIO, row: Series):
    c = canvas.Canvas(packet, pagesize=A4)
    c.drawString(100, 100, str(row[caseNumberProp]))

    c.save()
    packet.seek(0)


def draw_grid(filename="grid_test.pdf"):
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    for x in range(0, int(width), 50):
        c.setFont("Helvetica", 6)
        c.drawString(x + 2, height - 10, str(x))
        c.line(x, 0, x, height)

    for y in range(0, int(height), 50):
        c.setFont("Helvetica", 6)
        c.drawString(2, y + 2, str(y))
        c.line(0, y, width, y)

    c.save()

draw_grid()