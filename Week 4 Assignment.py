import urllib.request
import urllib.parse
import re
import requests
import json

# part1(): Web Scraping
# a user will be asked to enter a stock ticker (symbol). The program will directly scrape webpage https://finance.yahoo.com/ 
# and will return the current price of the current price for each ticker that the User enters until the User quits.

def yahoo_req(url):
    """
    url:
    """
    headers = {
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
        'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': r'https://finance.yahoo.com/'}
    
    request = urllib.request.Request(url, data=None, headers=headers)
    response = urllib.request.urlopen(request)
    # print(response.getcode())
    if response.getcode() == 200:
        html = response.read().decode('utf-8')
        # print(html)
        return html
    else:
        return None


# yahoo_req("https://finance.yahoo.com/quote/BABA?p=BABA&.tsrc=fin-srch")


def part1():
    # input stock symbol
    stock_code = input("please enter the stock code.\n")
    # url
    url = "https://finance.yahoo.com/quote/"+stock_code+"?p="+stock_code+"&.tsrc=fin-srch"
    try: 
        # return result
        _html = yahoo_req(url)
        # if Y, get stock price 
        # <span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="34">153.67</span>
        # <span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="34"></span>
        # <span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="34">1,152.32</span>
        search_data = re.search(r'<span class="Trsdu\(0.3s\) Fw\(b\) Fz\(36px\) Mb\(-4px\) D\(ib\)" data-reactid="34">(.*?)</span>', _html)
        cur_price = search_data.group(1)
        cur_price = re.sub(",", "", cur_price)
        # print stock price
        print("{0} Current price is {1}\n".format(stock_code, cur_price))
    except Exception as e:
        # if stock price is not returned, or page error, print result
        print("{0} Current price search error --> {1}\n".format(stock_code, str(e))) 
    pass


# part2: the program will ask the User to enter a zip code and will return 
# results, the zipcode, the date, the state, the city, and the AQI results (air quality).
# also part1 and part2 are combined

def air_new_req(zip_code):
    # url
    # http://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode=20002&API_KEY=968366E5-84C5-4D28-8FFE-40D6858219AE
    headers = {
        'Connection':'close',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    url = "http://www.airnowapi.org/aq/forecast/zipCode/"+"?zipCode="+zip_code+"&format=application/json&API_KEY=968366E5-84C5-4D28-8FFE-40D6858219AE"
    response = requests.post(url, headers=headers)
    # get feedback
    json_str = response.content.decode("utf-8")
    if not json_str or json_str.strip() == "":
        return None
    # print(json_str)
    json_data = json.loads(json_str)
    return json_data


def part2(FILE_PATH):
    # input zipcode
    zip_code = input("please enter the zipCode.\n")
    try: 
        #  date --> DateForecast or DateIssue
        # the zipcode, the date, the state, the city, and the AQI 
        res_data = air_new_req(zip_code)
        for data in res_data:
            # print(data)
            dateIssue = data["DateIssue"]
            stateCode = data["StateCode"]
            reportingArea = data["ReportingArea"]
            aqi = data["AQI"]
            # print result
            print_str = "{0}\t{1}\t{2}\t{3}\t{4}\n".format(zip_code, dateIssue, stateCode, reportingArea, aqi)
            print(print_str)
            with open(FILE_PATH, "a+", encoding="utf-8") as f:
                f.write(print_str)
    except Exception as e:
        # if stock price is not returned, or page error, print result
        print("{0} search error --> {1}\n".format(zip_code, str(e)))
    pass


if __name__ == "__main__":
    FILE_PATH = "./Part2_OUTFILE.txt"
    with open(FILE_PATH, "w", encoding="utf-8") as f:
        f.write("zipCode\tdateIssue\tstateCode\treportingArea\taqi\n")
    while(True):
        opt = input("please enter `part1` or `part2` to select, enter other to stop\n")
        if opt == "part1":
            part1()
        elif opt == "part2":
            part2(FILE_PATH)
        else:
            print("end ...")
            break
        is_continue = input("Press `Y` to continue and `N` to stop.\n")
        # If input "N", end loop
        if is_continue == "N":
            break
        pass    


