# Generates the student's badges

from badgeGen3 import badgeGen

inputCSV = "Students.csv"

print "Starting..."
badges = badgeGen("badgesStudents.pdf","ST")
badges.setIndivLoc("badgesStudents")
badges.fromCSV(inputCSV, [2,3], [4], 6, "Team ", [0])
badges.save()
print "Done."
