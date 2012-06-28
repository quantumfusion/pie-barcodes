# Special script for PiE 2012 Registration Forms Spreadsheet
from PIRNCode import gen4
from badgeGen3 import badgeGen
import os, csv

csvFile = "PiE 2012 Registration Forms Spreadsheet - Student Info.csv"
outDir = "badgesStudentsTest"
assignedCodes = "_assignedCodes.csv"

badges = badgeGen(csvFile[:-4]+".pdf","ST")
csvDat = csv.reader(open(csvFile,"rb"))
newCodes = csv.writer(open(assignedCodes, "wb"))

no = ["n","N","no","No","NO"]
yes = ["y","Y","yes","Yes","YES"]

for row in csvDat:
    try:
        if len(row) > 8 and row[8].strip() in no and not row[0] == "School":
            badges.setIndivLoc(os.path.join(outDir,row[0]))
            code = row[6]
            if not row[6].strip():
                code = "ST12" + row[1] + "%02d" % int(row[2]) + gen4()
                newCodes.writerow([row[3],row[4],code])
            badges.addBadge(" ".join(row[3:5]),"Team " + row[2], code)
    except:
        print "Error: "
        print row

badges.save()
del newCodes
