from string import Template
import requests
import logging
import urllib.parse
import os
import json

url = Template("https://api.bing.microsoft.com/v7.0/news/search?q=$query")


class NewsEntry:
    def __init__(self, name, url, provider, description):
        self.name = name
        self.url = url
        self.provider = provider
        self.description = description

    def to_string(self):
        template = Template(
            "NAME: $name, URL: $url, PROVIDER: $provider, DESC: $description"
        )
        return template.substitute(
            {
                "name": self.name,
                "url": self.url,
                "provider": self.provider,
                "description": self.description,
            }
        )


def search(query_text):
    query_string = urllib.parse.quote(query_text)
    url_string = url.substitute(
        query=query_string
    )  # Ensure 'url' is defined and valid.

    params = {
        "Ocp-Apim-Subscription-Key": os.getenv("BING_APIM_KEY"),
        "freshness": "Week",
        "sortBy": "Relevance",
        "count": "7",
        "mkt": "en-US",
        "setlang": "en-US",
    }

    try:
        r = requests.get(
            url_string, headers=params
        )  # Ensure 'params' is defined and valid.

        logging.info(f"API key: {params['Ocp-Apim-Subscription-Key']}")
        if r.status_code != 200:
            # pretty print error message
            raise ValueError(f"{json.dumps(json.loads(r.text), indent=2)}")
        data = r.json()
        logging.info(f"request {data}")

        if "value" not in data or not data["value"]:
            raise ValueError("No data found in response.")

        res = ""
        for entry in data["value"]:
            try:
                provider = entry.get("provider", [{}])[0]
                entry_obj = NewsEntry(
                    entry.get("name"),
                    entry.get("url"),
                    provider.get("name"),
                    entry.get("description"),
                )
                res += entry_obj.to_string() + " | "
            except Exception as e:
                logging.error("Error processing entry: %s", e)
                continue
        return res

    except requests.RequestException as e:
        logging.error("Request error: %s", e)
        raise
    except Exception as e:
        logging.error("An error occurred: %s", e)
        raise
