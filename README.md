# 爬取豆瓣T250
python爬虫 豆瓣电影T250 不断改进的过程~

## 2019.11.4 
  ### Debug总结：
- 1.因为是在介绍页进行提取，因此会发生导演名称缺省的问题，还有一些法文或者印度语之类的情况，不能被正则表达式匹配到...
- 2.中文导演名的正则表达式r'[\u4e00-\u9fa5]+·*[\u4e00-\u9fa5]*'
- 3、英文会出现/xa00这种情况，不能被写入文件
  ### 修改：
- 中文部分的修改：进入介绍页的具体电影链接href，爬取导演名或者演员名
- 代码文件为crawdouban_ch.py
