import urllib2
fn = 'lecture'
for i in range(24):
    i = str(i+1)
    filename = fn + i
    url = 'https://courses.csail.mit.edu/6.006/fall11/lectures/lecture' + i + '.pdf'
    lec = urllib2.urlopen(url)
    with open(filename+'.pdf','wb') as output:
        output.write(lec.read())
