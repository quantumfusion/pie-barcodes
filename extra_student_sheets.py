# Generate a new sheet of barcodes for all schools.

from PIRNCode import gen4
from badgeGen3 import badgeGen
import os, csv

csvFile = "Teachers.csv"
fileOutName = "_Extras.pdf"
binderName = "ExtraStudentBadges.pdf"

print "Starting..."
schools = csv.reader(open(csvFile,"rb"))
binder = badgeGen(binderName, "ST")
for row in schools:
    if not row[0].strip() or not row[6][:2] == "TE":
        continue
    school = row[0]
    abbrev = row[1]
    teamNum = row[4]
    fileOut = badgeGen(os.path.join("badgesStudents",school,fileOutName), "ST")
    for i in range(6):
        code = "ST12" + abbrev + "%02d" % int(teamNum) + gen4()
        fileOut.addBadge(None, "Team " + teamNum, code)
        binder.addBadge(None, "Team " + teamNum, code)
    fileOut.save()
binder.save()
del csvFile
print "Done."
