# Generates the mentor's badges

from badgeGen3 import badgeGen

inputCSV = "Mentors.csv"

print "Starting..."
badges = badgeGen("badgesMentors.pdf","MT")
badges.setIndivLoc("badgesMentors")
badges.fromCSV(inputCSV,[0,1],None,3)
badges.save()
print "Done."
