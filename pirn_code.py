# Report Lab API: http://www.reportlab.com/apis/reportlab/2.4/index.html
from reportlab.lib.units import inch
from reportlab.graphics.barcode import createBarcodeDrawing
from reportlab.graphics.shapes import Drawing
from reportlab.graphics.charts.barcharts import HorizontalBarChart
import random

class PIRNCode(Drawing):
    def __init__(self,
                 code,
                 code_height = 0.4*inch,
                 code_width = 188,
                 *args,
                 **kw):
        barcode = createBarcodeDrawing('Code128',
                                        value = code,
                                        humanReadable = True,
                                        barHeight = 0.2*inch,
                                        textHeight = 10,
                                        width = code_width,
                                        height = code_height)
        Drawing.__init__(self, barcode.width, barcode.height, *args, **kw)
        self.add(barcode, name = code)

def gen4():
    chars = ['0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F','G','H','J','K','L','M',
             'N','P','Q','R','S','T','U','V','W','X','Y','Z']
    return "".join([random.choice(chars) for i in xrange(4)])
