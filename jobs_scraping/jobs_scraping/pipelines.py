# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import duckdb
from itemadapter import ItemAdapter


class DuckDbPipeline:
    collection_name = "jobs_items"

    def __init__(self, db_path) -> None:
        self.db_path = db_path
        self.conn = None

    @classmethod
    def from_crawler(cls, crawler):
        db_path = crawler.settings.get("DUCKDB_PATH", "jobs.duckdb")
        return cls(db_path)

    def open_spider(self, spider):
        self.conn = duckdb.connect(self.db_path)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                company_name TEXT,
                job_title TEXT,
                location TEXT,
                salary TEXT,
                tech_stack TEXT[],
                listing_url TEXT,
                description TEXT,
                date_posted DATE
            )
                          """)

    def process_item(self, item, spider):
        self.conn.execute(
            """
            INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                          """,
            (
                item.get("company_name"),
                item.get("job_title"),
                item.get("location"),
                item.get("salary"),
                item.get("tech_stack"),
                item.get("listing_url"),
                item.get("description"),
                item.get("date_posted"),
            ),
        )
        return item

    def close_spider(self, spider):
        self.conn.close()
