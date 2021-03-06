import scrapy
from scrapy.selector import *
from scrapy.contrib.spiders import CrawlSpider, Rule
import json
from scrapy.http import Request 
class snap(CrawlSpider):
    name = "hnsnap"
    allowed_domains = ["snapdeal.com"]
    start_urls = []
    items={}	
    def __init__(self, category=None, *args, **kwargs):
        super(snap, self).__init__(*args, **kwargs)
	with open("hn_urls.txt") as f:
		strings=f.readlines()
	for string in strings:
		self.start_urls.append(string)
	print self.start_urls

	self.out=open("hnoutput.txt",'w')
     	self.out.write(str("product|price|SP|value|supc|id|prodid"+'\n'))
	    	
    
    def parse(self, response):
	true=True
	false=False
	hxs=HtmlXPathSelector(response)	
	p=response.request.url
	p=p.split('/')
	#print p
	product=p[4]
	prodid=p[5]
	prodid=prodid[:len(prodid)-3]
	prod=hxs.select('//div[@class="product-attr-outer"]/input/@value').extract()
	if prod!=[]:
		prod=eval(prod[0])
		for pro in prod:
			prurl="http://www.snapdeal.com/acors/json/gvbps?supc="+str(pro["supc"])+"&pc=&catId=322"
			yield Request(url=prurl,callback=self.parse_price,cookies={"supc":pro["supc"],\
"id":pro["id"],"value":pro["value"],"product":product,"prodid":prodid})
	else:
		sprice=hxs.select('//span[@id="selling-price-id"]/text()').extract()
		mrp=hxs.select('//div[@id="mrp-price-outer"]/strike/span/text()').extract()
		self.out.write(product+'|'+str(mrp[0])+'|'+str(sprice[0])+'|'+'-'+'|'+'-'+'|'+'-'+'|'+prodid+'\n')
		
    def parse_price(self,response):
	ck= response.request.cookies
	false=False
	true=True	 		
	data=eval(response.body)
	data=data[0]
	ck["SP"]=data["sellingPrice"]
	ck["Price"]=data["price"]
	print ck["prodid"]	
	self.out.write(ck['product']+'|'+str(ck['Price'])+'|'+str(ck['SP'])+'|'+ck['value']+'|'+ck['supc']+'|'+str(ck['id'])+'|'+str(ck['prodid'])+'\n')
	
