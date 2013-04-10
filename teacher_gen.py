#! /usr/bin/python2.7
# generates the teacher's badges

from badgeGen3 import BadgeGen

inputCSV = "teachers.csv"

print "Starting..."
badges = BadgeGen("badgesTeachers.pdf", "TE")
badges.setIndivLoc("badgesTeachers")
badges.fromCSV(inputCSV,[3,4],[1],7,"Team ", [0])
badges.save()
print "Done."
