import esea
import colorama

MAXRWSNOW = 6 #the maximum current rws for a player to match
MAXRWSAVG = 9 #the maximum average rws for a player to match
NUMMONTHSACTIVE = 3 #the minimum number of months a player must have rws stats for, in order
STARTPAGE = 10 #page to start on inclusive
ENDPAGE = 20 #number of pages to check from 1-n inclusive. 10 = 1,2,3,4,5,6,7,8,9,10

searchUrl = "https://play.esea.net/index.php?s=search&query=&source=users&sort_by=last_visit&filters%5Bgeo_country%5D=&filters%5Btier%5D=3&fields%5Balias%5D=1&fields%5Bname%5D=1&fields%5Bunique_ids%5D=1"
months = esea.get_all_months("4", NUMMONTHSACTIVE) #use lpkanes profile to scrape all the months


matches = []
for i in range(STARTPAGE, ENDPAGE+1):
    print(colorama.Fore.CYAN + "Scraping page", i, colorama.Fore.RESET)
    ids = esea.find_userids_from_search_url(searchUrl, page=i)
    for id in ids:
        rdubs = esea.get_rws_stats_from_userid(id, numMonths=NUMMONTHSACTIVE, allMonths=months)

        if len(rdubs) == 0: #divide by zero fix for inactive players
            continue

        averageRdubs = sum(rdubs)/len(rdubs)

        if averageRdubs < MAXRWSAVG and len(rdubs) >= NUMMONTHSACTIVE and rdubs[0] < MAXRWSNOW:
            print(colorama.Fore.GREEN + id, rdubs, "--", round(averageRdubs, 2), colorama.Fore.RESET)

            matches.append([id, rdubs, averageRdubs])
        else:
            print(colorama.Fore.RED + id, rdubs, "--", round(averageRdubs, 2), colorama.Fore.RESET)

print("RESULTS")
print("-------")
for match in matches:
    print("AVG", round(match[2], 2), " - ", "RDUBS", match[1], " -- https://play.esea.net/users/" + match[0])


