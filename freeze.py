from flask_frozen import Freezer
from app import app
import contentful

SPACE_ID = "jokk403r56yp"
DELIVERY_API_KEY = "8b9ddca4bfaa8e3f68520e1211700c6b0fbee29459e7d5b5c776626a3230e8d0"

client = contentful.Client(SPACE_ID, DELIVERY_API_KEY)

freezer = Freezer(app)


@freezer.register_generator
def deck_by_id():
    decks = client.entries({"content_type": "slideDeck"})
    for deck in decks:
        yield {"deck_id": deck.id}


if __name__ == "__main__":
    freezer.freeze()
