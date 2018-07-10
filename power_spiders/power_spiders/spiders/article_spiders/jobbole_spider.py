"""
@file: jobbole_spider.py
@brief: 伯乐在线博客网站爬虫
@author: feihu1996.cn
@date: 18-7-10 下午10:47
@version: 1.0
"""

from urllib.parse import urljoin

import scrapy

from power_spiders.items import ArticleSpiderItem, ArticleSpiderItemLoader


class JobboleSpider(scrapy.Spider):
    name = 'jobbole_spider'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        # 自动翻页
        page_url = response.css('a.next.page-numbers::attr(href)').extract_first()
        if page_url:
            yield response.follow(url=page_url, callback=self.parse)

        # 爬取当前页面上每一篇文章
        post_nodes = response.xpath('//div[@class="post floated-thumb"]/div[@class="post-thumb"]/a')
        for post_node in post_nodes:
            post_image = post_node.xpath('img/@src').extract_first()
            if post_image:
                post_image = urljoin(response.url, post_image)
            post_url = post_node.xpath('@href').extract_first()
            yield response.follow(url=post_url, meta={'post_image': post_image} , callback=self.parse_detail)

    @staticmethod
    def parse_detail(response):
        item = ArticleSpiderItem()

        """
        # 文章标题
        post_title = ''.join(response.xpath("//div[@class='entry-header']/h1/text()").extract())
        # title = response.css("div.entry-header h1::text").extract_first()
        post_title = re.sub('\s', '', post_title)
        print('post_title:' + post_title)

        # 发表时间
        create_time = ''.join(response.xpath('//p[@class="entry-meta-hide-on-mobile"]/text()').extract())
        # createTime = response.css('p.entry-meta-hide-on-mobile::text').extract_first()
        create_time = re.sub('\s|\·|,', '', create_time)
        print('create_time:' + create_time)
        try:
            create_time = datetime.datetime.strptime(create_time, "%Y/%m/%d").date()
        except:
            create_time = datetime.datetime.now().date()

        # 点赞数
        praise_nums = ''.join(response.xpath('//span[@class=" btn-bluet-bigger href-style vote-post-up   register-user-only "]/h10/text()').extract())
        # praiseNums = response.css('span.vote-post-up h10::text').extract_first()
        praise_nums = re.sub('\s', '', praise_nums)
        if praise_nums:
            praise_nums = int(praise_nums)
        else:
            praise_nums = 0
        print('praiseNums:' + str(praise_nums))

        # 收藏数
        fav_nums = ''.join(response.xpath('//span[@class=" btn-bluet-bigger href-style bookmark-btn  register-user-only "]/text()').extract())
        # favNums = response.css('span.bookmark-btn::text').extract_first()
        fav_nums = re.sub('\s|(收藏)', '', fav_nums)
        if fav_nums:
            fav_nums = int(fav_nums)
        else:
            fav_nums = 0
        print('fav_nums:' + str(fav_nums))

        # 评论数
        comment_nums = ''.join(response.xpath('//span[@class="btn-bluet-bigger href-style hide-on-480"]/text()').extract())
        # commentNums = response.css('a[href="#article-comment"] span::text').extract_first()
        comment_nums = re.sub('\s|(评论)', '', comment_nums)
        if comment_nums:
            comment_nums = int(comment_nums)
        else:
            comment_nums = 0
        print('comment_nums:' + str(comment_nums))

        # 文章标签
        post_tag = response.xpath('//p[@class="entry-meta-hide-on-mobile"]/a/text()').extract()
        # tag = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        post_tag = ','.join(post_tag) if len(post_tag) > 1 else ''.join(post_tag)
        post_tag = re.sub('\s', '', post_tag)
        print('post_tag:' + post_tag)

        # 文章内容
        post_content = ''.join(response.xpath('//div[@class="entry"]').extract())
        # content = response.css('div.entry').extract_first()
        post_content = re.sub('\s', '', post_content)
        print('post_content:' + post_content)

        # 封面图片
        post_image = response.meta.get('post_image')
        print('post_image:' + post_image)

        # url md5 hash
        url_object_id = get_md5(response.url)
        print('url_object_id:' + url_object_id)

        item['post_title'] = post_title
        item['create_time'] = create_time
        item['praise_nums'] = praise_nums
        item['fav_nums'] = fav_nums
        item['comment_nums'] = comment_nums
        item['post_tag'] = post_tag
        item['post_content'] = post_content
        item['post_image'] = [post_image]
        item['url_object_id'] = url_object_id
        item['post_url'] = response.url
        """

        item_loader = ArticleSpiderItemLoader(item, response)

        # 文章标题
        item_loader.add_xpath("post_title", "//div[@class='entry-header']/h1/text()")

        # 发表时间
        item_loader.add_xpath("create_time", '//p[@class="entry-meta-hide-on-mobile"]/text()')

        # 点赞数
        item_loader.add_css('praise_nums', 'span.vote-post-up h10::text')

        # 收藏数
        item_loader.add_css('fav_nums', 'span.bookmark-btn::text')

        # 评论数
        item_loader.add_css('comment_nums', 'a[href="#article-comment"] span::text')

        # 文章标签
        item_loader.add_css('post_tag', 'p.entry-meta-hide-on-mobile a::text')

        # 文章内容
        item_loader.add_css('post_content', 'div.entry')

        # 封面图片
        item_loader.add_value('post_image', [response.meta.get('post_image', '')])

        # url md5 hash
        item_loader.add_value('url_object_id', response.url)

        # 文章网址
        item_loader.add_value('post_url', response.url)

        item = item_loader.load_item()

        yield item
