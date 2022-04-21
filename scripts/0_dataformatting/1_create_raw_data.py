import pandas as pd
import numpy as np
import shutil
import os

BASEDIR ="1_raw_data_for_c2s"
# java sourceの保存 statusはtrain or val or test が入る
def saveJavaSource(idx: int, source_str: str, status:str,when:str ):
  f = open("./"+BASEDIR +"/" + when +"/"+status+"/"+str(idx)+".java", mode="w")
  f.write(source_str)
  f.close()

# ファイルを分割して保存する

for status in ["train", "val","test"]:
  df = pd.read_csv(f"./0_raw_data_splitted/{status}.csv",index_col=0)
  df["index"] = df.index
  df = df.loc[0:640] # 10ファイルずつのみ
  for when in ["before", "after"]:
    df[["index",when]].apply(lambda row: saveJavaSource(row["index"],row[when],status,when), axis=1)
    print(f"done {status}/{when}")
#　作ったjavaファイルをcode2seq/2_data_code_reviewにコピーする
from distutils.dir_util import copy_tree
copy_tree("./1_raw_data_for_c2s", "../code2seq/data/2_code_review")
# 元ディレクトリをきれいにする


for status in ["train", "val","test"]:
  for when in ["before", "after"]:
    target_dir = f"./{BASEDIR}/{when}/{status}"
    shutil.rmtree(target_dir)
    os.mkdir(target_dir)