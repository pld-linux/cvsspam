#!/bin/sh
svn="http://svn.badgers-in-foil.co.uk/cvsspam"
tag=RELEASE-0_2_12

svn diff --old=$svn/tags/$tag --new=$svn/trunk | filterdiff -x project.xml > cvsspam-branch.diff
sed -i -e 's,\$''Revision\$,$''Revision: 1.12 $,' cvsspam-branch.diff
