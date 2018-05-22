import json
from pathlib import Path
import colorama
colorama.init(autoreset=True)
import traceback
import os
absPath = os.path.dirname(os.path.abspath(__file__))


def buildMain(inputPath, outputPath, templatePath):
    templates = {
        "main": (templatePath / "main.html").read_text(),
        "column": (templatePath / "column.html").read_text(),
        "screenshot": (templatePath / "screenshot.html").read_text(),
        "screenshots": (templatePath / "screenshots.html").read_text()
    }
    makePages(inputPath, outputPath, templates)
    print("DONE", end="")


def readJson(path):
    jsonText = json.loads(path.read_text())
    return(jsonText)


def makePage(inputPath, outputPath, templates):
    fileJson = readJson(inputPath)

    columnsText = ""
    for column in fileJson["columns"]:
        # print(column)
        columnsText += """<div class="columns">"""
        for card in column["cards"]:
            if card["header"] == "Screenshots":
                screenshotsText = ""
                for screenshot in card["content"]:
                    screenText = templates["screenshot"].replace(
                        "{{src}}", screenshot["src"])

                    caption = ""
                    captionJson = (screenshot["setup"], screenshot["artist"])
                    for lineJson in captionJson:
                        line = ""
                        if lineJson["url"] != None:
                            line += f"""<p><a href="{lineJson["url"]}">{lineJson["text"]}</a></p>\n"""
                        else:
                            line += f"""<p>{lineJson["text"]}</p>\n"""
                        caption += line
                    screenText = screenText.replace("{{caption}}", caption)

                    screenshotsText += screenText
                columnsText += templates["column"].replace(
                    "{{card-header}}", card["header"]).replace("{{card-content}}", templates["screenshots"].replace("{{screenshots}}", screenshotsText))
            else:
                columnsText += templates["column"].replace(
                    "{{card-header}}", card["header"]).replace("{{card-content}}", card["content"])
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
            outPath = outputPath / filePath.with_suffix(".html").name
            try:
                makePage(filePath, outPath, templates)
                print(
                    colorama.Fore.GREEN + colorama.Style.BRIGHT + "SUCCESS" +
                    colorama.Style.RESET_ALL + ": " +
                    str(outPath.relative_to(Path(absPath).parent))
                )
            except Exception:
                print(
                    colorama.Fore.RED + colorama.Style.BRIGHT + "FAILURE" +
                    colorama.Style.RESET_ALL + ": " +
                    str(outPath.relative_to(Path(absPath).parent)) + "\n" +
                    traceback.format_exc().strip()
                )

        elif filePath.is_dir() and filePath.name != "output":
            makePages(filePath, outputPath / filePath.name, templates)


buildMain(
    Path(absPath + "/content"),
    Path(absPath).parent,
    Path(absPath + "/templates")
)
