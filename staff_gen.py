# generates the staff's badges

from badgeGen3 import badgeGen

inputCSV = "Staff.csv"

print "Starting..."
badges = badgeGen("badgesStaff.pdf","PI")
badges.setIndivLoc("badgesStaff")
badges.fromCSV(inputCSV,[0,1],[2],6)
badges.save()
print "Done."
