# -*- coding: utf-8 -*-
import scrapy
import datetime
import os
from string import Template

""" A Scrapy spider that crawls informations from mql5.com.

The spider goes through all pages that are listed in the 
function list at: https://www.mql5.com/en/docs/function_indices.
The information in this pages are used to generate the Mql5 code
snippets for Sublime Text 3.
"""
class Mql5SnippetSpider(scrapy.Spider):
    name = "snippet_spider"
    allowed_domains = ['mql5.com']
    start_urls = ['https://www.mql5.com/en/docs/function_indices']
    custom_settings = {
        'DOWNLOAD_DELAY': 7.5   # Without a delay we are banned after 100 pages
    }

    """
    Default callback function that will be called by the Scrapy framework
    when the function_indices page was requested and downloaded. The given
    response parameter can be used to search through the page via xpath or
    css selectors.
    """
    def parse(self, response):
        # By now we have downlaoded the function_indices page.
        # We search for all functions that are listed in the main table of
        # the function_indices page. Each row contains a link to the details
        # page of one of this functions.
        # First row of the table contains the table header, therefore we 
        # start at position()>1.
        for row in response.xpath('//div/table/tr[position()>1]'):
            next_function_url = row.xpath('.//td[1]/p/span/a/@href').get()
            next_function_name = row.xpath('.//td[1]/p/span/a/text()').get()
            if next_function_url is not None:
                # We have found a link for a function details page.
                next_function_url = response.urljoin(next_function_url)
                callback_args = {
                'cur_function': next_function_name.encode('utf-8')
                }
                # Now crawl the details page
                yield scrapy.Request(next_function_url, dont_filter=True, callback=self.parse_details_page, cb_kwargs=callback_args)

    """
    Callback function that will be called when a function details page
    was requested and downloaded.

    Parses the details page and generates one .sublime-snippet file.
    The details that are collected are:
    1. Description of the function
    2. Function name
    3. Parameters

    The cur_function parameter contains the title of the link that lead to
    this details page. This is used as tabTrigger in the snippet file and may
    differ from the real function name in some cases. For example MathAbs and fabs,
    both uses MathAbs as function name but the later uses fabs as tabTrigger.
    """
    def parse_details_page(self, response, cur_function):
        description = response.xpath('//p[@class="p_Function"][1]/span/text()').getall()
        codeexample = response.xpath('//div[1]/table[1]//p[@class="p_CodeExample"][1]')
        function_name = codeexample.xpath('./span[@class="f_Functions" or @class="f_Indicators"]/text()').get().encode('utf-8')
        function_params = codeexample.xpath('./span[@class="f_Param"]/text()').getall()

        # Prepare params to match a format like ${1:param}, ${2:param2}
        for i, value in enumerate(function_params):
            function_params[i] = "${%i:%s}" % (i+1, function_params[i].encode('utf-8'))

        if len(function_params) > 1:
            function_params = ', '.join(map(str, function_params))
        elif len(function_params) == 1:
            function_params = function_params[0]
        else:
            function_params = ''

        for i, value in enumerate(description):
            description[i] = description[i].encode('utf-8')

        if(len(description) > 1):
            description = ''.join(map(str, description))
        elif(len(description) == 1):
            description = description[0]
        else:
            description = ''

        f = {
        'time': datetime.datetime.now(),
        'description': description,
        'function_name': function_name,
        'function_params': function_params,
        'tab_trigger': cur_function
        }
        # Read the snippet template file
        template_file = open('template.txt', 'r')
        src = Template(template_file.read())
        template_file.close()

        # Write and put snippet file into appropiate directory
        dir_name = cur_function[0].upper()
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        output_file = open(dir_name + '/' + cur_function +'.sublime-snippet', 'w')
        output_file.write(src.substitute(f))
        output_file.close()
