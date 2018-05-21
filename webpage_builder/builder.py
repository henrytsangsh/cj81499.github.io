import json
from pathlib import Path


def buildMain(inputPath, outputPath, templatePath):
    nav = buildNav(inputPath / "mainNav.json").strip()
    # print(nav)
    templates = {
        "main": (templatePath / "main.html").read_text().replace("{{mainNav}}", nav),
        "column": (templatePath / "column.html").read_text(),
        "screenshot": (templatePath / "screenshot.html").read_text(),
        "screenshots": (templatePath / "screenshots.html").read_text()
    }
    makePages(inputPath, outputPath, templates)
    print("DONE", end="")
    # makePage(inputPath/"index.json", outputPath/"index.html", templates)


def buildNav(navPath):
    nav = ""
    navJson = readJson(navPath)
    # print(json.dumps(navJson, indent=4))
    for item in navJson["items"]:
        try:
            children = item["children"]
            nav += """\n<div class="navbar-item has-dropdown is-hoverable">\n<a href="{0}" id={1} class="navbar-link">{2}</a>\n<div class="navbar-dropdown">""".format(
                item["url"], item["name"].lower(), item["name"])

            for child in children:
                nav += """\n<a id="{2}" class="navbar-item" href="{0}">{1}</a>""".format(
                    child["url"], child["name"], child["name"].lower())

            nav += """\n</div>\n</div>"""
        except KeyError:
            nav += """\n<a href="{0}" id="{1}" class="navbar-item">{2}</a>""".format(
                item["url"], item["name"].lower(), item["name"])
    return nav


def readJson(path):
    jsonText = json.loads(path.read_text())
    return(jsonText)


def makePage(inputPath, outputPath, templates):
    fileJson = readJson(inputPath)
    # if(inputPath.name == "index.json"):
    #     print("index")

    columnsText = ""
    for column in fileJson["columns"]:
        # print(column)
        columnsText += """<div class="columns">"""
        for card in column["cards"]:
            if type(card["content"]) == str:
                columnsText += templates["column"].replace(
                    "{{card-header}}", card["header"]).replace("{{card-content}}", card["content"])
            elif type(card["content"]) == list:
                screenshotsText = ""
                for screenshot in card["content"]:
                    screenshotText = templates["screenshot"].replace(
                        "{{url}}", screenshot["url"]).replace(
                        "{{label}}", screenshot["label"])
                    screenshotsText += screenshotText
                columnsText += templates["column"].replace(
                    "{{card-header}}", card["header"]).replace("{{card-content}}", templates["screenshots"].replace("{{screenshots}}", screenshotsText))
            else:
                print(f"""\n{card["content"]}""")
        columnsText += "</div>"

    mainPage = templates["main"]
    if fileJson["hero"]["subtitle"] != None:
        mainPage = mainPage.replace(
            """<h1 class="title ">{{hero-title}}</h1>""", """<h1 class="title ">{{hero-title}}</h1>\n<p class="subtitle ">{{hero-subtitle}}</p>""")

    replacementList = [
        ["{{page}}", fileJson["page"]],
        ["{{page-lower}}", fileJson["page"].lower()],
        ["{{hero-title}}", fileJson["hero"]["title"]],
        ["{{hero-subtitle}}", fileJson["hero"]["subtitle"]],
        ["{{columns-text}}", columnsText]
    ]
    for replacement in replacementList:
        # print(replacement)
        if replacement[1] != None:
            try:
                mainPage = mainPage.replace(replacement[0], replacement[1])
            except:
                pass

    outputPath.write_text(mainPage)


def makePages(inputPath, outputPath, templates):
    outputPath.mkdir(exist_ok=True)
    for filePath in inputPath.iterdir():
        if filePath.match("*.json") and filePath.stem != "mainNav":
            try:
                outPath = outputPath/filePath.with_suffix(".html").name
                makePage(filePath, outPath, templates)
                print("SUCCESS: " + str(filePath.with_suffix(".html")))
            except:
                print("FAIL: " + str(filePath.with_suffix(".html")))
        elif filePath.is_dir() and filePath.name != "output":
            makePages(filePath, outputPath / filePath.name, templates)


import os
absPath = os.path.dirname(os.path.abspath(__file__))
try:
    buildMain(Path("./content"), Path("../"), Path("./templates"))
except:
    buildMain(
        Path(absPath + "/content"),
        Path(absPath + "/output"),
        Path(absPath + "/templates")
    )
