
import scrapy
from qiubai.items import QiubaiItem


class qiubaiSpider(scrapy.Spider):

    name = 'qiubai'
    start_urls = ["http://www.qiushibaike.com/text/"]
    allowed_domains = ["qiushibaike.com"]

    def parse(self,response):
        pattern1 = "//div[@class='article block untagged mb15']"
        author_pattern = "./div[@class='author clearfix']/a[2]/h2/text()"
        content_pattern = "./div[@class='content']/text()"

        for block in response.xpath(pattern1):
            #print("block",block.extract())
            item = QiubaiItem()
            author = block.xpath(author_pattern).extract()[0] if block.xpath(author_pattern).extract() else ""
            content = block.xpath(content_pattern).extract()[0] if block.xpath(content_pattern) else ""
            item["author"] = author
            item["content"] = content

            href = block.xpath(".//span[@class='stats-comments']/a/@href").extract()[0] if block.xpath(".//span[@class='stats-comments']/a/@href") else ""
            #print("href:",href)
            comment_href = response.urljoin(href)
            req = scrapy.http.Request(comment_href,callback = self.parseComment)
            req.meta["item"] = item
            yield req

        pattern_nextpage = "//ul[@class='pagination']/li[2]/a/@href"
        s = response.xpath(pattern_nextpage).extract()[0][-7:]
        for i in range(2,36):
            next_page = "http://www.qiushibaike.com/text/page/%s?s=%s" %(i,s)
            req_next = scrapy.http.Request(next_page,callback = self.parse_otherPage)
            yield req_next

    def parse_otherPage(self, response):
        pattern1 = "//div[@class='article block untagged mb15']"
        author_pattern = "./div[@class='author clearfix']/a[2]/h2/text()"
        content_pattern = "./div[@class='content']/text()"

        for block in response.xpath(pattern1):
            # print("block",block.extract())
            item = QiubaiItem()
            author = block.xpath(author_pattern).extract()[0] if block.xpath(author_pattern).extract() else ""
            content = block.xpath(content_pattern).extract()[0] if block.xpath(content_pattern) else ""
            item["author"] = author
            item["content"] = content

            href = block.xpath(".//span[@class='stats-comments']/a/@href").extract()[0] if block.xpath(
                ".//span[@class='stats-comments']/a/@href") else ""
            # print("href:",href)
            comment_href = response.urljoin(href)
            req = scrapy.http.Request(comment_href, callback=self.parseComment)
            req.meta["item"] = item
            yield req

    def parseComment(self,response):
        item = response.meta["item"]

        comments = []
        for block in response.xpath("//div[starts-with(@class,'comment-block clearfix floor')]"):
            author = block.xpath("./div[2]/a/text()").extract()[0] if block.xpath("./div[2]/a/text()") else ""
            #author = author.decode('unicode-escape').encode('ascii','ignore')
            comment = block.xpath("./div[2]/span/text()").extract()[0] if block.xpath("./div[2]/span/text()") else ""
            comments.append({"comment_author":author,"comment_content":comment})
        item["comment"] = comments
        yield item






