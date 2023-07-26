import sys

#
# De module head is een imitatie van de unix head.
#
#
# Bijv:
#
# sxs) d:\sxs>py src\head.py 5 dat\out\sample-cy.xml
# <?xml
#
# (sxs) d:\sxs>py src\head.py 15 dat\out\sample-cy.xml
# <?xml version="
#
# (sxs) d:\sxs>py src\head.py 150 dat\out\sample-cy.xml
# <?xml version="1.0" encoding="UTF-8"?>
# <Extract xmlns="http://www.nbb.be/cba/2021-06/extract">
# ____<Header>
# ________<DeclarerId>
# ____________<Declarer
#
#
chunk = int(sys.argv[1])
ifile = sys.argv[2]
f = open(ifile, encoding='utf-8')
data_read = f.read(chunk)
print(data_read)
f.close()
