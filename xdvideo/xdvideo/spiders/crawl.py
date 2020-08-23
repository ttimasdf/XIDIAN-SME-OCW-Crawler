import scrapy
from scrapy.http import Request, Response

from xdvideo.items import XdvideoItem

class CrawlSpider(scrapy.Spider):
    name = 'xdvideo'
    allowed_domains = ['sme.xidian.edu.cn']

    VIDEOS_PER_PAGE = 15
    # start_urls = [f'https://sme.xidian.edu.cn/html/bkjj/zxkt/bdtwl1/list_92_{i}.html' for i in range(1, 4)]
    def __init__(self, url="https://sme.xidian.edu.cn/html/bkjj/zxkt/bdtwl1/list_92_{}.html", pages=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.url = url
        self.pages = int(pages)

    def start_requests(self):
        for i in range(1, self.pages + 1):
            yield Request(self.url.format(i), meta={"page": i})

    def parse(self, response: Response):
        XPATH_URL = "//body//div[@class='childinfo']//div//div[*]//a[1]/@href"
        urls = response.xpath(XPATH_URL).getall()
        
        for i in range(len(urls)):
            yield response.follow(urls[i], callback=self.parse_detail,
                meta = {"n": (response.meta["page"] - 1) * self.VIDEOS_PER_PAGE + i + 1})
    
    def parse_detail(self, response: Response):
        XPATH_TITLE = "//div[@class='text']//h4[1]/text()"
        XPATH_COURSE = "//div[@class='childtitle']//p/text()"
        XPATH_VIDEO = "//video/@src"
        title = response.xpath(XPATH_TITLE).get()
        course = response.xpath(XPATH_COURSE).get()
        video_url = response.urljoin(response.xpath(XPATH_VIDEO).get())
        return XdvideoItem(title=title, course=course, file_urls=[video_url], episode=response.meta["n"])
