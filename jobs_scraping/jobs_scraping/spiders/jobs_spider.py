import scrapy
from datetime import datetime


class JobsSpider(scrapy.Spider):
    name = "jobs"
    allowed_domains = ["dev.bg"]

    def parse_homepage(self, response):
        category_links = response.css("a.show-all-jobs-cat::attr(href)").getall()

        for url in category_links:
            yield scrapy.Request(
                url=response.urljoin(url),
                meta={"playwright": True, "playwright_context": "default"},
                callback=self.parse,
            )

    def start_requests(self):
        yield scrapy.Request(
            "https://dev.bg",
            meta={"playwright": True, "playwright_context": "default"},
            callback=self.parse_homepage,
        )

    def parse_company(self, response):
        item = response.meta["item"]

        company_info = response.css("div.company-info-1 p.p-big-16::text").getall()
        secondary_company_info = response.css(
            "div.company-info p.p-big-18::text"
        ).getall()

        if len(company_info) >= 3:
            item["activity"] = company_info[0]
            item["sector"] = company_info[1]
            item["central_office"] = company_info[2]

        if len(secondary_company_info) >= 6:
            item["creation_date"] = secondary_company_info[0]
            item["number_employees"] = secondary_company_info[1]
            item["implemented_in_bulgaria_date"] = secondary_company_info[2]
            item["number_employees_bulgaria"] = secondary_company_info[3]
            item["offices_in_bulgaria"] = secondary_company_info[4]
            item["it_employees_in_bulgaria"] = secondary_company_info[5]

        yield item

    def parse_listing(self, response):
        item = response.meta["item"]

        item["description"] = response.css("div.job_description").get()
        item["date_posted"] = response.css("li.date-posted time::attr(datetime)").get()
        item["categories"] = response.css("a.pill::text").getall()

        company_url = response.css("a.company-logo-link::attr(href)").get()

        if company_url is not None:
            yield scrapy.Request(
                url=response.urljoin(company_url),
                callback=self.parse_company,
                meta={
                    "item": item,
                    "playwright": True,
                    "playwright_context": "default",
                },
            )
        else:
            yield item

    def parse(self, response):
        page = response.url
        self.log(f"Crawled {page}")

        base_item = {
            "company_name": None,
            "job_title": None,
            "location": None,
            "salary": None,
            "tech_stack": None,
            "listing_url": None,
            "description": None,
            "date_posted": datetime.now().date(),
            "categories": None,
            "date_scraped": datetime.now().date(),
            # Company info defaults:
            "activity": None,
            "sector": None,
            "central_office": None,
            "creation_date": None,
            "number_employees": None,
            "implemented_in_bulgaria_date": None,
            "number_employees_bulgaria": None,
            "offices_in_bulgaria": None,
            "it_employees_in_bulgaria": None,
        }

        for listing in response.css("div.job-list-item"):
            item = base_item.copy()
            listing_url = listing.css("a.overlay-link::attr(href)").get()
            item["company_name"] = listing.css("span.company-name::text").get()
            item["job_title"] = listing.css("h6.job-title::text").get()
            item["location"] = listing.xpath(
                "normalize-space(.//span[contains(@class, 'badge')])"
            ).get()
            item["salary"] = listing.xpath(
                "normalize-space(.//span[contains(@class, 'blue')])"
            ).get()
            item["tech_stack"] = listing.css(
                "div.tech-stack-item img::attr(title)"
            ).getall()
            item["listing_url"] = listing_url

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
                next_page,
                meta={"playwright": True, "playwright_context": "default"},
                callback=self.parse,
            )
