a = 'index,len'
a_index_len = a.index(',')
a_last_len = len(a)
i = 0
a_index = ''
a_last = ''
while i < a_index_len:
    a_index = a_index + a[i]
    i += 1
print(a_index)
i = a.index(',') + 1
while i < a_last_len:
    a_last = a_last + a[i]
    i += 1
print(a_last)
