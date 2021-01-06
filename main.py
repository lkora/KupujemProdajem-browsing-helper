import scrapy as sc

class KPSpider(sc.Spider):
    name = "item_scraper"
    allowed_domains = ["www.kupujemprodajem.com"]
    start_urls = ["https://www.kupujemprodajem.com/", "https://www.kupujemprodajem.com/search.php?action=list&data[action]=list&data[submit][search]=Tra%C5%BEi&data[dummy]=name&data[page]=4&data[prev_keywords]=macbook&data[keywords]=macbook&data[list_type]=search"]

    rules = (
        
    )

    def parse(self, response):
        ITEM_SELECTOR = ".item"
        for item in response.css(ITEM_SELECTOR):
            # AD_NAME_SELECTOR = ".adName"
            AD_NAME_SELECTOR = ".adName ::text"
            AD_DESCRIPTION_SELECTOR = ".adDescription ::text"
            AD_IMAGE_SELECTOR = ".adImgWrapper img ::attr(src)"
            AD_LINK_SELECTOR = ".imgAndBlurHolder a ::attr(href)"
            AD_PRICE_SELECTOR = ".adPrice ::text"
            yield {
                "name": item.css(AD_NAME_SELECTOR).extract_first(), 
                "description": item.css(AD_DESCRIPTION_SELECTOR).extract_first(), 
                "image": item.css(AD_IMAGE_SELECTOR).extract_first(), 
                "link": item.css(AD_LINK_SELECTOR).extract_first(), 
                "image": item.css(AD_IMAGE_SELECTOR).extract_first(), 
                "price": item.css(AD_PRICE_SELECTOR).extract_first(),
            }

        # Fix next page loading
        NEXT_PAGE_SELECTOR = ".pagesList li a ::attr(href)"
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_last()
        
        if next_page:
            yield sc.Request(
                response.urljoin(next_page),
                callback=self.parse
            )
            
