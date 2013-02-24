#! /usr/bin/python

# ReportLab API: http://www.reportlab.com/apis/reportlab/2.4/index.html
from reportlab.lib.units import inch
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics import renderPDF
from reportlab.pdfgen import canvas

from pirn_code import PIRNCode

#PIRN_PREFIX = 'TL'
PIRN_PREFIX = 'KE'

FILE_NAME = 'ke_barcodes'

def intToString(i):
    ops = ['0','1','2','3','4','5','6','7','8','9',
           'A','B','C','D','E','F','G','H','I','J',
           'K','L','M','N','P','Q','R','S','T', # Note: removed letter O
           'U','V','W','X','Y','Z']
    if i < 35:
        return ops[i]
    else:
        return intToString(i // 35) + ops[i % 35]

def padString(s, length=6):
    return '0' * (length - len(s)) + s

def increment(s):
    pass

def main():
    c = canvas.Canvas(FILE_NAME + '.pdf')
    c.setPageSize((8.5*inch, 11*inch))
    c.setFont("Courier", 12)

    x = 0.17
    y = 0.75

    start = 0
    end = 33 * 5
    for i in range(start, end):
        code = PIRNCode(PIRN_PREFIX + padString(intToString(i)), code_height=0.6*inch)
        renderPDF.draw(code, c, x*inch, y*inch)
        x = x + 2.775
        if x > 7:
            x = 0.17
            y = y + 0.9
            if y > 10:
                c.showPage()
                c.setFont('Courier', 12)
                y = 0.75
    c.save()

if __name__ == '__main__':
    main()
