import urllib2

fn = 'lecture'
for i in range(24):
    i = str(i + 1)
    filename = fn + i
    url = 'https://courses.csail.mit.edu/6.006/fall11/lectures/lecture' + i + '.pdf'
    lec = urllib2.urlopen(url)
    with open(filename + '.pdf', 'wb') as output:
        output.write(lec.read())

fn = 'MIT6_006F11_lec'
for i in range(24):
    i = '{:02d}'.format(i + 1)
    filename = fn + i
    url = 'https://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-006-introduction-to-algorithms-fall-2011/lecture-videos/MIT6_006F11_lec'\
        + i + '.pdf'
    lec = urllib2.urlopen(url)
    with open(filename + '.pdf', 'wb') as output:
        output.write(lec.read())
