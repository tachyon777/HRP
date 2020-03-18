"""
ver4.21がベース
オッズ帯ごとの的中率、回収率を算出する。
df対応
"""
#######setup#########
show_ozzper_rank =3#1=1位

#don't change:
lst = [i for i in range(6) if i != show_ozzper_rank-1]
#####################
import sys
import csv
import pprint
import pandas as pd
import numpy as np
import warnings
warnings.simplefilter('ignore')

file_name = sys.argv[1]
df = pd.read_csv(file_name,encoding="shift-jis",dtype={'レースID(新)':str})

answer = df["着差"].values.tolist()
raceid = df["レースID(新)"].values.tolist()
hukusita = df["複勝オッズ下限"].values.tolist()
hukuue = df["複勝オッズ上限"].values.tolist()
haitou = df["複勝配当"].values.tolist()
tanhaitou = df["単勝オッズ"].values.tolist()
aianswer = df["ya"].values.tolist()
hoursenum = len(df)

#raceidの下二桁処理
for i in range(0,hoursenum-1):
    try:
        raceid[i] = raceid[i][:-2]
    except:
        print(raceid[i])

firsth = 0
lasth = 1 #ここに出走＋１が組み込まれている
theaianswer = []
idpost = 0
syussou = 1
racetime = 0
arihit,nasihit,arisyuusi,nasisyuusi = 0,0,0,0
arihit2,arihit3,buy01,buy02,buy03,arisyuusi2,arisyuusi3 = 0,0,0,0,0,0,0
hukulist2 = []
hukulist3 = []
umaban,umaban2,umaban3,umaban4,umaban5,umaban6 = 0,0,0,0,0,0
kaihi = 0
tansyuusi2nd,tantekityu2nd,tansyuusi2nd2,tantekityu2nd2,tan2ndbuytime = 0,0,0,0,0
tanlist2nd= []
tanlist3rd= []
tanlist4th= []
tanlist5th= []
tanhaitou2nd = []
tanhaitou2nd2 = []
tansyuusi,tansyuusi2 = 0,0
tantekityu,tantekityu2 = 0,0
tan2buytime = 0
widebuy,allwidebuy = 0,0
uma2hit,uma3hit = 0,0
renjiku,renhimo = 0,0
idpost = raceid[0]
wide = []
allwide = []
umaren = []
tanlist = []
hukulist = []
a00,a01,a02 = 0,0,0
a10,a11,a12 = 0,0,0
a20,a21,a22 = 0,0,0
a30,a31,a32 = 0,0,0
a40,a41,a42 = 0,0,0
a50,a51,a52 = 0,0,0
b0,b1,b2,b3,b4,b5,b6,b7,b8 = 0,0,0,0,0,0,0,0,0
c0,c1,c2,c3,c4,c5,c6,c7,c8 = 0,0,0,0,0,0,0,0,0
d0,d1,d2,d3,d4,d5,d6,d7,d8 = 0,0,0,0,0,0,0,0,0
b30,c30,d30 = 0,0,0
b41,b42,b43,b44,b45,b46 = 0,0,0,0,0,0
c41,c42,c43,c44,c45,c46 = 0,0,0,0,0,0
d41,d42,d43,d44,d45,d46 = 0,0,0,0,0,0
ozz = []
haitoua = 0
for i in range(0,hoursenum-2):
    if idpost == raceid[i+1] and i != hoursenum -3 :
        syussou +=1
        idpost = raceid[i+1]
    else: #ここでストップがかかるとレースの処理が始まる
        if i == hoursenum -3:
            syussou += 1
        racetime += 1
        lasth = firsth + syussou #lasthは、出走馬＋１が既に組み込まれている
        for j in range(firsth,lasth):
            theaianswer.append(aianswer[j])
        #19/06/05追記。y'負の値の不具合調整(theaianswer内の型をstr→floatに変換)
        theaianswer = [float(s) for s in theaianswer]
        theaianswer.sort()
        #評価値の高い馬と馬番を一致させる
        for j in range (firsth,lasth):
            try:
                if theaianswer[show_ozzper_rank-1] == float(aianswer[j]):
                    umaban = j #但し、馬番ー１である。
                elif theaianswer[lst[0]] == float(aianswer[j]):
                    umaban2 = j
                elif theaianswer[lst[1]] == float(aianswer[j]):
                    umaban3 = j
                elif theaianswer[lst[2]] == float(aianswer[j]):
                    umaban4 = j
                elif theaianswer[lst[3]] == float(aianswer[j]):
                    umaban5 = j
                elif theaianswer[lst[4]] == float(aianswer[j]):
                    umaban6 = j
            except:
                print(j)
        if haitou[umaban2] != "0":
                uma2hit+=1
        if haitou[umaban3] != "0":
                uma3hit+=1
        #[10-7-4]21等を全評価順で算出させる
        ozz.append(tanhaitou[umaban])
        if aianswer[umaban] == aianswer[firsth]:
            a00 += 1
            renjiku += 1
        elif aianswer[umaban] == aianswer[firsth+1]:
            a01 += 1
            renjiku += 1
        elif aianswer[umaban] == aianswer[firsth+2]:
            a02 += 1
        if aianswer[umaban2] == aianswer[firsth]:
            a10 += 1
            renjiku += 1
        elif aianswer[umaban2] == aianswer[firsth+1]:
            a11 += 1
            renjiku += 1
        elif aianswer[umaban2] == aianswer[firsth+2]:
            a12 += 1
        if aianswer[umaban3] == aianswer[firsth]:
            a20 += 1
            renhimo += 1
        elif aianswer[umaban3] == aianswer[firsth+1]:
            a21 += 1
            renhimo += 1
        elif aianswer[umaban3] == aianswer[firsth+2]:
            a22 += 1
        if aianswer[umaban4] == aianswer[firsth]:
            a30 += 1
            renhimo += 1
        elif aianswer[umaban4] == aianswer[firsth+1]:
            a31 += 1
            renhimo += 1
        elif aianswer[umaban4] == aianswer[firsth+2]:
            a32 += 1
        if aianswer[umaban5] == aianswer[firsth]:
            a40 += 1
        elif aianswer[umaban5] == aianswer[firsth+1]:
            a41 += 1
        elif aianswer[umaban5] == aianswer[firsth+2]:
            a42 += 1
        if aianswer[umaban6] == aianswer[firsth]:
            a50 += 1
        elif aianswer[umaban6] == aianswer[firsth+1]:
            a51 += 1
        elif aianswer[umaban6] == aianswer[firsth+2]:
            a52 += 1
        if umaban == firsth: #単勝が当たった場合
            tansyuusi += float(tanhaitou[umaban])
            tantekityu += 1
            tanlist.append(tanhaitou[umaban])
        idpost = raceid[i+1]
        firsth = lasth
        syussou = 1
        renjiku = 0
        renhimo = 0
        theaianswer = []

    #オッズ帯ごとの回収率を算出
for j in range(0,len(ozz)):
        haitoua = ozz[j]
        haitoua = float(haitoua)
        if haitoua < 2.0:
            b0 += 1
        elif 2.0 <= haitoua < 3.0:
            b1 += 1
        elif 3.0 <= haitoua < 4.0:
            b2 += 1
        elif 4.0 <= haitoua < 5.0:
            b3 += 1
        elif 5.0 <= haitoua < 6.0:
            b30 += 1
        elif 6.0 <= haitoua < 7:
            b4 += 1
        elif 7 <= haitoua < 8:
            b41 += 1
        elif 8 <= haitoua < 9:
            b42 += 1
        elif haitoua < 10:
            b43 += 1
        elif haitoua < 13:
            b44 += 1
        elif haitoua < 15:
            b45 += 1
        elif haitoua < 18:
            b46 += 1
        elif haitoua < 20:
            b5 += 1
        elif 20 <= haitoua < 30:
            b6 += 1
        elif 30 <= haitoua < 40:
            b7 += 1
        elif 40 <= haitoua:
            b8 += 1
for j in tanlist:
    j = float(j)
    if j <= 2.0:
        c0 += 1
        d0 += j
    elif 2.0 <= j < 3.0:
        c1 += 1
        d1 += j
    elif 3.0 <= j < 4.0:
        c2 += 1
        d2 += j
    elif 4.0 <= j < 5.0:
        c3 += 1
        d3 += j
    elif 5.0 <= j < 6.0:
        c30 += 1
        d30 += j
    elif 6.0 <= j < 7:
        c4 += 1
        d4 += j
    elif j < 8:
        c41 += 1
        d41 += j
    elif j < 9:
        c42 += 1
        d42 += j    
    elif j < 10:
        c43 += 1
        d43 += j
    elif j < 13:
        c44 += 1
        d44 += j
    elif j < 15:
        c45 += 1
        d45 += j
    elif j < 18:
        c46 += 1
        d46 += j
    elif j < 20:
        c5 += 1
        d5 += j
    elif 20 <= j < 30:
        c6 += 1
        d6 += j
    elif 30 <= j < 40:
        c7 += 1
        d7 += j
    elif 40 <= j:
        c8 += 1
        d8 += j

print("オッズ帯ごと的中・回収率----------------------------------------------")
print("集計対象：評価値",show_ozzper_rank,"位")
print(" ")
if b0 == 0:
    print("1.0~1.9 : 該当なし")
else:
    print("1.0~1.9 : " + "{:.1f}".format(c0/b0*100) + "%, " + "{:.1f}".format(d0/b0*100) + "%, " + "(" + str(c0) + " / " + str(b0) + "R)")
if b1 == 0:
    print("2.0~2.9 : 該当なし")
else:
    print("2.0~2.9 : " + "{:.1f}".format(c1/b1*100) + "%, " + "{:.1f}".format(d1/b1*100) + "%, " + "(" + str(c1) + " / "+ str(b1) + "R)")
if b2 == 0:
    print("3.0~3.9 : 該当なし")
else:
    print("3.0~3.9 : " + "{:.1f}".format(c2/b2*100) + "%, " + "{:.1f}".format(d2/b2*100) + "%, " + "(" + str(c2) + " / "+ str(b2) + "R)")
if b3 == 0:
    print("4.0~5.9 : 該当なし")
else:
    print("4.0~4.9 : " + "{:.1f}".format(c3/b3*100) + "%, " + "{:.1f}".format(d3/b3*100) + "%, " + "(" + str(c3) + " / "+ str(b3) + "R)")
if b30 == 0:
    print("5.0~5.9 : 該当なし")
else:
    print("5.0~5.9 : " + "{:.1f}".format(c30/b30*100) + "%, " + "{:.1f}".format(d30/b30*100) + "%, " + "(" + str(c30) + " / "+ str(b30) + "R)")
if b4 == 0:
    print("6.0~6.9 : 該当なし")
else:
    print("6.0~6.9 : " + "{:.1f}".format(c4/b4*100) + "%, " + "{:.1f}".format(d4/b4*100) + "%, " + "(" + str(c4) + " / "+ str(b4) + "R)")
if b41 == 0:
    print("7.0~7.9 : 該当なし")
else:
    print("7.0~7.9 : " + "{:.1f}".format(c41/b41*100) + "%, " + "{:.1f}".format(d41/b41*100) + "%, " + "(" + str(c41) + " / "+ str(b41) + "R)")
if b42 == 0:
    print("8.0~8.9 : 該当なし")
else:
    print("8.0~8.9 : " + "{:.1f}".format(c42/b42*100) + "%, " + "{:.1f}".format(d42/b42*100) + "%, " + "(" + str(c42) + " / "+ str(b42) + "R)")
if b43 == 0:
    print("9.0~9.9 : 該当なし")
else:
    print("9.0~9.9 : " + "{:.1f}".format(c43/b43*100) + "%, " + "{:.1f}".format(d43/b43*100) + "%, " + "(" + str(c43) + " / "+ str(b43) + "R)")
if b44 == 0:
    print("10.0~12.9 : 該当なし")
else:
    print("10.0~12.9 : " + "{:.1f}".format(c44/b44*100) + "%, " + "{:.1f}".format(d44/b44*100) + "%, " + "(" + str(c44) + " / "+ str(b44) + "R)")
if b45 == 0:
    print("13.0~14.9 : 該当なし")
else:
    print("13.0~14.9 : " + "{:.1f}".format(c45/b45*100) + "%, " + "{:.1f}".format(d45/b45*100) + "%, " + "(" + str(c45) + " / "+ str(b45) + "R)")
if b46 == 0:
    print("15.0~17.9 : 該当なし")
else:
    print("15.0~17.9 : " + "{:.1f}".format(c46/b46*100) + "%, " + "{:.1f}".format(d46/b46*100) + "%, " + "(" + str(c46) + " / "+ str(b46) + "R)")

if b5 == 0:
    print("18.0~19.9 : 該当なし")
else:
    print("18~19.9 : " + "{:.1f}".format(c5/b5*100) + "%, " + "{:.1f}".format(d5/b5*100) + "%, " + "(" + str(c5) + " / "+ str(b5) + "R)")
if b6 == 0:
    print("20~29.9 : 該当なし")
else:
    print("20~29.9 : " + "{:.1f}".format(c6/b6*100) + "%, " + "{:.1f}".format(d6/b6*100) + "%, " + "(" + str(c6) + " / "+ str(b6) + "R)")
if b7 == 0:
    print("20~39.9 : 該当なし")
else:
    print("20~39.9 : " + "{:.1f}".format(c7/b7*100) + "%, " + "{:.1f}".format(d7/b7*100) + "%, " + "(" + str(c7) + " / "+ str(b7) + "R)")
if b8 == 0:
    print("40~     : 該当なし")
else:
    print("40~     : " + "{:.1f}".format(c8/b8*100) + "%, " + "{:.1f}".format(d8/b8*100) + "%, " + "(" + str(c8) + " / "+ str(b8) + "R)")
#print(" ")
#print("試行レース数:"+str(racetime))
#print("評価値1位: ["+str(a00)+"-"+str(a01)+"-"+str(a02)+"] "+str(a00+a01+a02))
#print("評価値2位: ["+str(a10)+"-"+str(a11)+"-"+str(a12)+"] "+str(a10+a11+a12))
#print("評価値3位: ["+str(a20)+"-"+str(a21)+"-"+str(a22)+"] "+str(a20+a21+a22))
#print("評価値4位: ["+str(a30)+"-"+str(a31)+"-"+str(a32)+"] "+str(a30+a31+a32))
#print("評価値5位: ["+str(a40)+"-"+str(a41)+"-"+str(a42)+"] "+str(a40+a41+a42))
#print("評価値6位: ["+str(a50)+"-"+str(a51)+"-"+str(a52)+"] "+str(a50+a51+a52))
#print("1~3位PHR: "+"{:.2f}".format((a00+a01+a02+a10+a11+a12+a20+a21+a22)/racetime))
#print("1~6位PHR: "+"{:.2f}".format((a00+a01+a02+a10+a11+a12+a20+a21+a22+a30+a31+a32+a40+a41+a42+a50+a51+a52)/racetime))