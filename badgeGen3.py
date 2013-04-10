# Class is a convenience class that makes it easier to create badges with the
# barcode on them.

# A class written to make barcode generation easier
from pirn_code import PIRNCode

# Report Lab API: http://www.reportlab.com/apis/reportlab/2.4/index.html
# Ubuntu install directory: /usr/share/pyshared/reportlab
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

#_badgeHeight = 3.1
#_badgeWidth = 4.1
#_initXpos = 0.15
#_initYpos = 1
    
class BadgeGen:
    __version__ = 3
    #x = _initXpos
    #y = _initYpos
    #_pdf_canvas = None
    #_default_badge_type = None
    #_print_individual = False
    #_print_individual_location = ""

    _badges = {"PI":os.path.join("BadgeTemplates","StaffBadge.png"),
               "staff":os.path.join("BadgeTemplates","StaffBadge.png"),
               "MT":os.path.join("BadgeTemplates","MentorBadge.png"),
               "mentor":os.path.join("BadgeTemplates","MentorBadge.png"),
               "ST":os.path.join("BadgeTemplates","StudentBadge.png"),
               "student":os.path.join("BadgeTemplates","StudentBadge.png"),
               "TE":os.path.join("BadgeTemplates","TeacherBadge.png"),
               "teacher":os.path.join("BadgeTemplates","TeacherBadge.png"),
               "VT":os.path.join("BadgeTemplates","VolunteerBadge.png"),
               "volunteer":os.path.join("BadgeTemplates","VolunteerBadge.png"),
               "ref":os.path.join("BadgeTemplates","RefBadge.png"),
               "judge":os.path.join("BadgeTemplates","JudgeBadge.png"),
               "guest":os.path.join("BadgeTemplates","GuestBadge.png"),
               "captain":os.path.join("BadgeTemplates","CaptainBadge.png"),
               "coach":os.path.join("BadgeTemplates","CoachBadge.png"),
               "driver":os.path.join("BadgeTemplates","DriverBadge.png")}


    def __init__(self, file_out_name, badge_type, badge_height = 3, 
            badge_width = 4, init_x_position = 0.18, init_y_position = 1):
        #Imports custom fonts
        _ttfFile = os.path.join(os.getcwd(), 'clan-mediumsc-webfont.ttf')
        pdfmetrics.registerFont(TTFont("clan", _ttfFile))

        self._pdf_canvas = canvas.Canvas(file_out_name)
        self._pdf_canvas.setPageSize((8.5*inch, 11*inch))
        self._default_badge_type = badge_type
        self._print_individual = False
        self.__badge_height = badge_height
        self.__badge_width = badge_width
        self.__init_x_position = init_x_position
        self.__init_y_position = init_y_position
        self.x = init_x_position
        self.y = init_y_position

    # currently, loc can only be a folder, not a hierarchy
    def setIndivLoc(self, loc):
        self._print_individual = True
        self._print_individual_location = loc
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

    def addBadge(self, name, line2, code, badge_type = None):
        if not badge_type:
            if not self._default_badge_type:
                # need to throw an exception here
                print "Bad badge type."
                exit(1)
            else:
                badge_type = self._default_badge_type
        self.makeBadge(
            name,
            line2,
            code,
            self.x, self.y,
            badge_type)
        if self._print_individual:
            if not name.strip():
                filename = code + ".pdf"
            else:
                filename = name + ".pdf"
            copyLoc = os.path.join(self._print_individual_location, filename)
            individualBadge = canvas.Canvas(copyLoc)
            self.makeBadge(name,
                           line2,
                           code,
                           2.2, 4,
                           badge_type,
                           new_canvas=individualBadge)
            individualBadge.save()
        # Adding 0.05 so there is some separation between badges
        self.x = self.x + self.__badge_width + 0.02
        if self.x > 8:
            self.x = self.__init_x_position
            self.y = self.y + self.__badge_height + 0.02
            if self.y > 8:
                # Create blank page to trick the printers
                self._pdf_canvas.showPage()
                self._pdf_canvas.showPage()
                self.y = self.__init_y_position

    # nameList, line2List are lists of indices that need to be combined.
    def fromCSV(self, csvFileName, nameIndexes, line2_indexes, codeLoc,
                line2_extra = "", organizeBy = None):
        csvDat = csv.reader(open(csvFileName))
        originalIndivLoc = self._print_individual_location
        for row in csvDat:
            #try:
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
            #except:
                # need to raise exception...
                #print "Bad row: " + str(row) + "\tContinuing..."

    def save(self):
        self._pdf_canvas.save()

    def makeBadge(self, name, Line2, code, x, y, badge_type, new_canvas=None):
        pdf_canvas = new_canvas or self._pdf_canvas
        pdf_canvas.translate(0,0)
        pdf_canvas.drawImage(self._badges[badge_type],
                             x*inch,
                             y*inch,
                             width = self.__badge_width*inch,
                             height = self.__badge_height*inch)
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
            code = PIRNCode(code, code_height= 0.5*inch)
            renderPDF.draw(code, pdf_canvas, (x + 0.76)*inch, (y + 0.6)*inch)

    # Custom function designed for the clan-mediumsc-webfont. This takes the
    # text to be output and attempts to scale the font size so that the width
    # of the string when it appears on the badge will not exceed the sides of
    # the badge. Weights were calculated with a 12 pt font size.
    def findFont(self,string):
        baseWidth = re.compile("[bdeghnpstzCEFLPSZ234567890]") # 0.10 inches
        thinWidth = re.compile("[Ii.:,;]") # 0.03 inches
        bigWidth = re.compile("[wW]") # 0.18 inches
        medbigWidth = re.compile("[myABGMVY]") # 0.14 inches
        medWidth = re.compile("[akoqruvxDHKNOQRTUX]") # 0.12 inches
        smallWidth = re.compile("[cfjlJ1-]") # 0.08 inches

        width2font = (36-16)/(0.29 - 0.14)
        goalWidth = self.__badge_width - 0.5 # 0.5 is combined left+right margin
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
            # Need to change this to raise an exception for error handling
            print "Really long string. Bad input."
            print "Error string: %s" % string
            exit(1) # That's pretty long...
        if width < goalWidth:
            return (goalWidth/width)*12

    def gen4():
        chars = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F',
                'G','H','J','K','L','M','N','P','Q','R','S','T','U','V','W','X','Y',
                'Z']
        return "".join([random.choice(chars) for i in xrange(4)])
