import scrapy
from datetime import datetime


class JobsSpider(scrapy.Spider):
    name = "jobs"

    async def start(self):
        urls = [
            "https://dev.bg/company/jobs/python/",
        ]

        for url in urls:
            yield scrapy.Request(
                url=url, meta={"playwright": True}, callback=self.parse
            )

    async def parse_listing(self, response):
        item = response.meta["item"]

        item["description"] = response.css("div.job_description").get()
        item["date_posted"] = response.css("li.date-posted time::attr(datetime)").get()

        yield item

    def parse(self, response):
        page = response.url
        self.log(f"Crawled {page}")

        for listing in response.css("div.job-list-item"):
            listing_url = listing.css("a.overlay-link::attr(href)").get()
            item = {
                "company-name": listing.css("span.company-name::text").get(),
                "job_title": listing.css("h6.job-title::text").get(),
                "location": listing.xpath(
                    "normalize-space(.//span[contains(@class, 'badge')])"
                ).get(),
                "salary": listing.xpath(
                    "normalize-space(.//span[contains(@class, 'blue')])"
                ).get(),
                "tech_stack": listing.css(
                    "div.tech-stack-item img::attr(title)"
                ).getall(),
                "listing_url": listing_url,
                "date_scraped": datetime.now().date(),
            }

            if listing_url is not None:
                yield scrapy.Request(
                    url=response.urljoin(listing_url),
                    callback=self.parse_listing,
                    meta={"item": item},
                )
            else:
                yield item

        next_page = response.css("a.facetwp-page.next::attr(data-page)").get()

        if next_page is not None:
            next_page = response.urljoin(f"?_paged={next_page}")
            print(next_page)
            yield scrapy.Request(
                next_page, meta={"playwright": True}, callback=self.parse
            )
