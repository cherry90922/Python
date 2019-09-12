import urllib.request
import urllib.parse
import re
import requests
import json


def yahoo_req(url):
    """
    url: 请求地址
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
    # 输入股票代码
    stock_code = input("please enter the stock code.\n")
    # 拼接请求地址
    url = "https://finance.yahoo.com/quote/"+stock_code+"?p="+stock_code+"&.tsrc=fin-srch"
    try: 
        # 发起请求、获取返回数据
        _html = yahoo_req(url)
        # 正则抓取 股票价格  
        # <span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="34">153.67</span>
        # <span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="34"></span>
        # <span class="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)" data-reactid="34">1,152.32</span>
        search_data = re.search(r'<span class="Trsdu\(0.3s\) Fw\(b\) Fz\(36px\) Mb\(-4px\) D\(ib\)" data-reactid="34">(.*?)</span>', _html)
        cur_price = search_data.group(1)
        cur_price = re.sub(",", "", cur_price)
        # 打印输出股票价格
        print("{0} Current price is {1}\n".format(stock_code, cur_price))
    except Exception as e:
        # 未搜索到股票价格、或返回页面有误等情况、打印输出
        print("{0} Current price search error --> {1}\n".format(stock_code, str(e))) 
    pass

# part1()

def air_new_req(zip_code):
    # 拼接请求地址
    # http://www.airnowapi.org/aq/forecast/zipCode/?format=application/json&zipCode=20002&API_KEY=968366E5-84C5-4D28-8FFE-40D6858219AE
    headers = {
        'Connection':'close',
        'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
    url = "http://www.airnowapi.org/aq/forecast/zipCode/"+"?zipCode="+zip_code+"&format=application/json&API_KEY=968366E5-84C5-4D28-8FFE-40D6858219AE"
    response = requests.post(url, headers=headers)
    # 获取返回数据
    json_str = response.content.decode("utf-8")
    if not json_str or json_str.strip() == "":
        return None
    # 转换json格式
    # print(json_str)
    json_data = json.loads(json_str)
    return json_data


def part2(FILE_PATH):
    # 输入邮政编码
    zip_code = input("please enter the zipCode.\n")
    try: 
        # 发起请求、获取返回数据  date --> DateForecast or DateIssue
        # the zipcode, the date, the state, the city, and the AQI 
        res_data = air_new_req(zip_code)
        for data in res_data:
            # print(data)
            dateIssue = data["DateIssue"]
            stateCode = data["StateCode"]
            reportingArea = data["ReportingArea"]
            aqi = data["AQI"]
            # 打印输出 查询预测结果
            print_str = "{0}\t{1}\t{2}\t{3}\t{4}\n".format(zip_code, dateIssue, stateCode, reportingArea, aqi)
            print(print_str)
            with open(FILE_PATH, "a+", encoding="utf-8") as f:
                f.write(print_str)
    except Exception as e:
        # 未搜索到数据、或异常情况、打印输出
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
        # 如果输入N则跳出循环
        if is_continue == "N":
            break
        pass    


