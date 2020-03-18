# HRP
GBDTライブラリを用いた競馬の機械学習

dataフォルダ:  
実際に学習に用いた元データ、IDデータ、加工後データ、pickleデータなど  

hrp_feature系:  
特徴量エンジニアリング  
基本的にはラベルエンコーディングが主体となっている。  
v3以降では、IDデータから過去のレースデータを呼び出し、データフレームにするプログラムが動いている。  

xgmachina系：  
xgboostやcatboostを用いて実際に機械学習を行う。特徴量を入れたり抜いたりパラメータを替えたりしているのでバージョンがいっぱいある。  
0.2系と1.3系がcatboostを用いたモデルになっている。  
予測結果を出力するところまでを行う。  

retprog系：  
xgmachinaの出した予測結果を元に回収率を計算する。  
3.00は全体的な指標と単勝式を、3.01は複勝式を、3.02はオッズ帯ごとの回収率を算出する。  
ベースが相当前に作ったものなので可読性☓  

オマケ：  
auto_machina  
JRAのネット投票機能を用いて自動的に馬券を購入するシステム。別途JRA-VAN DataLabアプリ、"ipatdo","EveryDB2"が必要(前者は投票に、後者はリアルタイムのオッズの取得に必要)。
