# from flask import jsonify

gj_dict = {
    "大陆": "c_Mainland",
    "美国": "c_America",
    "韩国": "c_Korea",
    "日本": "c_Japan",
    "香港": "c_Hongkong",
    "台湾": "c_Taiwan",
    "泰国": "c_Thailand",
    "印度": "c_India",
    "法国": "c_France",
    "英国": "c_England",
    "俄罗斯": "c_Russia",
    "意大利": "c_Italy",
    "西班牙": "c_Spain",
    "德国": "c_Germany",
    "波兰": "c_Poland",
    "澳大利亚": "c_Australia",
    "伊朗": "c_Iran",
    "其他": "c_Others"
}

jd_list = [
    ["2016第一季度", "2016-03-31", "2016-01-01"],
    ["2016第二季度", "2016-06-30", "2016-04-01"],
    ["2016第三季度", "2016-09-30", "2016-07-01"],
    ["2016第四季度", "2016-12-31", "2016-10-01"],
    ["2017第一季度", "2017-03-31", "2017-01-01"],
    ["2017第二季度", "2017-06-30", "2017-04-01"],
    ["2017第三季度", "2017-09-30", "2017-07-01"],
    ["2017第四季度", "2017-12-31", "2017-10-01"],
    ["2018第一季度", "2018-03-31", "2018-01-01"],
    ["2018第二季度", "2018-06-30", "2018-04-01"],
    ["2018第三季度", "2018-09-30", "2018-07-01"],
    ["2018第四季度", "2018-12-31", "2018-10-01"],
]

rtn_dict = {
    "counties": list(gj_dict.keys()),
    "timeline": [x[0] for x in jd_list],
    "series": [],
}
#
# def exec_sql(sql):
#     global rtn_dict
#     cursor.execute(sql)
#     result = cursor.fetchall()[0]
#
#     if result[0] is None:
#         result[0] = 0
#     if result[2] is None:
#         result[2] = 0
#     print( result)
#     return result


for jd in jd_list:
    temp_list = []
    for (k_gj, v_gj) in gj_dict.items():
        sql = "SELECT sum(t.boxoffice),count(t.id),max(t.boxoffice),\'%s\',\'%s\' " % (k_gj, jd[0])
        sql = sql + "FROM film44 t WHERE t.%s=1 " % v_gj
        sql = sql + "and mdate <= \'%s\'and mdate >=\'%s\'" % (jd[1], jd[2])

        # r = exec_sql(sql)
        print(sql)
        # if r is not None:
        #     temp_list.append(r)
    # rtn_dict["series"].append(temp_list)
    # print(rtn_dict)