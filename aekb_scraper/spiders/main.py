import scrapy
from datetime import datetime
from time import sleep

#  To start scraper make sure that you have installed latest scrapy library.
#  In aekb_scraper folder from the terminal write on command "scrapy crawl aekb.de -O aekb.json" and wait for json :)
class Spider(scrapy.Spider):
    name = 'aekb.de'
    start_urls = ['https://www.aekb.de/service-kontakt/verzeichnisse/verzeichnis-der-weiterbildungsbefugten?tx_vdinterfaces_authoritieslist%5B__referrer%5D%5B%40extension%5D=VdInterfaces&tx_vdinterfaces_authoritieslist%5B__referrer%5D%5B%40controller%5D=Authority&tx_vdinterfaces_authoritieslist%5B__referrer%5D%5B%40action%5D=list&tx_vdinterfaces_authoritieslist%5B__referrer%5D%5Barguments%5D=YToxMjp7czo0OiJhcmVhIjtzOjA6IiI7czoxODoiYXV0aG9yaXphdGlvbkxldmVsIjtzOjA6IiI7czoxMjoiZmllbGRPZlN0dWR5IjtzOjA6IiI7czoxMDoibmFtZURvY3RvciI7czowOiIiO3M6MjA6Im9yZ2FuaXphdGlvbkxvY2F0aW9uIjtzOjA6IiI7czoxNjoib3JnYW5pemF0aW9uTmFtZSI7czowOiIiO3M6MTY6Im9yZ2FuaXphdGlvblR5cGUiO3M6MDoiIjtzOjE5OiJvcmdhbml6YXRpb25aaXBDb2RlIjtzOjA6IiI7czoxMDoicmVndWxhdGlvbiI7czowOiIiO3M6MjI6InNvcnRieUF1dGhvcml0eVNoYXJpbmciO3M6MDoiIjtzOjEwOiJzb3J0YnlUeXBlIjtzOjA6IiI7czo2OiJzdGF0dXMiO3M6MToiMSI7fQ%3D%3De65c96154237979a7daf79dddbaeb6ee20d14c60&tx_vdinterfaces_authoritieslist%5B__referrer%5D%5B%40request%5D=%7B%22%40extension%22%3A%22VdInterfaces%22%2C%22%40controller%22%3A%22Authority%22%2C%22%40action%22%3A%22list%22%7Dcc82df97e621634bd57e277a807d64b3a0ca4629&tx_vdinterfaces_authoritieslist%5B__trustedProperties%5D=%7B%22nameDoctor%22%3A1%2C%22authorizationLevel%22%3A1%2C%22organizationName%22%3A1%2C%22organizationZipCode%22%3A1%2C%22organizationLocation%22%3A1%2C%22organizationType%22%3A1%2C%22regulation%22%3A1%2C%22area%22%3A1%2C%22status%22%3A1%2C%22fieldOfStudy%22%3A1%2C%22sortbyType%22%3A1%2C%22sortbyAuthoritySharing%22%3A1%7Dc529929da20dc453bb2f239fe151589fa136e0f4&tx_vdinterfaces_authoritieslist%5BnameDoctor%5D=&tx_vdinterfaces_authoritieslist%5BauthorizationLevel%5D=&tx_vdinterfaces_authoritieslist%5BorganizationName%5D=&tx_vdinterfaces_authoritieslist%5BorganizationZipCode%5D=&tx_vdinterfaces_authoritieslist%5BorganizationLocation%5D=&tx_vdinterfaces_authoritieslist%5BorganizationType%5D=&tx_vdinterfaces_authoritieslist%5Bregulation%5D=&tx_vdinterfaces_authoritieslist%5Barea%5D=&tx_vdinterfaces_authoritieslist%5Bstatus%5D=1&tx_vdinterfaces_authoritieslist%5BfieldOfStudy%5D=&tx_vdinterfaces_authoritieslist%5BsortbyType%5D=&tx_vdinterfaces_authoritieslist%5BsortbyAuthoritySharing%5D=']

    def parse(self, response):
        for info_card in response.css('div.vd-result-list__item '):
            try:
                yield {
                    'comment': info_card.xpath('div/div[4]/p//text()').getall()[1].strip('\n').strip(),
                    'subject': info_card.xpath('div/div[1]/p[2]/strong//text()').get(),
                    'name': info_card.xpath('div/div[2]/p[2]/span/strong//text()').get(),
                    'authority_since': info_card.xpath('div/div[3]/p[3]/date//text()').get().strip('\n').strip(),
                    'WBO': info_card.xpath('div/div[1]/p[3]//text()').get(),
                    'duration': info_card.xpath('div/div[3]/p[2]/span/strong//text()').get(),
                    'address': info_card.css('span.address__street::text').get(),
                    'zip': info_card.css('span.address__location::text').get().split()[0],
                    'city': info_card.css('span.address__location::text').get().split()[1],
                    'address_title': info_card.css('span.address__title::text').get(),
                    'clinic_type': info_card.css('span.address__department::text').get(),
                    'import_date': datetime.now(),
                    'import_link': response.request.url
                }
            except IndexError:
                yield {
                    'comment': '',
                    'subject': info_card.xpath('div/div[1]/p[2]/strong//text()').get(),
                    'name': info_card.xpath('div/div[2]/p[2]/span/strong//text()').get(),
                    'authority_since': info_card.xpath('div/div[3]/p[3]/date//text()').get().strip('\n').strip(),
                    'WBO': info_card.xpath('div/div[1]/p[3]//text()').get(),
                    'duration': info_card.xpath('div/div[3]/p[2]/span/strong//text()').get(),
                    'address': info_card.css('span.address__street::text').get(),
                    'zip': info_card.css('span.address__location::text').get().split()[0],
                    'city': info_card.css('span.address__location::text').get().split()[1],
                    'address_title': info_card.css('span.address__title::text').get(),
                    'clinic_type': info_card.css('span.address__department::text').get(),
                    'import_date': datetime.now(),
                    'import_link': response.request.url
                }

        sleep(2)
        try:
            next_page = 'https://www.aekb.de'+response.css('li.next a').attrib['href']
            print(next_page)
            if next_page is not None:
                yield response.follow(next_page, callback=self.parse)
        except KeyError:
            print(input('Press enter to exit...'))

