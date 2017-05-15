import cPickle as pkl
dicts = pkl.load(open('translated_dict.pkl', 'rb'))

print dicts[12054]
print len(dicts)