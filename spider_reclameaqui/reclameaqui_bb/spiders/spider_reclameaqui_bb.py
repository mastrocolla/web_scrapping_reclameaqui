import scrapy
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait 

class ReclameaquiBbSpider(scrapy.Spider):
    name = 'spider_reclameaqui_bb'

#   --- Insira o número de páginas que gostaria de raspar
    pages_wanted = 10
    
    start_urls = (f'https://www.reclameaqui.com.br/empresa/banco-do-brasil/lista-reclamacoes/?pagina={i}&status=EVALUATED' for i in range(1, pages_wanted + 1))


    def parse(self, response):

        self.driver = webdriver.Edge('C:\\Users\\mvtm8\\AppData\\Local\\edgedriver_win64\\msedgedriver.exe')
        self.wait = WebDriverWait(self.driver, 10)
        
        self.driver.get(response.url)
        page = self.driver.page_source

        new = scrapy.Selector(text = page)

        for link in new.xpath('//div[@class="sc-1pe7b5t-0 bJdtis"]/a').xpath('@href').getall():

            main_url = 'https://www.reclameaqui.com.br'
            complaint_url = main_url + link
            yield scrapy.Request(complaint_url, callback=self.get_text)


    def get_text(self, response):
        title = response.xpath('//div[@class="lzlu7c-19 hpNFPP"]/h1/text()').getall()

        content = response.xpath('//p[@class="lzlu7c-17 fXwQIB"]/text()').getall()
        
        
        yield {
            'title' : title,
            'content': content,
            }