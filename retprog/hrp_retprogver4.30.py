"""
xgbのプログラムに対して単勝式の結果を出す
4.20がベースとなっている。
dataframeで扱う
"""
########mode#########
tansyo = True
hukusyo = True
ozzper = True
#####################

#######setup#########
tan_thresh = [
    [0,0], # thresh[i][0] <= x < thresh[i][1]
    [10,15],
    [15,20],
    [0,0],
    [0,0],
]
hukusita_thresh = [
    [2,5],
    [2,5],
    [2,5],
    [0,0],
    [0,0],
]
show_ozzper_rank = 1 #1=1位
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
for i in range(hoursenum):
    raceid[i] = raceid[i][:-2]

firsth = 0
lasth = 1 #ここに出走＋１が組み込まれている
theaianswer = []
idpost = 0
syussou = 1
racetime = 0
arihit,nasihit,arisyuusi,nasisyuusi = 0,0,0,0
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
uma2hit,uma3hit = 0,0
renjiku,renhimo = 0,0
idpost = raceid[0]
tanlist = []
a00,a01,a02 = 0,0,0
a10,a11,a12 = 0,0,0
a20,a21,a22 = 0,0,0
a30,a31,a32 = 0,0,0
a40,a41,a42 = 0,0,0
a50,a51,a52 = 0,0,0
b00,b01,b02,b03,b04,b05,b06,b07 = 0,0,0,0,0,0,0,0
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
        if haitou[umaban2] != "0":
                uma2hit+=1
        if haitou[umaban3] != "0":
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
        if umaban == firsth: #単勝が当たった場合
            tansyuusi += float(tanhaitou[umaban])
            tantekityu += 1
            tanlist.append(tanhaitou[umaban])
        if tan_thresh[0][0]<= float(tanhaitou[umaban]) < tan_thresh[0][1]: #単勝ｎ倍以下なら購入回避
            tan2buytime += 1
            if umaban == firsth:
                tansyuusi2 += float(tanhaitou[umaban])
                tantekityu2 += 1

        #ここから2位評価の単勝
        if umaban2 == firsth: #単勝が当たった場合
            tansyuusi2nd += float(tanhaitou[umaban2])
            tantekityu2nd += 1
            tanlist2nd.append(tanhaitou[umaban2])
        if tan_thresh[1][0]<= float(tanhaitou[umaban2]) < tan_thresh[1][1]: #単勝ｎ倍以下なら購入回避15,25
            tan2ndbuytime += 1
            if umaban2 == firsth:
                tansyuusi2nd2 += float(tanhaitou[umaban2])
                tantekityu2nd2 += 1
        
        #ここから3位評価の単勝
        if umaban3 == firsth: #単勝が当たった場合
                tanlist3rd.append(tanhaitou[umaban3])
        if tan_thresh[2][0]<= float(tanhaitou[umaban3]) < tan_thresh[2][1]:
            b00 += 1
            if umaban3 == firsth:
                b01 += float(tanhaitou[umaban3])
                b02 += 1

        if umaban4 == firsth:
            tanlist4th.append(tanhaitou[umaban4])
        if umaban5 == firsth:
            tanlist5th.append(tanhaitou[umaban5])

        idpost = raceid[i+1]
        firsth = lasth
        syussou = 1
        renjiku = 0
        renhimo = 0
        theaianswer = []

"""print("単勝配当")
print(tanlist)
print("評価値2位単勝配当")
print(tanlist2nd)
print("評価値3位単勝配当")
print(tanlist3rd)

print("評価値4位単勝配当")
print(tanlist4th)
print("評価値5位単勝配当")
print(tanlist5th)"""

print("-----------------------------------------------------")
print("試行レース数:"+str(racetime))
print("評価値1位: ["+str(a00)+"-"+str(a01)+"-"+str(a02)+"] "+str(a00+a01+a02))
print("評価値2位: ["+str(a10)+"-"+str(a11)+"-"+str(a12)+"] "+str(a10+a11+a12))
print("評価値3位: ["+str(a20)+"-"+str(a21)+"-"+str(a22)+"] "+str(a20+a21+a22))
print("評価値4位: ["+str(a30)+"-"+str(a31)+"-"+str(a32)+"] "+str(a30+a31+a32))
print("評価値5位: ["+str(a40)+"-"+str(a41)+"-"+str(a42)+"] "+str(a40+a41+a42))
print("評価値6位: ["+str(a50)+"-"+str(a51)+"-"+str(a52)+"] "+str(a50+a51+a52))

print("1~3位PHR: "+"{:.3f}".format((a00+a01+a02+a10+a11+a12+a20+a21+a22)/racetime))
print("1~3位WHR: "+"{:.3f}".format((a00+a10+a20)/racetime))
print("1~6位PHR: "+"{:.3f}".format((a00+a01+a02+a10+a11+a12+a20+a21+a22+a30+a31+a32+a40+a41+a42+a50+a51+a52)/racetime))
#print("評価値1位的中回数:"+str(arihit))
#print("評価値2位的中回数:"+str(uma2hit))
#print("評価値3位的中回数:"+str(uma3hit))

print("単勝オッズ上下限設定時-----------------------------------------")
print("回避レース数:"+str(racetime - tan2buytime))
print("単勝的中回数:" + str(tantekityu2))
#print("単勝的中率:"+"{:.2f}".format(tantekityu2/tan2buytime *100)+"%")
print("払い戻し額/投資額:"+ "{:.1f}".format(tansyuusi2*100)+"円 / "+str((tan2buytime)*100) + "円")
#print("回収率:" + "{:.2f}".format(tansyuusi2*100/ (tan2buytime*100)*100)+ "%")
print("評価値2位単勝オッズ上下限設定時-----------------------------------------")
print("回避レース数:"+str(racetime - tan2ndbuytime))
print("単勝的中回数:" + str(tantekityu2nd2))
#print("単勝的中率:"+"{:.2f}".format(tantekityu2nd2/tan2ndbuytime *100)+"%")
print("払い戻し額/投資額:"+ "{:.1f}".format(tansyuusi2nd2*100)+"円 / "+str((tan2ndbuytime)*100) + "円")
#print("回収率:" + "{:.2f}".format(tansyuusi2nd2*100/ (tan2ndbuytime*100)*100)+ "%")
print("評価値3位単勝オッズ上下限設定時-----------------------------------------")
print("回避レース数:"+str(racetime - b00))
print("単勝的中回数:" + str(b02))
#print("単勝的中率:"+"{:.2f}".format(b02/b00 *100)+"%")
print("払い戻し額/投資額:"+ "{:.1f}".format(b01*100)+"円 / "+str((b00)*100) + "円")
#print("回収率:" + "{:.2f}".format(b01*100/ (b00*100)*100)+ "%")
print("評価値1，2位単勝上下限設定時-----------------------------------------")
print("単勝的中回数:" + str(tantekityu2nd2 + tantekityu2))
print("全体的中率:" "{:.2f}".format((tantekityu2nd2 + tantekityu2)/racetime*100)+ "%")
#print("単勝的中率:"+"{:.2f}".format((tantekityu2nd2 + tantekityu2) /(tan2ndbuytime + tan2buytime) *100)+"%")
#print("払い戻し額/投資額:"+"{:.1f}".format((tansyuusi2nd2+tansyuusi2)*100)+"円 / " + str((tan2ndbuytime + tan2buytime)*100) + "円")
#print("回収率:" + "{:.2f}".format((tansyuusi2nd2 + tansyuusi2)*100/ ((tan2ndbuytime + tan2buytime)*100)*100)+ "%")

print("-----------------------------------------------------")
print("評価値1~3位単勝上下限設定時-----------------------------------------")
print("単勝的中回数:" + str(tantekityu2nd2 + tantekityu2 + b02))
print("全体的中率:" "{:.2f}".format((tantekityu2nd2 + tantekityu2 + b02)/racetime*100)+ "%")
print("単勝的中率:"+"{:.2f}".format((tantekityu2nd2 + tantekityu2 + b02) /(tan2ndbuytime + tan2buytime + b00) *100)+"%")
print("払い戻し額/投資額:"+"{:.1f}".format((tansyuusi2nd2+tansyuusi2 + b01)*100)+"円 / " + str((tan2ndbuytime + tan2buytime + b00)*100) + "円")
print("回収率:" + "{:.2f}".format((tansyuusi2nd2 + tansyuusi2 + b01)*100/ ((tan2ndbuytime + tan2buytime + b00)*100)*100)+ "%")
print("-----------------------------------------------------")