import os
os.chdir('/Users/z/Downloads')
f = open(f'Untitled.tex')
ll = []
for i in f:
    if i[0] != '%':
        ll.append(i)
f.close()


f = open(f'u2.tex', 'w')
for L in ll:
    f.write(L)
f.close()
