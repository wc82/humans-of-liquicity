import os
import re
import glob
import html

print("Humans publisher v2 - Cloudinary enabled")


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



# -----------------------
# Create person page
# -----------------------

if body:

    name = get_field("Your Name") or "Anonymous"

    city = get_field("Your Home City")

    image_text = get_field("Upload Image Link")


    image = ""


    def extract_url(match):

        if not match:
            return ""

        if match.lastindex:
            return match.group(1)

        return match.group(0)



    # Look in image field first

    image_match = re.search(
        r"https?://[^\s\)\"<>]+",
        image_text
    )

    image = extract_url(image_match)



    # Look anywhere in issue body

    if not image:

        image_match = re.search(
            r"https?://github\.com/user-attachments/[^\s\)\"<>]+",
            body
        )

        image = extract_url(image_match)



    # Look for markdown image format

    if not image:

        image_match = re.search(
            r"\((https?://[^)]+)\)",
            body
        )

        image = extract_url(image_match)



    # Look for HTML image format

    if not image:

        image_match = re.search(
            r'src="([^"]+)"',
            body
        )

        image = extract_url(image_match)



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
            "<h3>"
            + html.escape(question.strip())
            + "</h3>"
            "<p>"
            + html.escape(answer.strip())
            + "</p>"
            "</div>"
        )



    person = [

        "<!DOCTYPE html>",
        "<html>",
        "<head>",

        "<title>"
        + html.escape(name)
        + " - Humans of Liquicity</title>",

        "<link rel='stylesheet' href='../../assets/style.css'>",

        "<meta name='viewport' content='width=device-width, initial-scale=1'>",

        "</head>",

        "<body>",

        "<div class='profile'>"

    ]



    if image:

        person.append(
            "<img class='profile-image' src='"
            + html.escape(image)
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


    person.extend(
        answers
    )


    person.extend(
        [
            "<a href='../../'>← Back to Humans of Liquicity</a>",
            "</div>",
            "</body>",
            "</html>"
        ]
    )



    with open(
        f"{folder}/index.html",
        "w",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n".join(person)
        )



# -----------------------
# Create homepage
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


    name_match = re.search(
        r"<h1>(.*?)</h1>",
        page
    )


    image_match = re.search(
        r"<img[^>]+src=['\"]([^'\"]+)['\"]",
        page
    )


    city_match = re.search(
        r"📍\s*(.*?)</h3>",
        page
    )



    name = (
        name_match.group(1)
        if name_match
        else folder.title()
    )


    image = (
        image_match.group(1)
        if image_match
        else ""
    )


    city = (
        city_match.group(1)
        if city_match
        else ""
    )



    cards.append(
        "<article class='human-card'>"
        "<a href='people/"
        + folder
        + "/'>"
        "<img class='human-image' src='"
        + image
        + "' loading='lazy'>"
        "<div class='card-content'>"
        "<h2>"
        + html.escape(name)
        + "</h2>"
        "<p>📍 "
        + html.escape(city)
        + "</p>"
        "<span>Read their story →</span>"
        "</div>"
        "</a>"
        "</article>"
    )



homepage = [

    "<!DOCTYPE html>",
    "<html>",
    "<head>",
    "<title>Humans of Liquicity</title>",
    "<meta name='viewport' content='width=device-width, initial-scale=1'>",
    "<link rel='stylesheet' href='assets/style.css'>",
    "</head>",
    "<body>",

    "<header class='hero'>",
    "<h1>🌌 Humans of Liquicity</h1>",
    "<p>The people, stories and memories behind the Liquicity family</p>",
    "</header>",

    "<main class='gallery'>",

    "".join(cards),

    "</main>",

    "</body>",
    "</html>"

]



with open(
    "index.html",
    "w",
    encoding="utf-8"
) as f:

    f.write(
        "\n".join(homepage)
    )
