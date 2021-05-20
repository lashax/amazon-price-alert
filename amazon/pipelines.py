from datetime import datetime

import pymongo
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

from amazon.user_input import MONGO_URI, MONGO_DATABASE, COLLECTION


class AmazonPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        mongo_id = adapter.get('_id')
        if not mongo_id:
            raise DropItem(f'Page has not been loaded correctly for {item}')

        for field in adapter:
            adapter[field] = adapter.get(field).strip()
        return item


class MongoPipeline:
    collection_name = COLLECTION

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=MONGO_URI,
            mongo_db=MONGO_DATABASE
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        mongo_id = adapter.get('_id')
        inside_db = self.db[self.collection_name].find_one({'_id': mongo_id})
        if inside_db:
            new_price = adapter.get('price')
            current_price = self.db[self.collection_name].find_one({'_id': mongo_id})['price']

            if new_price != current_price:
                self.db[self.collection_name].update_one(
                    {'_id': mongo_id}, {"$set": {'price': new_price, 'last price':
                        current_price, 'price updated': datetime.now()}})
                print(f"Price for {adapter.get('name')} has been updated on {datetime.now()}")
        else:
            self.db[self.collection_name].insert_one(ItemAdapter(item).asdict())
        return item
