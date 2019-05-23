from flask_frozen import Freezer
from app import app
import contentful
import os

SPACE_ID = os.environ.get("SPACE_ID")
DELIVERY_API_KEY = os.environ.get("DELIVERY_API_KEY")

client = contentful.Client(SPACE_ID, DELIVERY_API_KEY)

freezer = Freezer(app)


@freezer.register_generator
def deck_by_id():
    decks = client.entries({"content_type": "slideDeck"})
    for deck in decks:
        yield {"deck_id": deck.id}


if __name__ == "__main__":
    freezer.freeze()
