import schedule
import time
import datetime
import sys
import csv
import sqlite3
import subprocess

INET_ID = "xxxxxxxx"
kanyusya_NUM = "xxxx"
PASSWORD = "xxxx"
P_ARS_NUM = "xxxx"
bakenshiki = "TANSYO"
MONEY = "100"
flag_shutdown = False #17時にシャットダウンする際はTrueに

"""
buy_processが時間で起動し、which_raceを呼び出し、
which_raceがozz_listを呼び出すことでozz_listはそのレースだけの
オッズをsqliteサーバから呼び出しDBdata_req()に格納する。
DBdata_req()では、必要なデータ(そのレースのデータ)のみを取り出すようになっている
詳しくはEvernote参照
"""
csv_list = [] #buydata.csvそのもの(ヘッダーは消す)
DBdata = [] #DBdata_req()にて格納
THEracedata = [] #which_race()にて格納,csv_listの、該当レースのみを取り出したもの
buy_umaban = [] #最終的に購入する馬番がここに格納される
ozz_list = [] #購入該当馬のオッズを全て表示する
ozzrange = [0,0] #オッズ上下限がこのリストに書き込まれる
cmd = ""
hukunum = ""
baba_flag = True #良馬場ならTrue
placedic_toCODE = {"札幌":"SAPPORO","函館":"HAKODATE","福島":"FUKUSHIMA",
				"新潟":"NIIGATA","東京":"TOKYO","中山":"NAKAYAMA",
				"中京":"TYUKYO","京都":"KYOTO","阪神":"HANSHIN","小倉":"KOKURA"}
placedic_toNUM = {"札幌":"01","函館":"02","福島":"03",
				"新潟":"04","東京":"05","中山":"06",
				"中京":"07","京都":"08","阪神":"09","小倉":"10"}
umabanform = {"0":"00","1":"01","2":"02","3":"03","4":"04","5":"05","6":"06","7":"07","8":"08","9":"09",
	"10":"10","11":"11","12":"12","13":"13","14":"14","15":"15","16":"16","17":"17","18":"18","19":"19",
	"20":"20","21":"21","22":"22","23":"23","24":"24","25":"25","26":"26","27":"27","28":"28","29":"29",
	"30":"30","31":"31","32":"32"}
#csvのデータはデータベースと違って更新の必要はないので最初に読み込む
csvfile = open("buydata.csv", encoding="utf-8") #この名前しか読み出さないので注意！
for i in csv.reader(csvfile):
	csv_list.append(i)
del csv_list[0] #一番上のヘッダーはいらないので削除
def buy_process(): #全ての処理の大元
	if which_race(time_now.hour,time_now.minute): #THEracedateに書き込まれる
		print("------------------------------------------------------------------------------------")
		print(time_now.hour,"時",time_now.minute,"分","which_raceが可決されました。購入処理に入ります。")
		if baba_judge(THEracedata): #良馬場かを確認
			DBdata_req(time_now) #DBdataにデータが書き込まれる
			ozzrange_process() #そのコース条件のオッズ上下限をozzrangeに格納する
			buy_judge() #DBdataを元にして競争条件とオッズを考慮して購入を決める
			ipatgo() #ここで完全な購入処理が行われる
		else:
			print("馬場状態が良ではない為、回避します。")
		time.sleep(120) #連続して同じレースが購入されるのを防ぐ

def baba_judge(theracedata):
	with sqlite3.connect("database.db") as conn:
		cursor = conn.cursor()
		babadata = list(cursor.execute("SELECT * FROM S_TENKO_BABA"))
		babadata = [i for i in babadata if i[5] == placedic_toNUM[theracedata[0]]]
	#print(babadata)
	for i in range(len(babadata)):
		if babadata[i][9] == "1" or babadata[i][9] == "3":
			shiba = babadata[i][11]
			dart = babadata[i][12]
	if "d" in theracedata[4]:
		return dart == "1" #良馬場ならTrue,それ以外ならFalseを返す
	else: #芝
		return shiba == "1"
		
	return babadata #babadataにもう一回なんらかの処理をした後この行は消して良い

def DBdata_req(datime): #SQLiteサーバからDBdataにデータを格納
	global DBdata
	with sqlite3.connect("database.db") as conn:
		cursor = conn.cursor()
		DBdata = list(cursor.execute("SELECT * FROM S_ODDS_TANPUKU"))
		DBdata = [i for i in DBdata if i[2] == ( umabanform[str(datime.month)] + umabanform[str(datime.day)] ) 
		and  i[3] == placedic_toNUM[THEracedata[0]] and i[6] == umabanform[THEracedata[1]]]
		#↑データの選別.これで、DBdataには、馬番順にtest1のフォーマットでデータ格納
		#i[2] == ( umabanform[str(datime.month)] + umabanform[str(datime.day)] ) のところ確認済み
		#print(DBdata[0][0])
		
def which_race(hour,minute): #購入時間に該当するか判定、該当するならTHEracedataに格納
	global THEracedata
	for i in range(len(csv_list)):
		if 58 <= int(minute) <=59: #hour側を繰り上げないといけない
			hour = int(hour) +1
			minute = int(minute) - 60
		if int(hour) == int(csv_list[i][2]) and int(minute) + 2 == int(csv_list[i][3]) :#締め切り1分前(出走2分前)
			#同行の全データをTHEracedataに格納
			THEracedata = csv_list[i] #完璧に塗り替えるので初期化不要
			return True
		#which_raceは17:00にプログラム終了処理を行う
		if int(hour) == 17 :
			print("17時になりました。本日の処理を終了します。")
			subprocess.call("TASKKILL /F /IM EveryDB2.exe")
			if flag_shutdown == True:
				subprocess.call("shutdown -s -t 60")
			sys.exit()

def ozzrange_process(): #そのコース条件のオッズ上下限をozzrangeに格納する
	global ozzrange
	global MONEY
	ozzrange = [0,0]
	p = THEracedata[0] #競馬場
	k = THEracedata[4] #芝ダート、距離
	if p == "札幌":
		print("No Data")
		sys.exit()
	elif p == "函館":
		if k == "1200":
			ozzrange = [10,30]
		elif k == "d1700":
			ozzrange = [10,30]
	elif p == "新潟":
		if k == "d1200":
			ozzrange = [9,30]
		elif k == "d1800":
			ozzrange = [9,30]
	elif p == "小倉":
		if k == "1200":
			ozzrange = [10,50]
		elif k == "d1700":
			ozzrange = [10,40]
	elif p == "阪神":
		if k == "1800":
			ozzrange = [1.5,5.5]
		elif k == "d1400":
			ozzrange = [5,10]
		elif k == "d1800":
			ozzrange = [20,50]
	elif p == "中山":
		if k == "1600":
			ozzrange = [1.5,5]
		elif k == "d1800":
			ozzrange = [7,15]
		elif k == "d1200":
			ozzrange = [7,15]
	elif p == "東京":
		if k == "d1400":
			ozzrange = [10,30]
		elif k == "d1600":
			ozzrange = [3,7]
		elif k == "1600":
			ozzrange = [10,15]
	elif p == "京都":
		if k == "d1800":
			ozzrange = [10,50]
		elif k == "d1400":
			ozzrange = [10,30]
		elif k == "d1200":
			ozzrange = [10,30]
	elif p == "福島":
		if k == "1200":
			ozzrange = [10,20]
	else:
		print("buydata.csv内、競馬場名が不正です。")
		sys.exit()
	if ozzrange == [0,0]:
		print("buydata.csv内、距離欄が不正である可能性があります。")
		sys.exit()

def buy_judge():
	global buy_umaban
	global ozz_list
	global hukunum
	buy_umaban = [] #初期化
	ozz_list = []
	hukunum = ""
	flag_1_5 = False
	if THEracedata[5] != "":
		for i in range(len(DBdata)):
			if umabanform[THEracedata[5]] == DBdata[i][7]: #馬番1(◎)のこと
				ozz_list.append(THEracedata[5]+"番"+DBdata[i][8]+"倍")
				if float(ozzrange[0]) <= float(DBdata[i][8])/10 <= float(ozzrange[1]): #ozzrangeの条件を満たすなら
					buy_umaban.append(THEracedata[5])
				if float(DBdata[i][8])/10 <= 1.5:
					flag_1_5 = True
			elif THEracedata[6] != "" and umabanform[THEracedata[6]] == DBdata[i][7]: #馬番2(○)のこと
				ozz_list.append(THEracedata[6]+"番"+DBdata[i][8]+"倍")
				if float(ozzrange[0]) <= float(DBdata[i][8])/10 <= float(ozzrange[1]): #ozzrangeの条件を満たすなら
					buy_umaban.append(THEracedata[6])
				if float(DBdata[i][8])/10 <= 1.5:
					flag_1_5 = True
			elif THEracedata[7] != "" and umabanform[THEracedata[7]] == DBdata[i][7]: #馬番3(▲)のこと
				ozz_list.append(THEracedata[7]+"番"+DBdata[i][8]+"倍")
				if float(ozzrange[0]) <= float(DBdata[i][8])/10 <= float(ozzrange[1]): #ozzrangeの条件を満たすなら
					buy_umaban.append(THEracedata[7])
				if float(DBdata[i][8])/10 <= 1.5:
					flag_1_5 = True
			"""
			elif 以下、Theracedata[6] と[7]に関しては、まずその中に数字が入っているか
			どうかを確認するため、THEracedata[6] != "" andが入っている。
			([5]については最初のifで確認済み)
			これは、評価値1,2位の単勝だけ、などのときに必要になる。
			"""
		#複勝式
	if THEracedata[8] != "":
		for i in range(len(DBdata)):
			if umabanform[THEracedata[8]] == DBdata[i][7]:
				ozz_list.append("複勝式" + THEracedata[8] +"番 下限"+DBdata[i][10]+"倍")
				if 1.9 <= float(DBdata[i][10])/10 <= 10:
					hukunum = THEracedata[8]
				else:
					hukunum = ""
	print(ozz_list)
	if flag_1_5:
		buy_umaban = []
		print("上位評価馬番に単勝1.5倍以下の馬が該当します。購入を見送ります。")

def ipatgo():
	global cmd
	if len(buy_umaban) == 0:
		print("購入該当馬が存在しませんでした。",THEracedata[0],THEracedata[1],"R 単勝式の購入を見送ります。")
	else:
		for i in range(len(buy_umaban)):
			cmd = "ipatgo.exe data"+" "+INET_ID+" "+kanyusya_NUM+" "+PASSWORD+" "+ \
			P_ARS_NUM+" "+str(time_now.year)+umabanform[str(time_now.month)]+umabanform[str(time_now.day)]+","+ placedic_toCODE[THEracedata[0]]+"," +THEracedata[1]+ ","+ \
			bakenshiki+ "," + "NORMAL" + ",," + umabanform[buy_umaban[i]] + "," + MONEY
			result = subprocess.call(cmd) #購入処理の実行(テスト時はコメントアウトしておく)
			if result == 0: #購入処理の判定
				print(THEracedata[0],THEracedata[1],"R",buy_umaban[i],"番",MONEY,"円 購入処理は正常に行われました。")
				votedata_report(buy_umaban[i],"単勝",MONEY)
			else:
				print(THEracedata[0],THEracedata[1],"R",buy_umaban[i],"番",MONEY,"円 ipatgo送信時に例外が発生しました。")
				print("処理を継続します。")
			time.sleep(1)
	if hukunum != "": #複勝購入
		print("複勝式の購入が可決されました。" + hukunum + "番")
		time.sleep(1)
		cmd2 = "ipatgo.exe data"+" "+INET_ID+" "+kanyusya_NUM+" "+PASSWORD+" "+ \
			P_ARS_NUM+" "+str(time_now.year)+umabanform[str(time_now.month)]+umabanform[str(time_now.day)]+","+ placedic_toCODE[THEracedata[0]]+"," +THEracedata[1]+ ","+ \
			"FUKUSYO"+ "," + "NORMAL" + ",," + umabanform[hukunum] + "," + MONEY
		result = subprocess.call(cmd2) #購入処理の実行(テスト時はコメントアウトしておく)
		if result == 0: #購入処理の判定
			print(THEracedata[0],THEracedata[1],"R","複勝",hukunum,"番",MONEY,"円 購入処理は正常に行われました。")
			votedata_report(hukunum,"複勝",MONEY)
		else:
			print(THEracedata[0],THEracedata[1],"R","複勝",hukunum,"番",MONEY,"円 ipatgo送信時に例外が発生しました。")
			print("処理を継続します。")

def database_upload():
	today = datetime.date.today()
	yesterday = today + datetime.timedelta(days = -1)
	with sqlite3.connect("database.db") as conn:
		curs = conn.cursor()
		curs.execute("UPDATE S_ODDS_TANPUKU SET MakeDate = '" + str(yesterday.year)+umabanform[str(yesterday.month)]+umabanform[str(yesterday.day)]
		+ "' WHERE MakeDate = "+ str(today.year)+umabanform[str(today.month)]+umabanform[str(today.day)] )

def votedata_report(umaban,baken,money):
    global THEracedata
    vote_data = open("votedata_log/"+umabanform[str(time_now.month)]+"_"+
    umabanform[str(time_now.day)]+"votedata.csv", "a")
    writer = csv.writer(vote_data,lineterminator='\n')
    writer.writerow([THEracedata[0],THEracedata[1],THEracedata[4],umaban,baken,money])

def nyukin_process():
	global MONEY
	nyukingaku = int(MONEY)*20
	print("入金指示を行いますか？（1:はい 0:いいえ）")
	tf01 = int(input())
	if tf01 == 1:
		print("デフォルト値で入金しますか？（1:はい 0:いいえ）")
		print("デフォルト値：",str(int(MONEY)*20),"円")
		tf02 = int(input())
		if tf02 == 0:
			print("入金金額を入力してください。(100円単位、半角数字)")
			nyukingaku = int(input())
		cmd = "ipatgo.exe deposit"+" "+INET_ID+" "+kanyusya_NUM+" "+PASSWORD+" "+ \
			P_ARS_NUM+" "+str(nyukingaku)
		print("戻り値を待っています...")
		result = subprocess.call(cmd)
		if result == 0:
			print("入金が完了しました。")
			print("Ex Machinaをこのまま起動します。")
		else:
			print("入金ができませんでした。手動で入金指示を行ってください。")
			print("Ex Machinaをこのまま起動します。")



print("automachinaを起動します。 \
	\nbuydata.csvが最新のものか確認してください。\nEveryDBが稼働しているか確認してください。")
print("金額:",MONEY,"円")
nyukin_process()
#処理継続プロセス
if __name__ == "__main__":
	while True: #終了処理はsys.exit()で行われる
		time_now = datetime.datetime.now()
		buy_process()
		database_upload()
		time.sleep(30) #30秒ごとに実行