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
                date_posted DATE,
                categories TEXT[],
                company_activity TEXT,
                company_sector TEXT,
                company_central_office TEXT,
                company_creation_date TEXT,
                number_employees TEXT,
                implemented_in_bulgaria_date TEXT,
                number_employees_in_bulgaria TEXT,
                offices_in_bulgaria TEXT,
                it_employees_in_bulgaria TEXT,
                date_scraped DATE)
                          """)

    def process_item(self, item, spider):
        self.conn.execute(
            """
            INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
                item.get("categories"),
                item.get("activity"),
                item.get("sector"),
                item.get("central_office"),
                item.get("creation_date"),
                item.get("number_employees"),
                item.get("implemented_in_bulgaria_date"),
                item.get("number_employees_bulgaria"),
                item.get("offices_in_bulgaria"),
                item.get("it_employees_in_bulgaria"),
                item.get("date_scraped"),
            ),
        )
        return item

    def close_spider(self, spider):
        self.conn.close()
