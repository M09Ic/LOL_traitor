# LOL_traitor

https://m09ic.top/posts/29936/

- battledata 为我爬的几个账号的场次数据
- battledetaildata 为所有场次的详细数据
- img 为生成的图片示例
- data.db为sqlite数据库,保存了清洗入库后的数据
- hero.json 为英雄名字与英雄Id一一对应的数据,翻了半天才找到
- item.json 为装备的详细数据,如果要分析出装,可能用得上.
- main.py是数据分析的脚本
- scrapyspider.py 为scrapy脚本,需要用`scrapy genproject projectname`之后,把这个脚本复制到`spider`目录下运行
- spider 为requests爬虫,可直接运行.

我使用的是anaconda,里面自带了数据分析用的各种库,只需要额外安装一个scrapy.

**代码并不能直接运行,只能用作参考.**