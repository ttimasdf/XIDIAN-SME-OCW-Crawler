# XIDIAN-SME-OCW-Crawler

西安电子科技大学微电子学院公开课爬虫。

target url: https://sme.xidian.edu.cn/html/bkjj/zxkt/

## Usage

安装依赖。获取URL，以《半导体物理II》课程为例，先点击到第二页，复制URL。

URL为 `https://sme.xidian.edu.cn/html/bkjj/zxkt/bdtwl2/list_93_2.html` 将路径末尾的 `_2` 替换为 `_{}` ，并人工指定页码（我懒得写了）。

```bash
pip install scrapy
cd xdvideo
scrapy crawl xdvideo -a url="https://sme.xidian.edu.cn/html/bkjj/zxkt/bdtwl2/list_93_{}.html" -a pages=4
```

输出目录： `./output`
