import scrapy

class VehiclesspiderSpider(scrapy.Spider):
    name = 'vehiclesspider'
    start_urls = ['http://www.gotoauto.ca/inventory/']

    def parse(self, response):
        # the class li contained a class called vehicle-item
        vehics = response.xpath("//li[contains(@class,'vehicle-item')]")

        # the vehicle-item class contains the make, model and price of all the vehicles in the inventory
        for vehic in vehics:
            yield {
                'make': vehic.xpath('.//@data-make').get(),
                'model': vehic.xpath('.//@data-model').get(),
                'price': vehic.xpath('.//div[@class="price_holder "]/span[@class="price"]/text()').get()
            }
        # this is used to naavigate to the next page in the inventory based on the currently active page
        next_page = response.xpath(
            "//ul[@class='pagination']/li[contains(@class,'active')]/following-sibling::li/a/@href").get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)