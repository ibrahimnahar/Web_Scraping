# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        lowercase_keys = ["category", "product_type"]
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()

        price_keys = ["price", "price_excl_tax", "price_incl_tax", "tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace("£", "")
            adapter[price_key] = float(value)

        availability_string = adapter.get("availability")
        split_string_array = availability_string.split("(")
        if len(split_string_array) < 2:
            adapter["availability"] = 0
        else:
            availability_array = split_string_array[1].split(" ")
            adapter["availability"] = int(availability_array[0])

        num_reviews_string = adapter.get("num_reviews")
        adapter["num_reviews"] = int(num_reviews_string)

        stars_rating = adapter.get("stars")
        stars_rating_split = stars_rating.split(" ")
        if stars_rating_split[1].lower() == "zero":
            adapter["stars"] = 0
        elif stars_rating_split[1].lower() == "one":
            adapter["stars"] = 1
        elif stars_rating_split[1].lower() == "two":
            adapter["stars"] = 2
        elif stars_rating_split[1].lower() == "three":
            adapter["stars"] = 3
        elif stars_rating_split[1].lower() == "four":
            adapter["stars"] = 4
        else:
            adapter["stars"] = 5

        return item


import mysql.connector


class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host="localhost", user="root", password="#", database="books"
        )
        self.cur = self.conn.cursor()

        self.cur.execute(
            """
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment,
            url VARCHAR(255),
            title text,
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            availability INTEGER,
            tax DECIMAL,
            price DECIMAL,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """
        )

    def process_item(self, item, spider):
        self.cur.execute(
            """ insert into `books`(
            url,
            title,
            product_type,
            price_excl_tax,
            price_incl_tax,
            availability,
            tax,
            num_reviews,
            stars,
            category,
            price,
            description
            )values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""",
            (
                item["url"],
                item["title"],
                item["product_type"],
                item["price_excl_tax"],
                item["price_incl_tax"],
                item["availability"],
                item["tax"],
                item["num_reviews"],
                item["stars"],
                item["category"],
                item["price"],
                str(item["description"][0]),
            ),
        ),

        self.conn.commit()
        return item

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()
