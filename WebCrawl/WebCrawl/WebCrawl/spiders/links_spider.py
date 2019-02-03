import scrapy
from scrapy.linkextractor import LinkExtractor
from scrapy.spiders import Rule, CrawlSpider
from tutorial.items import ScraperItem
#Code Reference : https://www.data-blogger.com/2016/08/18/scraping-a-website-with-python-scrapy/

start_url = "https://www.claytonhotelgalway.ie/" #Change the link details depending on the hotel to be crawled
allowed_domain = "claytonhotelgalway.ie" # Change the domain name depending on the hotel website to crawl
class DatabloggerSpider(CrawlSpider):
	# The name of the spider
	name = "weblinks"

	# The domains that are allowed. This part needs to be changed depending on the hotel links defined below.
	allowed_domains = [allowed_domain]

	# The URLs to start with
	# https://www.galwaybayhotel.net/
	# https://www.claytonhotelgalway.ie/
	start_urls = [start_url]

	custom_settings = {
    # specifies exported fields and order
    'FEED_EXPORT_FIELDS': ["url_from", "url_to","name","type"],
  	}


	# This spider has one rule: extract all (unique and canonicalized) links, 
    # follow them and parse them using the parse_items method
	rules = [
		Rule(
			LinkExtractor(
				canonicalize=True,
				unique=True
			),
			follow=True,
			callback="parse_items"
		)
	]

	

	# In the following method we have written down the code which will be used to parse the total data to write down the data in excel format
	#We have extracted all the links in the following part where internal links and external links are getting extracted.
	#In the code we have also checked the following part where we have checked if the link is external link then we have extracted till the part of link domain
	def parse_items(self, response):
		# The list of items that are found on the particular page
		SET_SELECTOR = '.set'
		items = []
		# Here we have extracted the links that are related to the page that we want to crawl
		links = LinkExtractor(canonicalize=True, unique=True).extract_links(response)

        # Traverse all the links in the page
		for link in links :

			item = ScraperItem()
			
            #Initialise the items
			item['url_from'] = response.url # Update URL From
			item['url_to'] = link.url
			item['name'] = str.strip(link.text)
			item['type'] = ""
			
            # Update the Type as Internal or External Link
			if(not item['url_to'].startswith(start_url)):
				item['type'] = "External Link"
			else:
				item['type'] = "Internal Link"

			# Strip the title
			title = str.strip(response.css('title::text').get())
			
			# Check if name or Title as blank
			if((item['name'] == "") and  (title == "")):
				if(item['url_to'].startswith(start_url)):
					c = item['url_to'].count('/')
					item['name'] = item['url_to'].rsplit('/',c-1)[0]
				else :
					item['name'] = "External Link"
			# Update the name with title
			elif(item['name'] == ""):
				item['name'] = title

            # Update the URL To
			for i in item['url_to']:
				if (not item['url_to'].startswith(start_url)):
					c = item['url_to'].count('/')
					item['url_to'] = item['url_to'].rsplit('/',c-2)[0]
			items.append(item)
		# Return all the found items
		return items
