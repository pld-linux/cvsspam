#!/bin/sh
svn="http://svn.badgers-in-foil.co.uk/cvsspam"
tag=RELEASE-0_2_12

svn diff --old=$svn/tags/$tag --new=$svn/trunk | filterdiff -x project.xml > cvsspam-branch.diff

branch=svn_support
svn diff --old=$svn/trunk --new=$svn/branches/$branch | filterdiff -i svn_post_commit_hook.rb -i cvsspam.rb > cvsspam-svnspam-branch.diff
