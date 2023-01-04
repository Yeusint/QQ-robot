from fun.music import get_kugou

cookies={
            'dfid': '2C7nx20YQMEs0yz5uR1RaHXI',
            'KuGoo': 'KugooID=875231868&KugooPwd=FCDD11161D9C9444E7AF9192682FB26D&NickName=%u4e00%u4e2a%u0032%u0035%u0030&Pic=http://imge.kugou.com/kugouicon/165/20100101/20100101192931478054.jpg&RegState=1&RegFrom=&t=d471095e761713ffb3eec6c5a6d5e38ecd60c37d67261634efe5af25a01bede2&t_ts=1672710651&t_key=&a_id=1014&ct=1672710651&UserName=%u006b%u0067%u006f%u0070%u0065%u006e%u0038%u0037%u0035%u0032%u0033%u0031%u0038%u0036%u0038',
            'UserName': '%u006b%u0067%u006f%u0070%u0065%u006e%u0038%u0037%u0035%u0032%u0033%u0031%u0038%u0036%u0038',
            't': 'd471095e761713ffb3eec6c5a6d5e38ecd60c37d67261634efe5af25a01bede2',
            'KugooID': '875231868',
            'kg_dfid_collect': 'd41d8cd98f00b204e9800998ecf8427e',
            'kg_mid': '9e2f6588ff79eb10e50a8e27e13d8dc4',
            'mid': '9e2f6588ff79eb10e50a8e27e13d8dc4',
            'kg_dfid': '2C7nx20YQMEs0yz5uR1RaHXI',
            'UM_distinctid': '181e5c6e5bafb-0f2109c82915ac-9136f2c-15f900-181e5c6e5bb248'
        }
print(get_kugou('打上花火', 1, cookies))

