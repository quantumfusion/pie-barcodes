# A convenience class for generating barcodes. Inherits from drawing,
# so can be drawn directly onto a canvas.

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
                                        barHeight = 0.3*inch,
                                        #textHeight = 10,
                                        width = code_width,
                                        height = code_height)
        Drawing.__init__(self, barcode.width, barcode.height, *args, **kw)
        self.add(barcode, name = code)
