#!/usr/bin/python
# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy_splash import SplashRequest

script = """
local treat = require('treat')

function main(splash)
  local url = splash.args.url
  assert(splash:go(url))
  assert(splash:wait(2))
  local element = splash:select('.news-list')
  local newsList = element.outerHTML
  local aList = splash:select_all('.news-list li>div.txt-box>h3>a')
  local hrefs = {}

  for _, a in ipairs(aList) do
    hrefs[#hrefs+1] = a.node.attributes.href
  end

  return treat.as_array(hrefs)
end
"""

class ShareditorSpider(scrapy.Spider):
    name = "dashujuwenzhai"
    allowed_domains = ["qq.com"]
    start_urls = [
        "http://weixin.sogou.com/"
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                endpoint='execute',
                args={
                    'lua_source': script
                }
            )

    def parse(self, response):
        print response.body
        newsListHrefs = json.loads(response.body)
        for href in newsListHrefs:
            print href
            yield scrapy.Request(href, callback=self.parse_profile)

    def parse_profile(self, response):
        print response.body
