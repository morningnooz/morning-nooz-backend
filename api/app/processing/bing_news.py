
from string import Template
import requests
import urllib.parse

url = Template('https://api.bing.microsoft.com/v7.0/news/search?q=$query')

params = {
    "Ocp-Apim-Subscription-Key":"fef7f950ce104cedaff30e1ab38c8807",
    "freshness":"Week",
    "sortBy":"Relevance",
    "count":"10",
    "mkt":"en-US",
    "setlang":"en-US"
}

class NewsEntry:
    def __init__(self, name, url, provider, description):
        self.name = name
        self.url = url
        self.provider = provider
        self.description = description
    
    def to_string(self):
        template = Template('NAME: $name, URL: $url, PROVIDER: $provider, DESC: $description')
        return template.substitute({"name": self.name, "url": self.url, "provider": self.provider, "description": self.description})

def search(query_text):
    query_string = urllib.parse.quote(query_text)
    url_string = url.substitute(query=query_string)
    r = requests.get(url_string, headers=params)

    if r.status_code == 200:
        data: dict = r.json()
        res = ""

        for entry in data.get('value'):
            try:
                entry_obj = NewsEntry(entry.get('name'), entry.get('url'), entry.get('provider')[0].get('name'), entry.get('description'))
                # res.append(entry_obj)
                res += entry_obj.to_string()
                res += " | "
            except:
                continue
        return res

    else:
        return ""