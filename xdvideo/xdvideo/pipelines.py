# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

import logging

from scrapy.http import Request
from scrapy.pipelines.files import FilesPipeline
from itemadapter import ItemAdapter
from xdvideo.items import XdvideoItem

class XdvideoPipeline(FilesPipeline):
    _l = logging.getLogger(__name__)
    _l.setLevel(logging.DEBUG)

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        # self._l.debug(item)
        for file_url in adapter["file_urls"]:
            yield Request(file_url, meta={"item": item})

    def file_path(self, request, response=None, info=None):
        item = request.meta["item"]
        self._l.debug("file_path request %s, response %s, meta %s", request, response, request.meta["item"])
        try:
            extension = request.url.rsplit('.', maxsplit=1)[-1]
            path = f"{item['course']}/[{item['episode']:02d}]{item['title']}.{extension}"
            self._l.debug("file_path target: %s", path)
            return path
        except Exception as e:
            self._l.debug("file_path Exception: %s, %s", e, str(e))

