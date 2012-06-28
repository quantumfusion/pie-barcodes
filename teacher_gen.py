# generates the teacher's badges

from badgeGen3 import badgeGen

inputCSV = "Teachers.csv"

print "Starting..."
badges = badgeGen("badgesTeachers.pdf", "TE")
badges.setIndivLoc("badgesTeachers")
badges.fromCSV(inputCSV,[2,3],[4],6,"Team ", [0])
badges.save()
print "Done."
