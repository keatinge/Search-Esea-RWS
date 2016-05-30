import requests
from bs4 import BeautifulSoup
import re

def find_userids_from_search_url(url, page):
    """
    Takes a esea search url and page and returns the esea user ids for all the users on that page as list
    """

    respText = requests.get(url + "&page=" + str(page)).text
    soup = BeautifulSoup(respText, "html.parser")
    resultA = soup.find_all("a", {"class" : "result"})

    #use regex to get the userid out of the hrefs of all the <a class="result">
    idsList = [(re.search(r'/users/(.+)', a['href']).group(1)) for a in resultA]
    return idsList


def get_rws_per_month(userid, month):
    """
    Returns the rws of a user in a specific month
    """

    url = "https://play.esea.net/users/" + str(userid) + "?tab=stats&last_type_scope=pug&game_id=25&type_scope=pug&period%5Btype%5D=months&period%5Bdate_start%5D=" + month
    respText = requests.get(url).text

    soup = BeautifulSoup(respText, "html.parser")
    statPage = soup.find("table", {"class" : "box"})

    return float(statPage.find_all("td", {"class": "stat"})[-1].text) #find the last td class=stat


def get_all_months(userid, numMonths):
    """
    Returns the possible months to get the rws from
    """

    url = "https://play.esea.net/users/" + str(userid) + "?tab=stats"
    respText = requests.get(url).text

    soup = BeautifulSoup(respText, "html.parser")

    monthsSelect = soup.find("select", {"name": "period[date_start]"})
    monthOptions = monthsSelect.find_all("option")

    monthVals = [month['value'] for month in monthOptions]


    return monthVals[:numMonths]



def get_rws_stats_from_userid(userid, numMonths, allMonths):
    """
    Takes an esea user id and returns the rws for the past n months as list
    """

    months = allMonths

    rwsStats = []

    for month in months:
        thisMonthsRws = get_rws_per_month(userid, month)

        if thisMonthsRws == 0.0: #end of stats
            break

        rwsStats.append(thisMonthsRws)

    return rwsStats




