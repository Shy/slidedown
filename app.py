from flask import Flask, request
import contentful
import os
from rich_text_renderer import RichTextRenderer

renderer = RichTextRenderer()

SPACE_ID = os.environ.get("SPACE_ID")
DELIVERY_API_KEY = os.environ.get("DELIVERY_API_KEY")

client = contentful.Client(SPACE_ID, DELIVERY_API_KEY)

app = Flask(__name__)


@app.errorhandler(404)
def page_not_found():
    # note that we set the 404 status explicitly
    return (
        "# Slide Deck Does not Exist",
        200,
        {"Content-Type": "text/markdown", "Access-Control-Allow-Origin": "*"},
    )


@app.route("/<string:deck_id>.md")
def deck_by_id(deck_id):
    try:
        entry = client.entry(deck_id)
    except:
        return page_not_found()

    slides = entry.slides
    renderedRichText = ""
    for slide in slides:
        if renderedRichText != "":
            renderedRichText += """

---

"""
        if "duration" in slide.fields():
            renderedRichText += '<section data-autoslide="{0}">'.format(
                slide.duration * 1000
            )
        else:
            renderedRichText += '<section data-autoslide="5000">'

        try:
            renderedRichText += "".join([renderer.render(slide.rt_body), "\n"])

        except AttributeError:
            print("Empty rtBody")
        renderedRichText += "</section>"

    return (
        renderedRichText,
        200,
        {"Content-Type": "text/markdown", "Access-Control-Allow-Origin": "*"},
    )


# We only need this for local development.
if __name__ == "__main__":
    app.run(debug=True)
