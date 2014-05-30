import scraperwiki
import re
scraperwiki.sqlite.attach("forbes_billionaires","list")
print scraperwiki.sqlite.execute("select * from list.swdata")


import lxml.html
import lxml.etree
root_url = "forbes.com/billionaires/list/"
initial_page = 1
final_page = 13
root_url_end = "/#tab:overall"

for n in range(initial_page,final_page+1):
    print n
    html = scraperwiki.scrape(root_url + str(n) + root_url_end)
    root = lxml.html.fromstring(html)
    the_list = root.xpath("//div[@id='thelist']//table//tbody//tr") #

    for tr in the_list:
        tds = tr.cssselect("td")
        #print lxml.etree.tostring(tds[1])
        data = {
            'rank' : tds[0].text_content(),
            'name' : re.sub('\n','',tds[1].text_content()).strip(),
            'thumbnail' : str(re.search(r"img src=\"(.*?)\"",lxml.etree.tostring(tds[1])).group(1)).strip(),
            'profile' : "http://www.forbes.com" + str(re.search(r"a rel=\"(.*?)\"",lxml.etree.tostring(tds[1])).group(1)),
            'net_worth' : float(re.sub('\$|B','',tds[2].text_content()).strip()),
            'age' : tds[3].text_content().strip(),
            'source' : tds[4].text_content().strip(),
            'country' : tds[5].text_content().strip(),
        }
        data['key'] = "%s %s" % (data['rank'], data['name'])
        scraperwiki.sqlite.save(unique_keys=['key'], data=data)
        print data

