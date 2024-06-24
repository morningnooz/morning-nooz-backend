import logging
import instructor
import feedparser
import re
from urllib.parse import urlparse
from pydantic import BaseModel
from lib.processing.bing_news import search
# from processing.bing_news import search
# from bing_news import search
from openpipe import OpenAI
from string import Template
from datetime import datetime, timedelta, timezone
import email.utils

# vars: docs_info, query_string
reduce_template = Template("""The goal is to create a news digest for an educated user, using the most relevant news to $query_string
    The following is set of articles and their name, url, provider, and description. The articles contain varying degrees of relevance to $query_string, and you will only extract the most relevant points:
    $docs_info ---------
    Extract the key points then synthesize and refine it into a final, consolidated summary of the top three to five key ideas across all the sources, with up to five (5) points for each, using examples from the articles. Use details from the texts, and please cite the references by creating an <a> tag referencing the url for the given article, with the text in the <a> tag set to the article's provider.
    Do NOT include information from articles that are not relevant news stories pertaining to $query_string.
    Please do NOT include the words "the documents" or "the articles" or "this theme" (or other metadata) in the summaries. Just provide detailed, straight-forward summaries of the facts encountered.
    Filter out any information about privacy policies or the authors of the articles. Ignore any information that is likely not to be relevant to a news digest, such as sales deals and descriptions about products.
    Output the summaries as a bulleted list, and try to include multiple citations for each key point.
    $prefs
    Use this format:
    {{
        "summaries": [
            {{
            "title": "Example title that captures one key detail about the news",
            "summary": "<ul><li>Example summary that shows information relating to this key detail</li><li>Example summary line 2<a href="article url">[first provider name]</a> <a href="article url">[second provider name]</a></li></ul>"
            }},
            {{
            "title": "Example title that captures a second, different key detail about the news",
            "summary": "<ul><li>Example summary that shows information relating to this second key detail</li><li>Example summary line 2 <a href="article url">[provider name]</a></li><ul>"
            }},
            {{
            "title": "Example title that captures a third, different key detail about the news",
            "summary": "<ul><li>Example summary that shows information relating to this third key detail <a href="article url">[third provider name]</a></li><li>Example summary line 2 <a href="article url">[provider name]</a></li><ul>"
            }}
        ]
    }}
    ___
    here is an example for the topic 'Microsoft':
    {{
        "summaries": [
        {{
            "title": "Activision Blizzard Acquisition",
            "summary": "<ul><li>Microsoft proposed an acquisition of Activision Blizzard in January 2022, but has since restructured the acquisition to meet the competition demands of the UK government</li><li>They have proposed to grant cloud streaming rights for all current and newly released games to Ubisoft <a href=\"https://www.theverge.com/2023/10/13/23791235/microsoft-activision-blizzard-acquisition-complete-finalized\">[The Verge]</a></li></ul>"
        }},
        {{
            "title": "AI Integrations",
            "summary": "<ul><li>Microsoft is pushing for AI to be integrated across many disciplines. Company vice chairman Brad Smith claims that generative AI will be both a tool and a threat to managing cybersecurity concerns <a href=\"https://www.pcworld.com/article/2132572/copilot-may-be-coming-to-windows-10-after-all.html\">[PC World]</a></li><li>Microsoft also has plans to integrate AI-powered features into built-in Windows apps, such as Photos, Snipping Tool, and Paint <a href=\"https://www.ft.com/content/81db7c36-f9ae-496b-9dd4-971aefe6f9a9\">[Financial Times]</a></li></ul>"
        }},
        {{
            "title": "Product Releases and Discontinuations",
            "summary": "<ul><li>Microsoft has recently released a slew of new products. They have integrated Python into Excel, enabling users to manipulate data with code</li><li>Meanwhile, Microsoft has also announced that is is discontinuing the Kinect sensor, which transitioned from a gaming device to a tool for hobbyist and research projects <a href=\"https://www.theverge.com/2023/8/21/23840327/microsoft-azure-kinect-developer-kit-discontinued\">[The Verge]</a><a href=\"https://www.pcworld.com/article/2041963/you-can-now-use-python-in-microsoft-excel.html\">[PC World]</a></li></ul>"
        }}
        ]
    }}
    ---
    Helpful Answer:""")

# vars: docs, query
old_scoring_template = Template("""The following is set of articles and their name, url, provider, and description:
    $docs
    Based on this list of docs, please rank the relevance of news articles relating to $query. If there are many articles, only score the most relevant 25 articles.
    Repeat the text and provide a 'news score' for each document, as a number from 1 to 10, which is higher when the content is news that would have high relevance for a reader trying to learn about the current events and discourse for $query, and
    lower for text which is unrelated to current events related to their topic. Summaries with sales/deals information, general encyclopedia-like descriptions of things or authors, or simple references to other sites must receive scores less than 3.
    $prefs
    ---
    Example Answer 1:
news:
NAME: AI robotics' 'GPT moment' is near
URL: https://uk.news.yahoo.com/ai-robotics-gpt-moment-near-143539650.html
PROVIDER: Yahoo News UK
DESC: It's no secret that foundation models have transformed AI in the digital world. Large language models (LLMs) like ChatGPT, LLaMA, and Bard revolutionized AI for language. While OpenAI's GPT models aren't the only large language model available
SCORE: 6 (as the description is not extremely relevant news and is quite general)

NAME: California is the robotics capital of the world
URL: https://robohub.org/california-is-the-robotics-capital-of-the-world/
PROVIDER: Robohub
DESC: Countries with no robotics; Andorra, Montenegro, Albania, Macedonia, Kosovo, Moldova, Malta, Vatican City.
SCORE: 3 (as this is not really a news story, and the description is quite general)

NAME: Robotics Q&A: CMU's Matthew Johnson-Roberson, URL: https://uk.finance.yahoo.com/news/robotics-q-cmus-matthew-johnson-141517997.html
PROVIDER: Yahoo Finance
DESC: Johnson-Roberson also co-founded and serves as the co-founder and CTO of robotic last-mile delivery startup Refraction AI. What role(s) will generative AI play in the future of robotics? Generative AI
SCORE: 3 (as this is an interview and not a news story)

NAME: Robotics funding saw another dip in 2023, 
URL: https://uk.news.yahoo.com/robotics-funding-saw-another-dip-225702372.html
PROVIDER: Yahoo News UK
DESC: In 2021, robotics startups were flying high. Unlike other categories that had buckled under the strains of a global pandemic, interest in automation was at an all-time high, as companies attempted to navigate supply chain issues and ongoing labor shortages.
SCORE: 8

NAME: Robotics competition challenges students to merge art and technology
URL: https://www.msn.com/en-us/news/technology/robotics-competition-challenges-students-to-merge-art-and-technology/ar-AA1jNJS9
PROVIDER: wsbt on MSN.com
DESC: LEGO robotics teams across our region appeared in the first LEGO Leage Challenge in the Masterpiece season.Spectators had the chance to see the Lego Robots in a
SCORE: 7

NAME: Don't wait to plan next year's robotics investments
URL: https://www.themanufacturer.com/articles/dont-wait-to-plan-next-years-robotics-investments/
PROVIDER: Manufacturing,
DESC: Businesses looking to automate in 2024 should start preparations early to avoid delays and to realise the full potential of their investments.
SCORE: 6 (it is fairly pertinent to the query topic, but it is not really a news story)

NAME: Robotics
URL: https://www.bbc.com/news/topics/c8nq32jw88jt?page=24
PROVIDER: BBC
DESC: Audio, 29 minutesThe Works Robotics The word 'robot' didn't exist until 1921 © 2023 BBC. The BBC is not responsible for the content of external sites. Read about our approach to external linking. 
SCORE: 1 (not news)

NAME: 2023 Robotics Funding Trends: A Closer Look
URL: https://pc-tablet.com/2023-robotics-funding-trends-a-closer-look/
PROVIDER: PC Tablet
DESC: The robotics industry has seen a downturn in funding in 2023, with investment figures falling significantly from previous years. This decline follows a high point for the sector during the pandemic years when automation and robotics were seen as critical for business continuity
SCORE: 9

NAME: Why this autonomous vehicle veteran joined a legged robotics startup
URL: https://uk.movies.yahoo.com/why-autonomous-vehicle-veteran-joined-010006450.html
PROVIDER: Yahoo Movies UK
DESC: Zhang Li's career path has looked like a bellwether for China's tech trends. When the Cisco veteran joined WeRide in 2018, the Chinese autonomous vehicle company was less than a year old. In the next few years 
SCORE: 7

NAME: Robotics kits for sale at a discount
URL: https://yahoo.com/robotics-kits-are-discounted.html
PROVIDER: Yahoo
DESC: Robotics kits are now on sale at a discount
SCORE: 1 (it is sales information and not news)

NAME: Boston Dynamics is a robotics company 
URL: https://msn.com/boston-dynamics.html
PROVIDER: MSN.com
DESC: Boston Dynamics is a robotics company revolutionizing the defense sector
SCORE: 1 (it is descriptive information of a company and not news)
    ---
    Example Answer 2:
news:
NAME: VC investment into impact startups plummets worldwide in 2023 Dealroom research
URL: https://www.pioneerspost.com/news-views/20231107/vc-investment-impact-startups-plummets-worldwide-2023-dealroom-research
PROVIDER: Pioneers Post
DESC: Latest figures launched at ImpactFest show downward trend in impact venture capital funding continues to gather pace since 2021s high point.
SCORE: 7

NAME: VC Funding Tanks, Alpha Partners Shares Perspective and Future Expectations on Venture Market
URL: https://www.crowdfundinsider.com/2023/11/215174-vc-funding-tanks-alpha-partners-shares-perspective-and-future-expectations-on-venture-market/
PROVIDER: Crowdfund Insider
DESC: So when does the pause in VC funding end? When is the gloomy market going to turn the corner? Is it when interest rates are no longer expected to rise?
SCORE: 5

NAME: Venture Capital Explained: How Does It Work?
URL: https://www.forbes.com/advisor/au/investing/venture-capital-explained/
PROVIDER: Forbes
DESC: According to data from the governments Department of Industry, Science and Resources, Australia has around 130 active venture capital firms which have committed around $30 billion of capital since the introduction of the Venture Capital Act in 2002. 
SCORE: 6

NAME: Venture Funding Dried Up Even More in October -- and It's Not Expected to Rebound Soon
URL: https://www.msn.com/en-us/money/savingandinvesting/venture-funding-dried-up-even-more-in-october-and-its-not-expected-to-rebound-soon/ar-AA1jynum
PROVIDER: Inc on MSN.com
DESC: According to a new analysis, October saw global funding slump by 24 percent year over year. Founders -- even those behind A.I. companies -- should prepare for a longer funding drought.
SCORE: 8

NAME: All-male venture capital funds raise 10 times more than all-female
URL: https://www.msn.com/en-gb/money/other/all-male-venture-capital-funds-raise-10-times-more-than-all-female/ar-AA1jvAcx
PROVIDER: City A.M. on MSN.com
DESC: A new report has exposed that in the UK, all-male-owned VC funds collectively raised around 10 times more capital than all-female-owned funds.
SCORE: 10

NAME: Venture capital guilty of "diversity washing" says Ada Ventures
URL: https://growthbusiness.co.uk/venture-capital-guilty-of-diversity-washing-says-ada-ventures-2570890/
PROVIDER: Growth Business
DESC: Venture capital firms guilty of 'diversity washing' says VC Ada Ventures, with men continuing to dominate venture capital management. 
SCORE: 10

NAME: Top 10 Crypto Venture Capital Firms Beyond 2023
URL: https://www.msn.com/en-us/money/smallbusiness/top-10-crypto-venture-capital-firms-beyond-2023/ar-AA1jD2KY
PROVIDER: Cryptopolitan on MSN.com
DESC: Venture capitalists step into the business terrain where the uncertain terrain of new ventures presents a greater risk than the paths walked by traditional lenders or financiers. They typically trade this higher risk for a slice of the company's equity, 
SCORE: 5 (not really news)

NAME: Breaking Barriers: Empowering Women Entrepreneurs In Venture Capital
URL: https://www.forbes.com/sites/melissahouston/2023/11/06/breaking-barriers-empowering-women-entrepreneurs-in-venture-capital/
PROVIDER: Forbes
DESC: This kind of disparity is unacceptable, especially when there's a plethora of talented women-led businesses that are contributing significantly to our economy. 
SCORE: 8

NAME: Biotech Companies Tap Saudi Arabia for Venture Funding
URL: https://www.wsj.com/articles/biotech-companies-tap-saudi-arabia-for-venture-funding-f09c0a88
PROVIDER: Wall Street Journal
DESC: Slowing U.S. venture investment is spurring startups to consider investors from the oil-rich country.
SCORE: 10

NAME: The AlleyWatch October 2023 New York Venture Capital Funding Report
URL: https://www.alleywatch.com/2023/11/new-york-venture-capital-october-2023/
PROVIDER: alleywatch.com
DESC: The average late-stage round in NYC for October was $56.4M Tweet This The median late-stage round in NYC for October was $40.0M Tweet This $395.0M was invested across late-stage rounds in NYC in October Tweet This 16.82% of late-stage funding nationally went to startups in NYC in October Tweet
SCORE: 6
    Helpful Answer:""")

scoring_template = Template("""The following is set of articles and their name, url, provider, and description. $prefs:
    $docs
    Based on this list of docs, please rank the relevance of news articles relating to $query.
    Repeat the text and provide a 'news score' for each document, as a number from 1 to 10, which is higher when the content is news that would have high relevance for a reader trying to learn about the current events and discourse for $query, and
    lower for text which is unrelated to current events related to their topic. Summaries with sales/deals information, general encyclopedia-like descriptions of things or authors, or simple references to other sites must receive scores less than 3.
    $prefs
    ---
    Helpful Answer:""")

# vars: query
augment_template = Template("""You are a helpful semantics expert who can generate semantically similar news queries for a keyword-based news search engine, returning a list of 2 different options, delimited by ,.
            ---EXAMPLE--- INPUT: nvidia OUTPUT: queries: [nvidia gpu, nvidia chips] ---END EXAMPLE--- 
            ---EXAMPLE--- INPUT: indonesian tech OUTPUT: queries:[indonesia startups, indonesia venture capital] ---END EXAMPLE--- 
            ---EXAMPLE--- INPUT: formula one racing tech OUTPUT: queries: [formula one drivers, formula one races] ---END EXAMPLE--- 
            Generate similar queries to this: $query""")

def extract_subdomain(url):
    parsed_url = urlparse(url)
    # parts = parsed_url.netloc.split('.')
    return parsed_url.hostname

def clean_html(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext

def is_older(date_str):
    # Parse the date string using email.utils
    parsed_date = email.utils.parsedate_to_datetime(date_str)
    if parsed_date.tzinfo is None:
        parsed_date = parsed_date.replace(tzinfo=timezone.utc)

    # Get the current time in UTC
    current_time = datetime.now(timezone.utc)

    # Check if the parsed date is older than one day from the current time
    days_ago = current_time - timedelta(days=1.5)
    return parsed_date < days_ago


def parse_rss_feed(feed_url, url_set: set):
    # Parse the RSS feed
    feed = feedparser.parse(feed_url)

    feed_entries = dict(feed)["entries"]
    result = ""
    cleaned_entries = 0

    logging.info(f'num of feed entries: {str(len(feed_entries))}')
    logging.info(f'RSS url: {feed_url}')
    
    for article in feed_entries[:15]:
        # only include if article was published in last two days
        if ('published' in article and is_older(article.published)):
            continue

        # Extracting the feed title (name), link (URL), and description (DESC)
        feed_name = article.title if 'title' in article else 'No title'
        feed_url = article.link if 'link' in article else 'No link'
        feed_provider = extract_subdomain(article.link) if 'link' in article else article.get('publisher', article.get('author', 'No provider'))
        feed_desc = clean_html(article.get('summary', article.get('content', 'No provider')))

        url_set.add(feed_url)
    
        # Format the output string
        result += f"NAME: {feed_name}, URL: {feed_url}, PROVIDER: {feed_provider}, DESC: {feed_desc}| "

        cleaned_entries += 1
    
    logging.info(f'num of clean entries: {str(cleaned_entries)}')
    
    return result

# Define your desired output structure
class NewsScore(BaseModel):
    name: str
    url: str
    provider: str
    desc: str
    score: str
    
class NewsScores(BaseModel):
    news: list[NewsScore]

class TopicSummary(BaseModel):
    title: str
    summary: str

class TopicSummaries(BaseModel):
    summaries: list[TopicSummary]

class AugmentedQueries(BaseModel):
    queries: list[str]

# Patch the OpenAI client
client = instructor.from_openai(OpenAI())

def scoring(articles, topic, preference) -> NewsScores:

    pref_message = f"also score the news based on its relevance to the user's topic ({topic}) and their preference: {preference}" if preference else ""
    score_prompt = scoring_template.safe_substitute({ "docs": articles, "query": topic, "prefs": pref_message})
    logging.info(f'SCORE PROMPT: {score_prompt}')

    try:
        return client.messages.create(
        model="openpipe:clear-bobcats-attack",
        max_retries=5,
        messages=[
            {
                "role": "user",
                "content": scoring_template.safe_substitute({ "docs": articles, "query": topic, "prefs": pref_message}),
            }
        ],
        response_model=NewsScores
    )
    except Exception as e:
        # Other exceptions
        return client.messages.create(
            model="gpt-4o",
            max_retries=5,
            messages=[
                {
                    "role": "user",
                    "content": scoring_template.safe_substitute({ "docs": articles, "query": topic, "prefs": pref_message}),
                }
            ],
            response_model=NewsScores
        )

def get_summaries(query, query_results, preferences, url_set: set) -> TopicSummaries:
    # chunk scoring into each group then join then
    scored_news: list[list[NewsScore]] = []
    for group in query_results:
        scored_group = scoring(group, query, preferences)
        if (len(scored_group.news) > 0):
            scored_news.append(scored_group.news)
    logging.info(f"SCORED NEWS: {scored_news}\n")
    # filter out scores <= 5
    # Flatten the list of lists
    flattened_scored_news = [news for group in scored_news for news in group]

    # Filter out scores <= 5
    filtered_news = [news for news in flattened_scored_news if (int(news.score) > 6 and news.url in url_set)]

    logging.info(f"FILTERED NEWS: {filtered_news}\n")

    pref_message = f"Prioritize content based on this user's preference: {preferences}" if preferences else ""

    logging.info(f'REDUCE PROMPT: {reduce_template.safe_substitute({"docs_info": filtered_news, "query_string": query, "prefs": pref_message})}')

    # synthesize
    summaries = client.messages.create(
        model="gpt-4o",
        max_retries=5,
        messages=[
            {
                "role": "user",
                "content": reduce_template.safe_substitute({"docs_info": filtered_news, "query_string": query, "prefs": pref_message}),
            }
        ],
        response_model=TopicSummaries,
    )
    logging.info(f"SYNTHESIS{summaries}\n")

    return summaries

def augment_query(query):
    # synthesize
    query_list = client.messages.create(
        model="gpt-4o",
        max_retries=5,
        messages=[
            {
                "role": "user",
                "content": augment_template.safe_substitute({"query": query}),
            }
        ],
        response_model=AugmentedQueries,
    )

    return query_list.queries

# run query + construct summary & return object with summaries
def run_process(query, preferences, sources) -> TopicSummaries:
    url_set = set()

    results = []
    # scan each RSS feed and append it to query_results
    for u in sources:
        res = parse_rss_feed(u, url_set)
        if len(res) > 0:
            results.append(res) 

    query_topics = [query]

    # time.sleep(1)
    # if no RSS feeds are provided, augment Bing search
    if (len(results) == 0):
        augment_queries = augment_query(query)
        query_topics.append(augment_queries)

        logging.info(f"AUG QUERIES {str(query_topics)}\n")

    for q in query_topics:
        res = search(q, url_set)
        if len(res) > 0:
            results.append(res) 

    logging.info(f"RESULTS: {results}")

    summaries = get_summaries(query, results, preferences, url_set)

    return summaries