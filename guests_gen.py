#! /usr/bin/python2.7
# Generates the student's badges

from badgeGen3 import BadgeGen

inputCSV = "guests.csv"

print "Starting..."
badges = BadgeGen("badgesGuests.pdf","guest")
badges.setIndivLoc("badgesGuests")
badges.fromCSV(inputCSV, [0], [1], 2)
badges.save()
print "Done."
