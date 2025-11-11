import scrapy


class JobsSpider(scrapy.Spider):
    name = "jobs"

    async def start(self):
        urls = [
            "https://dev.bg/company/jobs/python/",
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url
        self.log(f"Crawled {page}")

        for listing in response.css("div.job-list-item"):
            yield {
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
            }
