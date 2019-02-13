# flavour_hunter

**这是一个很不规范的文档，用于在开发阶段作为草稿给我们几个自己看**

关于仓库的目录

flavour_hunter

├─analyze     *数据分析模块*

├─backend    *后端模块*

├─docs      *用来储存一些md格式的文档*

├─frontend *前端模块*

└─spider *爬虫模块*

队伍成员自己整理的一些文档（写成markdown上传博客或github，用来替代QQ群传word交流的形式）：

0. 各成员的详细学习资料整理，传送门在下面的分工表格中（目前踩完了17级两个人的坑）
1. [黄琦：对几个微信公众号2018年到现在所发表爬虫文章的简单整理](https://hqzing.github.io/2019/02/10/0002/)
2. [黄琦：安装thrift并使用python3驱动Hbase](https://hqzing.github.io/2019/02/11/3/)
3. [黄琦：使用python3通过pyhive操作Hive](https://hqzing.github.io/2019/02/11/4/)
4. [黄琦：Hive与Hbase整合，共享表和数据](https://hqzing.github.io/2019/02/12/5/)
5. [李思佳：参考资源与可爬取网站整合（各种链接](https://github.com/hqZing/flavour_hunter/blob/master/docs/%E5%8F%82%E8%80%83%E8%B5%84%E6%BA%90%E4%B8%8E%E5%8F%AF%E7%88%AC%E5%8F%96%E7%BD%91%E7%AB%99%E6%95%B4%E5%90%88%EF%BC%88%E5%90%84%E7%A7%8D%E9%93%BE%E6%8E%A5%EF%BC%89.md)
6. [李思佳：项目策划电影篇](https://github.com/hqZing/flavour_hunter/blob/master/docs/%E9%A1%B9%E7%9B%AE%E7%AD%96%E5%88%92%E7%94%B5%E5%BD%B1%E7%AF%87.md)
7. [黄琦：本项目虚拟机使用指南](https://github.com/hqZing/flavour_hunter/blob/master/docs/本项目虚拟机使用指南.md)

## 1. 备赛要点

**主要的评分项在这里，根据得分点来设计作品**

| 主要评分项 | 解释 |
| -------- | -------- |
| 作品意义 | 必须能够自圆其说 |
| 完成程度 | 在word文档里面必须要有所体现，体现我做了什么东西 |
| 逻辑完整性 | 包括数据的逻辑完整性和需求的逻辑完整性 |
| 成果展示 | 必须部署在云服务器上让评委通过网址访问 |
| 架构设计原则 | 说明选用的框架以及为什么使用这个框架而不用别的框架 |



## 2. 功能需求

**这里的功能需求是根据上面的得分点制定出来的，编写程序实现这些功能**

//TODU


## 3. 技术架构

**经过考虑，挑选了这些工具。使用这些工具完成上面的功能代码**

//TODU

## 4. 人员分工


**各主要模块**

| 模块 | 大概工作 | 备注 |
| ----- | --------- | ---- |
| 爬虫 | 爬虫写入Hbase | 
| 数据分析 | 使用Hive从Hbase从读取数据进行分析，分析结果存入mysql中 |  |
| web前后端 | 后端给前端提供web api，读取mysql的内容输出给前端。前端用ajax访问后端接口，用echarts等UI框架进行可视化 |  |
| 设计与完善工作 |  文档撰写、视频剪辑、需求确定、字段统一、架构设计、集群部署 |   |


**总体分工**

| 模块 | 人员 | 备注 |
| ----- | ----| ------|
| 爬虫 | 李鑫宇（主要负责）严东阳（协助）|  |
| 数据分析 | 孙志远（主要负责）、严东阳（协助）|   |
| web前后端 | 黄琦、李思佳 |   |
| 设计与完善工作 | 黄琦、李思佳 |   |


**个人任务详情**

| 人员 | 详情 | 学习资料 |
| ---- | ---- | ---------- |
| 李鑫宇 |  1. 学习Hbase的基本用法，不需要学习太深，够用就行，看一天左右就行了。<br>2. 学会用python驱动Hbase，对其进行增删改查操作（主要是插入操作）<br> 3. 编写爬虫，按需求将爬取到的信息存到Hbase中<br> 4. 爬虫要爬好几个网站，工作量较大，暂时不分配过多任务  |  [学习资料](https://github.com/hqZing/flavour_hunter/blob/master/docs/lxy_help.md) |
| 孙志远 | 1. 学习Hive的基本用法。<br>2. 学习用python驱动Hive和mysql。<br>3. 根据大家讨论得出的要求，将所需要统计的内容通过HiveSQL语句查询出来，存入mysql中，供web后端程序使用。<br>4. 注意，虚拟机中已经安装了mysql，其中一些表是用来存储Hive的配置数据的（也称为元数据），不用管那些表，就只管创建自己的新表去存储统计得出的数据就行了 |   [学习资料](https://github.com/hqZing/flavour_hunter/blob/master/docs/szy_help.md) |
| 严东阳 | 1. 爬虫的目标网站较多，一个人不够应付，在有必要的时候，去帮忙写一些爬虫代码。 | 无  |
| 李思佳 | 后端工作较为简单，不会占用太多时间。主要和黄琦一起商量前端的美化和项目的优化，以及上面提到的设计与完善工作，这部分工作占了项目的半边天，想办法在这些方面提高项目竞争力  | 无  |
| 黄琦 | 研究使用ambari在云服务器上建立内网集群 ，沟通各种大小事情，解决各种疑难杂症，处理上面的设计与完善工作。并在开发环境上面提前进行踩坑 | 无 |

分工任务不是限定死的，尽可能快速的完成自己的工作然后互相帮助。争取更多时间来互相优化。开发过程中有疑问的话第一时间发到群里讨论





## 5. 开发环境

### 5.1 编程语言、框架

除了网页前端以外，所有环节统一使用python

大数据框架已经在虚拟机中配置好了

前端可视化框架使用echarts

### 5.2 虚拟机

为了统一所有人的开发工具，方便后期集成和部署，我配好了一个ubuntu虚拟机，所有人使用这套环境进行开发。

[本项目虚拟机使用指南](https://github.com/hqZing/flavour_hunter/blob/master/docs/本项目虚拟机使用指南.md)
[我自己录的视频说明](https://pan.baidu.com/s/1Ztu33-pdEF1fallVwCGJzg) 提取码：mc2i 
[虚拟机下载地址](https://pan.baidu.com/s/1iJp9mqMd6dls_QfFYMTjJA) 提取码：4mx8 

### 5.3 云服务器

华为云学生机，目前由严东阳搭建

| 主机名 | master.hd | slave1.hd | slave2.hd |
| ------- | ----------- | ----------- |---------- |
| 公网IP | 114.115.169.217 | 114.116.5.101 |
| 内网IP | 172.16.0.22 | 192.168.10.156 |
| 用户名 | root | root | root |
| 登陆密码 | DHv2535fg | NT4bDKPVg |
| 学生机拥有者 | 黄琦 | 严东阳 |
| 控制台账号 | 18677681204 | hahaha1235 |
| 控制台密码 | xgsn1D++ | NT4bDKPVgHQIxpEK |

## 6. 网上可用的参考资料

1. [发现杯官方，赛事说明会的回放链接 ](http://www.tmooc.cn/course/100054.shtml)
2. 在github上面搜索“发现杯”，可以搜到一些去年的作品，有几个把截图和演示视频都放进去了。有空的时候可以去看看
3. [【厦门大学】大数据技术原理与应用 ](https://www.bilibili.com/video/av25922369)
4. [与厦大这门课程配套的学习指南和各种软件的安装、使用教程。](http://dblab.xmu.edu.cn/blog/)虽然教程有点旧，但依旧可以正常使用，照着打代码打命令就可以了。
5. [轻松部署ambari2.7](https://www.bilibili.com/video/av30362634)
6. [如何优雅地使用Apache Ambari安装HDFS、HBase等分布式应用](https://www.jianshu.com/p/af50f3e8b8b2)


