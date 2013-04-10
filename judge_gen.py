#! /usr/bin/python2.7
# generates the judge's badges

from badgeGen3 import BadgeGen

inputCSV = "judges.csv"

print "Starting..."
badges = BadgeGen("badgesJudges.pdf", "judge")
badges.setIndivLoc("badgesJudges")
badges.fromCSV(inputCSV,[0,1],[2],3)
badges.save()
print "Done."
