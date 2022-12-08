import lxml.html
import requests

html = requests.get('https://store.steampowered.com/explore/new/')
doc = lxml.html.fromstring(html.content)
new_releases = doc.xpath('//div[@id="tab_newreleases_content"]')[0]
titles = new_releases.xpath('.//div[@class="tab_item_name"]/text()')
prices = new_releases.xpath('.//div[@class="discount_final_price"]/text()')
tags = new_releases.xpath('.//div[@class="tab_item_top_tags"]')
total_tags = []
for i in tags:
    total_tags.append(i.text_content())

tags = [i.text_content() for i in new_releases.xpath('.//div[@class="tab_item_top_tags"]')]

tags = [i.split(', ') for i in tags]

platform_div = new_releases.xpath('.//div[@class="tab_item_details"]')
total_platform = []
for game in platform_div:
    temp = game.xpath('.//span[contains(@class, "platform_img")]')
    platforms = [t.get('class').split(' ')[-1] for t in temp]
    if "hmd_separator" in platforms:
        platforms.remove("hmd_separator")

    total_platform.append(platforms)

output = []
for i in zip(titles, prices, tags, total_platform):
    resp = {
        'title': i[0],
        'price': i[1],
        'tags': i[2],
        'platforms': i[3]
    }
    output.append(resp)

print(output)
