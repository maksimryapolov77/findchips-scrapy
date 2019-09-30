# -*- coding: utf-8 -*-
import logging
import sleep
from collections import OrderedDict

import scrapy
from bs4 import BeautifulSoup
from scrapy.utils.log import configure_logging
from findchipdetail.items import FindchipdetailItem


class DetailchipinfoSpider(scrapy.Spider):
    name = 'detailchipinfo'
    allowed_domains = ['findchips.com']

    def start_requests(self):
        with open('link.txt') as f:
            start_urls = [url.strip() for url in f.readlines()]
            for url in start_urls:
                self.settings.attributes['COLLECTION'] = url.split('/')[5].replace('%20', ' ').replace('%2F', '_')
                yield scrapy.Request(url=url, callback=self.parse)

    configure_logging(install_root_handler=False)
    logging.basicConfig(
        filename='log.txt',
        format='%(levelname)s: %(message)s',
        level=logging.INFO
    )

    def parse(self, response):
        # generating soup object from response
        soup = BeautifulSoup(response.body, 'html.parser')
        if soup.find(class_='no-match-message'):
            logging.info(f'page count limited {response.url}')
            return
        else:
            field_list = []
            value_list = []
            # getting table element
            table = soup.find(class_='default-table parametric-table')
            # header parsing
            th_elements = table.thead.findAll('tr')[1].findAll('th')
            for idx, th in enumerate(th_elements):
                # field parsing
                field = th.contents
                field_name = ''
                if idx == 3:
                    field_name = 'DataSheet'
                if len(field) != 0:
                    field_name = field[0].replace('\n', '').strip()
                if idx != 0 and idx != 1:
                    field_list.append(field_name.replace('.', ''))
                    if idx == 2:
                        field_list.append('Company')
                    if idx == 3:
                        field_list.append('File_Path')
            field_list.append('MyConnection')
            
            # info parsing
            trs = table.tbody.findAll('tr')
            for index, tr in enumerate(trs):
                tds_elements = tr.findAll('td')
                for idx, td in enumerate(tds_elements):
                    value = ''
                    # normal value parsing
                    if len(td.contents) == 1:
                        value = td.contents[0].replace('\n', '').strip().replace('  ', '')
                    else:
                        # element image link
                        if td.find(class_='j-load-check'):
                            value = td.find(class_='j-load-check')['src']
                        # part-number and company
                        if td.find(class_='catalog-table-part-number'):
                            part_number = td.find(class_='catalog-table-part-number').text
                            value_company = td.find(class_='catalog-table-manu').text
                        # datasheet link
                        if td.find(class_='list-pdf-icon j-datasheet'):
                            value = td.find(class_='list-pdf-icon j-datasheet')['href']
                    if idx != 0 and idx != 1:
                        if idx != 2:
                            value_list.append(value)
                        if idx == 2:
                            value_list.append(part_number)
                            value_list.append(value_company)
                        if idx == 3:
                            url = response.url.split('?')[0].replace('%20', ' ').replace('%2F', '_')
                            value_list.append('/chip/' + url.split('/')[4] + '/' + url.split('/')[5] + '/' + part_number + '.pdf')
                            # value_list.append('/chip/' + url.split('/')[4] + '/' + url.split('/')[4] + ' ' + url.split('/')[5] + '/' + part_number + '.pdf')

                value_list.append(response.url.split('?')[0].replace('%20', ' ').replace('%2F', '_').split('/')[5])
                # filtered_url = response.url.split('?')[0].replace('%20', ' ').replace('%2F', '_')
                # value_list.append(filtered_url.split('/')[4] + ' ' + filtered_url.split('/')[5])

                data = dict(zip(field_list, value_list))
                value_list.clear()

                yield FindchipdetailItem(**data)
            if response.url.find('?sort=Risk%20Rank%20asc&page=') == -1:
                yield scrapy.Request(response.url + '?sort=Risk%20Rank%20asc&page=2', callback=self.parse)
            if response.url.find('?sort=Risk%20Rank%20asc&page=') != -1:
                page_index = int(response.url.split('page=')[1])
                page_index += 1
                yield scrapy.Request(response.url.split('page=')[0] + 'page=' + str(page_index), callback=self.parse)
