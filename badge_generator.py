# TODO: Add ability to pass a specially formatted csv and have it detect
# the type of badge, output individual badges, combine to single doc for
# printing, and output a csv for easily updating the online database.

from PIRNCode import PIRNCode

# Report Lab API: http://www.reportlab.com/apis/reportlab/2.4/index.html
from reportlab.lib.units import inch
from reportlab.lib.utils import ImageReader
from reportlab.graphics import renderPDF
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas

# For adding custom fonts
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# For generating pdfs
from reportlab.pdfgen.canvas import Canvas
import ImageFont, ImageDraw, Image
import csv, re, os

# Generating random identifier
import random, string

#Imports custom fonts
_ttfFile = os.path.join(os.getcwd(), 'clan-mediumsc-webfont.ttf')
pdfmetrics.registerFont(TTFont("clan", _ttfFile))

_badgeHeight = 3.1
_badgeWidth = 4.1
_initXpos = 0.15
_initYpos = 1
    
_badges = {"PI":os.path.join("Badge Templates","Staff Badge.png"),
           "staff":os.path.join("Badge Templates","Staff Badge.png"),
           "MT":os.path.join("Badge Templates","Mentor Badge.png"),
           "mentor":os.path.join("Badge Templates","Mentor Badge.png"),
           "ST":os.path.join("Badge Templates","Student Badge.png"),
           "student":os.path.join("Badge Templates","Student Badge.png"),
           "TE":os.path.join("Badge Templates","Teacher Badge.png"),
           "teacher":os.path.join("Badge Templates","Teacher Badge.png"),
           "VT":os.path.join("Badge Templates","Volunteer Badge.png"),
           "volunteer":os.path.join("Badge Templates","Volunteer Badge.png"),
           "ref":os.path.join("Badge Templates","Ref Badge.png"),
           "judge":os.path.join("Badge Templates","Judge Badge.png"),
           "guest":os.path.join("Badge Templates","Guest Badge.png"),
           "captain":os.path.join("Badge Templates","Captain Badge.png"),
           "coach":os.path.join("Badge Templates","Coach Badge.png"),
           "driver":os.path.join("Badge Templates","Driver Badge.png")}

class badgeGen:
    __version__ = 3

    x = _initXpos
    y = _initYpos
    #_pdfCanvas = None
    #_defaultBadgeType = None
    #_printIndividual = False
    #_printIndivLoc = ""

    def __init__(self, fileOutName, badgeType):
        self._pdfCanvas = canvas.Canvas(fileOutName)
        self._pdfCanvas.setPageSize((8.5*inch, 11*inch))
        self._defaultBadgeType = badgeType
        self._printIndividual = False

    # currently, loc can only be a folder, not a hierarchy
    def setIndivLoc(self, loc):
        self._printIndividual = True
        self._printIndivLoc = loc
        folders = self.parsePath(loc)
        if len(folders) == 1:
            if not loc in os.listdir("."):
                os.mkdir(loc)
                return
            
        for folder in folders:
            if not folder in os.listdir("."):
                os.mkdir(folder)
            os.chdir(folder)
        for folder in folders: # Return to working directory
            os.chdir("..")

    def parsePath(self,path):
        pair = os.path.split(path)
        pathList = []
        while pair[1]:
            pathList.append(pair[1])
            pair = os.path.split(pair[0])
        pathList.reverse()
        return pathList
                

    def addBadge(self, name, line2, code, badgeType = None):
        if not badgeType:
            if not self._defaultBadgeType:
                print "Bad badge type."
                exit(1)
            else:
                badgeType = self._defaultBadgeType
        self.makeBadge(self._pdfCanvas,
                       name,
                       line2,
                       code,
                       self.x, self.y,
                       badgeType)
        if self._printIndividual:
            if not name.strip():
                filename = code + ".pdf"
            else:
                filename = name + ".pdf"
            copyLoc = os.path.join(self._printIndivLoc, filename)
            individualBadge = canvas.Canvas(copyLoc)
            self.makeBadge(individualBadge,
                           name,
                           line2,
                           code,
                           2.2, 4,
                           badgeType)
            individualBadge.save()
        self.x = self.x + _badgeWidth
        if self.x > 8:
            self.x = _initXpos
            self.y = self.y + _badgeHeight
            if self.y > 8:
                self._pdfCanvas.showPage()
                self.y = _initYpos

    # nameList, line2List are lists of indices that need to be combined.
    def fromCSV(self, csvFileName, nameIndexes, line2_indexes, codeLoc,
                line2_extra = "", organizeBy = None):
        csvDat = csv.reader(open(csvFileName))
        originalIndivLoc = self._printIndivLoc
        for row in csvDat:
            try:
                if "Example" in row or "Oski" in row or "Barcode" in row:
                    continue
                name = ""
                for index in nameIndexes:
                    name = name + row[index] + " "
                name = name[:-1]

                line2 = line2_extra
                if line2_indexes:
                    for index in line2_indexes:
                        line2 = line2 + row[index] + " "
                    line2 = line2[:-1]

                if organizeBy:
                    path = ""
                    missing = False
                    for index in organizeBy:
                        element = row[index]
                        if not element:
                            missing = True
                            break
                        path = os.path.join(path,row[index])
                    if not missing:
                        self.setIndivLoc(os.path.join(originalIndivLoc, path))
                self.addBadge(name, line2, row[codeLoc])
            except:
                print "Bad row: " + str(row) + "\tContinuing..."

    def save(self):
        self._pdfCanvas.save()

    def makeBadge(self,pdf_canvas, name, Line2, code, x, y, badgeType):
        pdf_canvas.translate(0,0)
        pdf_canvas.drawImage(_badges[badgeType],
                             x*inch,
                             y*inch,
                             width = _badgeWidth*inch,
                             height = _badgeHeight*inch)
        if name:
            fontSize = self.findFont(name)
            if fontSize > 40:
                fontSize = 40
            pdf_canvas.setFont("clan", fontSize)
            pdf_canvas.drawCentredString((x + 2.03)*inch, (y + 1.9)*inch, name)
        if Line2:
            fontSize = self.findFont(Line2)
            if fontSize > 26:
                fontSize = 26
            pdf_canvas.setFont("clan",fontSize)
            pdf_canvas.drawCentredString((x + 2.03)*inch, (y + 1.3)*inch, Line2)
        if code:
            code = PIRNCode(code)
            renderPDF.draw(code, pdf_canvas, (x + 0.73)*inch, (y + 0.6)*inch)

    def findFont(self,string):
        baseWidth = re.compile("[abdeghnpstuzCFLPSZ234567890]") # 0.10 inches at 12 pt font
        thinWidth = re.compile("[Ii.:,;]") # 0.03 inches at 12 pt font
        bigWidth = re.compile("[wW]") # 0.18 inches at 12 pt font
        medbigWidth = re.compile("[ABMV]") # 0.14 inches at 12 pt font
        medWidth = re.compile("[kmoqrvxyDGHKNOQRTUXY]") # 0.12 inches at 12 pt font
        smallWidth = re.compile("[cfjlEJ1-]") # 0.08 inches at 12 pt font

        width2font = (36-16)/(0.29 - 0.14)
        goalWidth = _badgeWidth - 0.5
        width = 0

        for ch in string:
            if baseWidth.match(ch):
                width = width + 0.1
            elif thinWidth.match(ch):
                width = width + 0.03
            elif bigWidth.match(ch):
                width = width + 0.18
            elif medbigWidth.match(ch):
                width = width + 0.14
            elif medWidth.match(ch):
                width = width + 0.12
            else: # Assume small width
                width = width + 0.08

        if width > goalWidth:
            print "Really long string. Bad input."
            exit(1) # That's pretty long...
        if width < goalWidth:
            return (goalWidth/width)*12

deprecated = """    
def strLen(string):
    count = 0
    half = re.compile("[\WIi]")
    big = re.compile("[WwMm]")
    for ch in string:
        if half.match(ch):
            count = count + 0.8
        elif big.match(ch):
            count = count + 1.55
        else:
            count = count + 1
    return int(round(count))
"""
