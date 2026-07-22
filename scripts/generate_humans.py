import os
import re
import glob
import html


body = os.environ.get(
    "ISSUE_BODY",
    ""
)


def get_field(name):

    match = re.search(
        rf"### {re.escape(name)}\s*\n\s*(.*?)(?=\n###|$)",
        body,
        re.S
    )

    return match.group(1).strip() if match else ""



name = get_field("Your Name") or "Anonymous"

city = get_field("Your Home City")

image_text = get_field("Upload Image Link")



image = ""

image_match = re.search(
    r"https?://[^\s\)\"<>]+",
    image_text
)

if image_match:
    image = image_match.group(0)



slug = re.sub(
    r"[^a-z0-9]+",
    "-",
    name.lower()
).strip("-")



folder = f"people/{slug}"

os.makedirs(
    folder,
    exist_ok=True
)



sections = re.findall(
    r"### (.*?)\n\n(.*?)(?=\n###|$)",
    body,
    re.S
)



answers = []

for question, answer in sections:

    if question.strip() in [
        "Your Name",
        "Your Home City",
        "Upload Image Link"
    ]:
        continue


    answers.append(
        "<div class='answer'>"
        "<h3>" + html.escape(question.strip()) + "</h3>"
        "<p>" + html.escape(answer.strip()) + "</p>"
        "</div>"
    )



person = []

person.append("<!DOCTYPE html>")
person.append("<html>")
person.append("<head>")
person.append(
    "<title>"
    + html.escape(name)
    + " - Humans of Liquicity</title>"
)
person.append(
    "<link rel='stylesheet' href='../../assets/style.css'>"
)
person.append("</head>")
person.append("<body>")
person.append("<div class='profile'>")


if image:

    person.append(
        "<img class='profile-image' src='"
        + image
        + "'>"
    )


person.append(
    "<h1>"
    + html.escape(name)
    + "</h1>"
)

person.append(
    "<h3>📍 "
    + html.escape(city)
    + "</h3>"
)


person.extend(answers)


person.append(
    "<a href='../../'>← Back to Humans of Liquicity</a>"
)

person.append("</div>")
person.append("</body>")
person.append("</html>")


with open(
    f"{folder}/index.html",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(person)
    )



# -----------------------
# Build homepage
# -----------------------


cards = []


for file in glob.glob(
    "people/*/index.html"
):

    with open(
        file,
        encoding="utf-8"
    ) as f:

        page = f.read()


    folder = os.path.basename(
        os.path.dirname(file)
    )


    title = re.search(
        r"<h1>(.*?)</h1>",
        page
    )


photo = re.search(
    r"<img[^>]+src=['\"]([^'\"]+)['\"]",
    page
)


    location = re.search(
        r"📍 (.*?)</h3>",
        page
    )


    title = (
        title.group(1)
        if title
        else folder
    )


    photo = (
        photo.group(1)
        if photo
        else ""
    )


    location = (
        location.group(1)
        if location
        else ""
    )


    cards.append(
        "<article class='human-card'>"
        "<a href='people/"
        + folder
        + "/'>"
        "<img class='human-image' src='"
        + photo
        + "'>"
        "<h2>"
        + html.escape(title)
        + "</h2>"
        "<p>📍 "
        + html.escape(location)
        + "</p>"
        "</a>"
        "</article>"
    )



homepage = []

homepage.append("<!DOCTYPE html>")
homepage.append("<html>")
homepage.append("<head>")
homepage.append("<title>Humans of Liquicity</title>")
homepage.append(
    "<link rel='stylesheet' href='assets/style.css'>"
)
homepage.append("</head>")
homepage.append("<body>")

homepage.append(
    "<header class='hero'>"
    "<h1>🌌 Humans of Liquicity</h1>"
    "<p>The people behind the music</p>"
    "</header>"
)


homepage.append(
    "<main class='gallery'>"
)

homepage.extend(cards)

homepage.append("</main>")
homepage.append("</body>")
homepage.append("</html>")


with open(
    "index.html",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(homepage)
    )
