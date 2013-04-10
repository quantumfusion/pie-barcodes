#! /usr/bin/python2.7
# Generates the student's badges

from badgeGen3 import BadgeGen

inputCSV = "students.csv"

print "Starting..."
badges = BadgeGen("badgesStudents.pdf","ST")
badges.setIndivLoc("badgesStudents")
badges.fromCSV(inputCSV, [2,3], [1], 15, "Team ", [0])
badges.save()
print "Done."
