import pandas as pd

df = pd.read_csv("my.csv", encoding='gbk')
hive = "id string"
hbase = ":key"

for index, row in df.iterrows():
    hbase += (",f:" + row['hbase'])
    hive += ", " + row['hive'] + " " + row['dtype']

sql = "CREATE EXTERNAL TABLE film44(" + \
      hive + ") STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler' " \
      "WITH SERDEPROPERTIES (\"hbase.columns.mapping\" = \"" + \
      hbase + "\") TBLPROPERTIES(\"hbase.table.name\" = \"film22\");"

print(sql)


