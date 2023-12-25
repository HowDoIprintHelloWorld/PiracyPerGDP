from requests import get
from bs4 import BeautifulSoup


def getPage(pageNumber):
    page = get(f"https://fitgirl-repacks.site/page/{pageNumber}/?ref=xranks%2F").content
    soup = BeautifulSoup(page, "html.parser")
    return soup



def filterGames(soupPage):
    gamesTitles = soupPage.find_all(class_="entry-title")
    games = [game.find("a", href=True)["href"] for game in gamesTitles]
    return games


def getMagnetFromGame(gameLink):
    page = get(gameLink).content
    pageSoup = BeautifulSoup(page, "html.parser")
    links = pageSoup.find_all("a", href=True)
    for link in links:
        if "magnet:" in link["href"]:
            return link["href"]



def getMagnetsFromPage(pageNumber=0):
    soupPage = getPage(pageNumber)
    games = filterGames(soupPage)
    magnets = [getMagnetFromGame(game) for game in games]
    magnets = [magnet for magnet in magnets if magnet]
    return magnets

