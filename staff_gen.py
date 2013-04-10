#! /usr/bin/python2.7
# generates the staff's badges

from badgeGen3 import BadgeGen

inputCSV = "staffRoster.csv"

print "Starting..."
badges = BadgeGen("badgesStaff.pdf","PI")
badges.setIndivLoc("badgesStaff")
badges.fromCSV(inputCSV,[0,1],[2],15)
badges.save()
print "Done."
