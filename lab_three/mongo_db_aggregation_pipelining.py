import csv

from pymongo import MongoClient
from pymongo.synchronous.collection import Collection
from pymongo.synchronous.command_cursor import CommandCursor
from pymongo.synchronous.cursor import Cursor
from pymongo.synchronous.database import Database


def q_one(business_collection: Collection) -> None:
    aggregate_result: CommandCursor = business_collection.aggregate(
        [
            {
                "$match": {
                    "categories": {
                        "$in": ["Fast Food", "Restaurants"]
                    }
                }
            },
            {
                "$group": {
                    "_id": "$city",
                    "count": {"$sum": 1}
                }
            },
        ]
    )

    file_name: str = "query_results/q_one_results.csv"
    fieldnames: list[str] = ["city", "business_count"]
    with open(file_name, "w", newline="") as csv_file:
        csv_writer: csv.DictWriter = csv.DictWriter(f=csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for document in aggregate_result:
            csv_writer.writerow(
                {
                    "city": document["_id"],
                    "business_count": document["count"],
                }
            )


def q_two(business_collection: Collection) -> None:
    aggregate_result: CommandCursor = business_collection.aggregate(
        [
            {
                "$match": {
                    "review_count": {
                        "$gte": 10
                    }
                }
            },
            {
                "$group": {
                    "_id": {
                        "city": "$city",
                        "stars": "$stars",
                    },
                    "count": {"$sum": 1}
                }
            },
        ]
    )

    file_name: str = "query_results/q_two_results.csv"
    fieldnames: list[str] = ["city", "stars", "business_count"]
    with open(file_name, "w", newline="") as csv_file:
        csv_writer: csv.DictWriter = csv.DictWriter(f=csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for document in aggregate_result:
            csv_writer.writerow(
                {
                    "city": document["_id"]["city"],
                    "stars": document["_id"]["stars"],
                    "business_count": document["count"],
                }
            )


def q_three(business_collection: Collection) -> None:
    aggregate_result: CommandCursor = business_collection.aggregate(
        [
            {
                "$match": {
                    "review_count": {
                        "$gte": 10
                    },
                    "stars": {
                        "$gte": 4
                    }
                }
            },
            {
                "$sort": {
                    "review_count": -1
                }
            },
            {
                "$limit": 10
            }
        ]
    )

    file_name: str = "query_results/q_three_results.csv"
    fieldnames: list[str] = ["_id", "business_id"]
    with open(file_name, "w", newline="") as csv_file:
        csv_writer: csv.DictWriter = csv.DictWriter(f=csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for document in aggregate_result:
            csv_writer.writerow(
                {
                    "_id": document["_id"],
                    "business_id": document["business_id"],
                }
            )


def part_two(business_collection: Collection) -> None:
    aggregate_result: CommandCursor = business_collection.aggregate(
        [
            {
                "$match": {
                    "review_count": {
                        "$gte": 10
                    },
                    "stars": {
                        "$gte": 4
                    }
                }
            },
            {
                "$sort": {
                    "review_count": -1
                }
            },
            {
                "$limit": 10
            },
            {
                "$lookup": {
                    "from": "review",
                    "localField": "business_id",
                    "foreignField": "business_id",
                    "as": "reviews"
                }
            }
        ]
    )

    file_name: str = "query_results/part_two_results.csv"
    fieldnames: list[str] = ["review_id", "business_id", "review_stars", "review_text"]
    with open(file_name, "w", newline="") as csv_file:
        csv_writer: csv.DictWriter = csv.DictWriter(f=csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        for document in aggregate_result:
            for review_document in document["reviews"]:
                csv_writer.writerow(
                    {
                        "review_id": review_document["review_id"],
                        "business_id": review_document["business_id"],
                        "review_stars": review_document["stars"],
                        "review_text": review_document["text"],
                    }
                )


def main() -> None:
    # Create Mongo DB client
    mongodb_client: MongoClient = MongoClient(host='localhost', port=27017)
    # Get lab_three database
    db: Database = mongodb_client['lab_three']
    # Get business collection
    business_collection: Collection = db['business']

    # Create CSV file for Q2_1 results
    q_one(business_collection=business_collection)

    # Create CSV file for Q2_2 results
    q_two(business_collection=business_collection)

    # Create CSV file for Q2_3 results
    q_three(business_collection=business_collection)

    # Create CSV file for part two join results
    part_two(business_collection=business_collection)


if __name__ == '__main__':
    main()
