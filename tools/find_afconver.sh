find . -name '*Track.aiff' -type f -exec afconvert '{}' -o '{}'.m4a -q 127 -b 256000 -f m4af -d aac \;
