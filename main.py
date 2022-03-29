import subprocess
import sqlite3
import pandas as pd
import re
import time
import win32clipboard as w32c
import random


class asiseika:
    def __init__(self):
        c.execute("CREATE TABLE IF NOT EXISTS chara(id integer PRIMARY KEY, name text PRIMARY KEY)")
        c.execute("CREATE TABLE IF NOT EXISTS ex(id integer PRIMARY KEY,path text)")
        conn.commit()

    def readtolk(self,exe_path,voice,text_path,coma):
        vice = int(voice)
        cmd =  exe_path+f" -cid {voice} {coma} "+text_path
        print(cmd)
        subprocess.run(cmd,shell=True)

    def paexe(self):
        while True:
            df = pd.read_sql("SELECT * FROM ex",conn)
            de = df.empty
            if de == False:
                print(df)
            else:
                path=input(r"SeikaSay2のexeファイルがあるパスを入力してください")
                path = re.sub("\"","",path)
                path = re.sub(r"\\","\*",path)
                path = re.sub("\*",r"\\",path)
                path = path+r"\\"+r"SeikaSay2.exe"
                print(path)
                sql = f"INSERT INTO ex (id,path) values(1,'{path}')"
                print(sql)
                c.execute(sql)
                conn.commit()
                return path
            d =self.yn("実行パスを変更しますか？")
            if d==0:
                df = df["path"][0]
                return df
            else:
                path=input(r"SeikaSay2のexeファイルがあるパスを入力してください")
                path = re.sub("\"","",path)
                path = re.sub(r"\\",r"*",path)
                path = re.sub(r"*",r"\\",path)
                path = path+r"\\"+r"SeikaSay2.exe"
                print(path)
                sql = f"UPDATE ex SET {path} where id = 1')"
                print(sql)
                c.execute(sql)
                comm.commit()
                return path
                
        
    def sert(self,a,b):
        sql = f"INSERT INTO chara (id,name) values({a},'{b}')"
        print(sql)
        c.execute(sql)
        conn.commit()

    def update(self,a,b):
        aaa = f"UPDATE chara SET name = {a} where name = {b}"
        c.excute(aaa)
        conn.commit()

    def selectuse(self):
        df = pd.read_sql("SELECT * FROM chara", conn)
        print(df)
        id = int(input("使用したいvoiceloidの先頭にある数字を入力してください="))
        return df["id"][id]#タプル

    def yn(self,text):
        y=""
        while True:
            y=input(text +"(y/n)=")
            if(y=="y"):
                return 1
            elif(y=="n"):
                return 0

    def select(self):
        a = self.yn("voiceloidの-cidを入力しますか？もしくは紐づけられた名前を変更しますか？")
        while True:
            if a==0:
                break
            aa=input("新規[0]変更[1]=")
            print(aa)
            if aa=="0":
                try:
                    aa = input("-cid欄の4桁の数字を入力してください=")
                    name=input("紐づける名前を入力してください=")
                    aa = int(aa)
                    cid=[aa,name]
                    self.sert(cid[0],cid[1])
                except:
                    print("入力に失敗しました。\nすでに入力された-cidの可能性があります")
            elif aa=="1":
                try:
                    aa = input("名前を入力してください=")
                    name=input("変更する名前を入力してください=")
                    df = pd.read_sql("SELECT * FROM chara", conn)
                    print(df)
                    self.update(name, aa)
                except:
                    print("変更に失敗しました。\n登録された-cidが存在しない可能性があります")
            a = self.yn("もう一度入力を行いますか？")

    def monitor(self,interval_sec, onchange):
        pre_seq = None

        def read(self):
            try:
                w32c.OpenClipboard()
                return w32c.GetClipboardData()
            except Exception as ex:
                return ex
            finally:
                w32c.CloseClipboard()

        while True:
            seq = w32c.GetClipboardSequenceNumber()

            if pre_seq != seq:
                data = read(self)
                pre_seq = seq
                onchange(self,data)

            time.sleep(interval_sec)
    
    def clip(self,sexe,id):
        def onchange(self,text):
            if isinstance(text, Exception):
                print("Failed:",text)
            else:
                coma = "-t"
                text = re.sub(r"\n","",text)
                self.readtolk(sexe,id,text,coma)

        self.monitor(2, onchange)
    def main(self):
        try:
            self.select()
            id = self.selectuse()
            print(id)
            y=1
            sexe=self.paexe()
            print(sexe)
            while True:
                text=input("使用するテキストのパスを入力してください(終了する場合[0],voiceloidを変更する場合[1])\nクリップボードのテキスト読み上げの場合[3]=")
                if text=="0":
                    break
                elif text=="1":
                    id = self.selectuse()
                    continue
                elif text=="3":
                    try:
                        self.clip(sexe,id)

                    except:
                        print("コメントの取得に失敗しました。")
                try:
                    coma="-f"
                    self.readtolk(sexe,id,text,coma)
                except:
                    print("出力に失敗しました。\n入力データに不具合の可能性もあります。")
                
        except:
            print("すみません、メイン処理に失敗しました。")

if __name__ == '__main__':
    conn = sqlite3.connect("cid_id.db")
    c = conn.cursor()
    se = asiseika()
    se.main()    
    c.close()
    conn.close()
    print("終了しました")
    