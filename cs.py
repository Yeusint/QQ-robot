def TimeDate(times: int):
    h = 0 #hour
    m = 0 #minute
    while times >= 60:
        times-=60
        m+=1
        if m == 60:
            m-=60
            h+=1
    if h == 0 and m == 0:
        return "%d秒" %times
    elif times == 0:
        if h == 0 and m != 0:
            return "%d分" % m
        elif h != 0 and m == 0:
            return "%d时" % h
        elif h != 0 and m != 0:
            return "%d时%d分" % (h, m)
    else:
        if h == 0 and m != 0:
            return "%d分%d秒" % (m, times)
        elif h != 0 and m == 0:
            return "%d时%d秒" % (h, times)
        elif h != 0 and m != 0:
            return "%d时%d分%d秒" % (h, m, times)
print(TimeDate(int(input())))
