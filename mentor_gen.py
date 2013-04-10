#! /usr/bin/python2.7
# Generates the mentor's badges

from badgeGen3 import BadgeGen

inputCSV = "mentors.csv"

print "Starting..."
badges = BadgeGen("badgesMentors.pdf","MT")
badges.setIndivLoc("badgesMentors")
badges.fromCSV(inputCSV,[0,1],[2],3)
badges.save()
print "Done."
