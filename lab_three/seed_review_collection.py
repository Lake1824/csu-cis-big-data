import json

from pymongo import MongoClient


def main() -> None:
    # Create Mongo DB client
    mongodb_client: MongoClient = MongoClient(host='localhost', port=27017)
    # Create lab_three DB if it has not been created already
    db = mongodb_client['lab_three']
    # Create review collection if it has not been created already
    collection = db['review']

    # Insert each review JSON
    with open('yelp_data/yelp_academic_dataset_review.json', 'r') as reviews_json_file:
        for raw_review_json in reviews_json_file:
            review: dict = json.loads(raw_review_json)

            collection.insert_one(document=review)


if __name__ == '__main__':
    main()
