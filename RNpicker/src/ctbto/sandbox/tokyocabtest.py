'''
Created on Nov 4, 2009

@author: aubert
'''

from tokyocabinet import table

db = table.Table()
db.open('/tmp/test.tct', table.TDBOWRITER | table.TDBOCREAT)
db['knight-a'] = {'name':'The Green Knight','surname':'joe','strength':'mighty'}
db['knight-b'] = {'name':'aKnight','surname':'bill','strength':'pitiful'}
db['knight-c'] = {'name':'Knight','surname':'bab','strength':'pitiful'}

print("len %s : " % len(db))

r = db['knight-c']

q = db.query()
q.addcond('strength', table.TDBQCSTREQ, 'mighty')
print(q.search())
print("%s" % (dir(q) ))
#print q.hint()
db.setindex('strength', table.TDBITLEXICAL)
q = db.query()
q.addcond('strength', table.TDBQCSTREQ, 'pitiful')
q.setorder('name', table.TDBQCSTREQ)
q.setlimit(1,0)
res = q.search()
print(db.out(res[0]))
print("hello")
