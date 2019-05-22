from flask import Flask, request
import contentful
from rich_text_renderer import RichTextRenderer

renderer = RichTextRenderer()

SPACE_ID = "jokk403r56yp"
DELIVERY_API_KEY = "8b9ddca4bfaa8e3f68520e1211700c6b0fbee29459e7d5b5c776626a3230e8d0"

client = contentful.Client(SPACE_ID, DELIVERY_API_KEY)

app = Flask(__name__)


@app.route("/")
def hello():
    deck_id = request.args.get("deck", default="3hPCvDC6URrqtst7zNMkqI", type=str)
    try:
        entry = client.entry(deck_id)
    except:
        return (
            "# Slide Deck Does not Exist",
            200,
            {"Content-Type": "text/markdown", "Access-Control-Allow-Origin": "*"},
        )

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
