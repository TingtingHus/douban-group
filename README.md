# douban group
豆瓣小组社区流量数据分析
# 简介
利用Python的Selenium库爬取豆瓣部分小组数据，由于豆瓣小组每日发帖量巨大（日均12万左右）且豆瓣具有严厉的反爬虫机制，故仅针对25个热门小组爬取了2020年11月28号和2020年11月29号两天（周六周日）的数据。此外，针对TOP小组活跃用户进行数据采集，刻画小组活跃用户画像。

需要说明的是:
>豆瓣小组全站范围每增加一个新帖，帖子的id就会加一，程序在12月4号到12月16(20?)号期间按照帖子id依次爬取11月28号和11月29号两天发布的帖子及回复。
>由于当天不仅可以回复当日新发帖子也可以回复过往发布的帖子，29号以后也可以回复28号和29号发布的贴子，因此，所有活跃指标均基于当日（28、29号）新发帖子，故并不能完整反映小组活跃程度，小组真实活跃情况应远高于本文分析结果。
>不仅如此，本文的部分分析指标（如点赞数等）也与程序执行的时间段高度相关。
