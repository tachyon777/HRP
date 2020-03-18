"""
xgbのプログラムに対して複勝式の結果を出す
1~3位、複勝の上下限を設けてのプログラム
4.11がベースとなっている。
"""
#######setup#########
hukusita_thresh = [
    [0,0], #thresh[i][0] <= x < thresh[i][1]
    [1.5,3],
    [2,6],
    [0,0],
    [0,0],
]
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
aianswer = df["y'"].values.tolist()
hoursenum = len(df)

#raceidの下二桁処理
for i in range(0,hoursenum-1):
    raceid[i] = raceid[i][:-2]

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
tan2buytime = 0
widebuy,allwidebuy = 0,0
uma2hit,uma3hit = 0,0
renjiku,renhimo = 0,0
idpost = raceid[0]
tanlist = []
hukulist = []
a00,a01,a02 = 0,0,0
a10,a11,a12 = 0,0,0
a20,a21,a22 = 0,0,0
a30,a31,a32 = 0,0,0
a40,a41,a42 = 0,0,0
a50,a51,a52 = 0,0,0
b00,b01,b02,b03,b04,b05,b06,b07 = 0,0,0,0,0,0,0,0
hukumujoken1 = []
hukumujoken2 = []
hukumujoken3 = []
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
            if theaianswer[0] == float(aianswer[j]):
                umaban = j #但し、馬番ー１である。
            elif theaianswer[1] == float(aianswer[j]):
                umaban2 = j
            elif theaianswer[2] == float(aianswer[j]):
                umaban3 = j
            elif theaianswer[3] == float(aianswer[j]):
                umaban4 = j
            elif theaianswer[4] == float(aianswer[j]):
                umaban5 = j
            elif theaianswer[5] == float(aianswer[j]):
                umaban6 = j
        if haitou[umaban2] != 0:
                uma2hit+=1
        if haitou[umaban3] != 0:
                uma3hit+=1
        #[10-7-4]21等を全評価順で算出させる
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
        if haitou[umaban] != 0:
            hukumujoken1.append(haitou[umaban])
        if haitou[umaban2] != 0:
            hukumujoken2.append(haitou[umaban2])
        if haitou[umaban3] != 0:
            hukumujoken3.append(haitou[umaban3])
        if hukusita_thresh[0][0]<=float(hukusita[umaban]) < hukusita_thresh[0][1]:
            buy01 += 1
            if haitou[umaban] != 0:  #複勝１位処理
                arihit += 1
                hukulist.append(haitou[umaban])
                arisyuusi += int(haitou[umaban])
        if hukusita_thresh[1][0]<=float(hukusita[umaban2]) < hukusita_thresh[1][1]:
            buy02 += 1
            if haitou[umaban2] != 0:  #複勝2位処理
                arihit2 += 1
                hukulist2.append(haitou[umaban2])
                arisyuusi2 += int(haitou[umaban2])
        if hukusita_thresh[2][0]<=float(hukusita[umaban3]) < hukusita_thresh[2][1]:
            buy03 += 1
            if haitou[umaban3] != 0:  #複勝3位処理
                arihit3 += 1
                hukulist3.append(haitou[umaban3])
                arisyuusi3 += int(haitou[umaban3])
            

        idpost = raceid[i+1]
        firsth = lasth
        syussou = 1
        renjiku = 0
        renhimo = 0
        theaianswer = []

print("評価値1位複勝配当")
#print(hukumujoken1)
#print("複勝配当--------------------------------------------")
#pprint.pprint(hukulist)
print("評価値2位複勝配当")
#print(hukumujoken2)
print("評価値3位複勝配当")
#print(hukumujoken3)

print("-----------------------------------------------------")
print("試行レース数:"+str(racetime))
print("評価値1位: ["+str(a00)+"-"+str(a01)+"-"+str(a02)+"] "+str(a00+a01+a02))
print("評価値2位: ["+str(a10)+"-"+str(a11)+"-"+str(a12)+"] "+str(a10+a11+a12))
print("評価値3位: ["+str(a20)+"-"+str(a21)+"-"+str(a22)+"] "+str(a20+a21+a22))
print("評価値4位: ["+str(a30)+"-"+str(a31)+"-"+str(a32)+"] "+str(a30+a31+a32))
print("評価値5位: ["+str(a40)+"-"+str(a41)+"-"+str(a42)+"] "+str(a40+a41+a42))
print("評価値6位: ["+str(a50)+"-"+str(a51)+"-"+str(a52)+"] "+str(a50+a51+a52))

print("複勝1位")
print("購入回数:", buy01)
print("的中回数:", arihit)
#print("的中リスト：", hukulist)
try:
    print("的中率：", "{:.2f}".format(arihit/buy01*100),"%")
    print("回収率：", "{:.2f}".format(arisyuusi/buy01),"%" )
except:
    print("an error occured")
print("-----------------------------------------------------")

print("複勝2位")
print("購入回数:", buy02)
print("的中回数:", arihit2)
print("的中リスト：", hukulist2)
try:
    print("的中率：", "{:.2f}".format(arihit2/buy02*100),"%")
    print("回収率：", "{:.2f}".format(arisyuusi2/buy02),"%" )
except:
    print("an error occured")
print("-----------------------------------------------------")
print("複勝3位")
print("購入回数:", buy03)
print("的中回数:", arihit3)
print("的中リスト：", hukulist3)
try:
    print("的中率：", "{:.2f}".format(arihit3/buy03*100),"%")
    print("回収率：", "{:.2f}".format(arisyuusi3/buy03),"%" )
except:
    print("an error occured")
print("-----------------------------------------------------")

print("複勝1~3位合算")
print("的中率：", "{:.2f}".format((arihit + arihit2+arihit3)/(buy01+buy02+buy03)*100),"%")
print("払い戻し額/投資額:"+"{:.0f}".format(arisyuusi+arisyuusi2+arisyuusi3)+"円 / " + str((buy01+buy02+buy03)*100) + "円")
print("回収率：", "{:.2f}".format((arisyuusi+arisyuusi2+arisyuusi3)/(buy01+buy02+buy03)),"%" )