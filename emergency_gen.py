#! /usr/bin/python2.7
# generates the staff's badges

from badgeGen3 import BadgeGen

inputCSV = "emergency_run.csv"

print "Starting..."
badges = BadgeGen("badgesMisc.pdf","PI")
badges.setIndivLoc("badgesMisc")
badges.fromCSV(inputCSV,[0,1],[2],3)
badges.save()
print "Done."
