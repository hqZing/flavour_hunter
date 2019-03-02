这里是数据分析模块的代码，需要备注的注意事项可以写到此处

# 建表语句

```sql
CREATE EXTERNAL TABLE film44(id string, name string, male float, female float, under20 float, 20to24 float, 25to29 float, 30to34 float , 35to39 float, above40 float, degree_high float, degree_low float, city1 float, city2 float, city3 float, city4 float, occupation_whitecollar float, occupation_student float, occupation_others float, preference_action float, preference_comedy float, preference_romance float, occupation_science float, occupation_animate float) STORED BY 'org.apache.hadoop.hive.hbase.HBaseStorageHandler' WITH SERDEPROPERTIES ("hbase.columns.mapping" = ":key,f:n,f:m,f:fm,f:un20,f:20to24,f:25to29,f:30to34,f:35to39,f:ab40,f:dg_h,f:dg_l,f:ct1,f:ct2,f:ct3,f:ct4,f:oc_w,f:oc_s,f:oc_o,f:pf_ac,f:pf_co,f:pf_ro,f:pf_sc,f:pf_an") TBLPROPERTIES("hbase.table.name" = "film22");
```