from datetime import datetime

from outscraper import ApiClient

from app import db
from app.models import Review

client = ApiClient("KEY") #TODO: Change api key


def get_google_reviews(cutoff: datetime = None):
    result = client.google_maps_business_reviews(
        "https://www.google.com/maps/place/%D0%90%D1%82%D0%BC%D0%BE%D1%81%D1%84%D0%B5%D1%80%D0%B0+%D0%BA%D0%BE%D0%BC%D1%84%D0%BE%D1%80%D1%82%D0%B0/@55.5474282,37.0474304,14z/data=!4m8!1m2!2m1!1z0LDRgtC80L7RgdGE0LXRgNCwINC60L7QvNGE0L7RgNGC0LA!3m4!1s0x46caa848716b815d:0x69a92c94c9079ef9!8m2!3d55.5474282!4d37.0649399",
        cutoff=cutoff.timestamp(),
    )["reviews_data"]
    for review in result:
        if review["owner_answer"]:
            continue
        username = review["author_name"]
        text = review["review_text"]
        stars = review["review_rating"]
        date = datetime.fromisoformat(review["review_datetime_utc"])
        url = review["review_link"]

        db_review = Review(
            username=username, text=text, stars=stars, date=date, url=url
        )
        db.session.add(db_review)
        db.session.commit()
