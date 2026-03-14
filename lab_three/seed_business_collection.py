import json

from pymongo import MongoClient


def main() -> None:
    # Create Mongo DB client
    mongodb_client: MongoClient = MongoClient(host='localhost', port=27017)
    # Create lab_three DB if it has not been created already
    db = mongodb_client['lab_three']
    # Create business collection if it has not been created already
    collection = db['business']

    with open('yelp_data/yelp_academic_dataset_business.json', 'r') as businesses_json_file:
        for raw_business_json in businesses_json_file:
            business: dict = json.loads(raw_business_json)

            collection.insert_one(document=business)


if __name__ == '__main__':
    main()
