import pandas as pd
import random
import pyperclip
import re
from collections import Counter

def remov_duplicates(st):

    st = st.split(" ")

    for i in range(0, len(st)):

        st[i] = "".join(st[i])

        dupli = Counter(st)

        s = " ".join(dupli.keys())

    return s.title()

def get_title(kw):
    
    k1=int(len(kw)*1/10)
    k2=int(len(kw)*1/5)
    k3=int(len(kw)*1/3)
    k4=int(len(kw)*3/5)
    z=str(random.sample(['cuffs','cuff','ear'],1)[0])
    a=str(random.sample(kw[0:k1],1)[0])
    b=str(random.sample(kw[k1:k2],1)[0])
    c=str(random.sample(kw[k2:k3],1)[0])
    d=str(random.sample(kw[k3:k4],1)[0])
    e=str(random.sample(kw[k4:],1)[0])
    ti=remov_duplicates(a+'  '+b+' '+z+' '+c+' '+d+' '+e)
    ti=ti.replace('  ',' ')
    print('''
    KW1:{}
    KW2:{}
    KW3:{}
    KW4:{}
    KW5:{}
    TITLE:{}
    '''.format(a,b,c,d,e,ti))
    return pyperclip.copy(ti)
    # a,b,c,d,ti

def get_price(cb,wt,be_rt):
    ff=wt*0.1+20
    pc=float((cb+ff+6)*be_rt/6.6/0.8)
    print('售价${}'.format(pc))
    

while True:
    cat_list=[
        '珠宝耳环',
        '珠宝脚镯脚链',
        '手链手镯',
        '珠宝项链串珠项链'
        ]
    print('''
    1. 珠宝耳环
    2. 珠宝脚镯脚链
    3. 手链手镯
    4. 珠宝项链串珠项链
    ''')
    cat_num=input ('请输入编号:')
    
    dt=pd.read_excel('%s.xls' % cat_list[int(cat_num)-1])
    
    kw=dt['热搜关键词'].tolist()

    get_title(kw)
    ke=int(input('1.继续,2.重新生成'))
    if ke == 1:
        print('''
        1.低价流量产品
        2.普通产品
        3.品牌流量产品
        4.品牌利润产品
        ''')
        benefit_rate=[
            1.3,
            1.5,
            1.8,
            2.2
        ]
        be_le=int(input('请输入产品定位:'))
        be_rt=benefit_rate[be_le]
        cb=float(input('请输入成本￥:'))
        wt=float(input('请输入重量g:'))
        get_price(cb,wt,be_le)
    else:
        continue




