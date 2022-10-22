def TimeDate(times: int):
    H = 0  # 96
    M = 0
    i = 0
    for i in range(999999):
        if times < 60:
            break
        else:
            times -= 60
            H+=1
    for i in range(9999999):
        if H<60:
            break
        else:
            M+=1
            H -= 60
    while i == times:
        i += 1

    strs = "%d" %M +"小时" + "%.f"%H+"分钟"+ str(times)+"秒"
    print(strs)
TimeDate(int(input()))