import json
import os
import time
from lib.processing.bing_news import search
from types import SimpleNamespace
from langchain.chat_models.openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.llm import LLMChain

llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo-16k")

# to do - use Bing + augment queries + use chain of thought


def build_summary_chain(query, query_results):
    # Map
    map_template = """The following is set of articles and their name, url, provider, and description:
    {docs}
    Based on this list of docs, please rank the relevance of the news relating to {query}.
    Repeat the text and provide a 'news score' for each document, as a number from 1 to 10, which is higher when the content is news that would have high relevance for a reader trying to learn about the current events and discourse for {query}, and
    lower for text which is unrelated to current events related to their topic. Summaries with sales/deals information, general encyclopedia-like descriptions of things or authors, or simple references to other sites must receive scores less than 3.
    ---
    Example Answer 1:
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
    Helpful Answer:"""
    map_prompt = PromptTemplate.from_template(
        map_template, partial_variables={"query": query}
    )
    map_chain = LLMChain(llm=llm, prompt=map_prompt)

    mapped_res = map_chain.run(docs=query_results)

    # Reduce
    reduce_template = """The following is set of articles and their name, url, provider, description, and a score of their news relevance:
    {docs_info}
    Take these and then synthesize and refine it into a final, consolidated summary of the three to five key ideas across all the sources, with five sentences for each, using examples from the articles. Use details from the texts, and please cite the references by creating an <a> tag referencing the url for the given article, with the text in the <a> tag set to the article's provider.
    The goal is to create a news digest for an educated user, using the most relevant news to {query_string}
    Do NOT include information from articles that are not relevant news stories.
    ONLY include articles with news scores above 6.
    Please do NOT include the words "the documents" or "the articles" or "this theme" (or other metadata) in the summaries. Just provide detailed, straight-forward summaries of the facts encountered.
    Filter out any information about privacy policies or the authors of the articles. Ignore any information that is likely not to be relevant to a news digest, such as sales deals and descriptions about products.
    Use this format:
    {{
        "summaries": [
            {{
            "title": "Example title that captures one key detail about the news",
            "summary": "Example summary that shows information relating to this key detail <a href='article url'>[first provider name]</a>"
            }},
            {{
            "title": "Example title that captures a second, different key detail about the news",
            "summary": "Example summary that shows information relating to this second key detail <a href='article url'>[second provider name]</a>"
            }},
            {{
            "title": "Example title that captures a third, different key detail about the news",
            "summary": "Example summary that shows information relating to this third key detail <a href='article url'>[third provider name]</a>"
            }}
        ]
    }}
    ___
    here is an example for the topic 'Microsoft':
    {{
        "summaries": [
        {{
            "title": "Activision Blizzard Acquisition",
            "summary": "Microsoft proposed an acquisition of Activision Blizzard in January 2022, but has since restructured the acquisition to meet the competition demands of the UK government <a href='https://blogs.microsoft.com/on-the-issues/2023/08/21/microsoft-activision-restructure-acquisition/'>[Microsoft]</a>. They have proposed to grant cloud streaming rights for all current and newly released games to Ubisoft <a href='https://www.theverge.com/2023/10/13/23791235/microsoft-activision-blizzard-acquisition-complete-finalized'>[The Verge]</a>."
        }},
        {{
            "title": "AI Integrations",
            "summary": "Microsoft is pushing for AI to be integrated across many disciplines. Company vice chairman Brad Smith claims that generative AI will be both a tool and a threat to managing cybersecurity concerns <a href='https://www.pcworld.com/article/2132572/copilot-may-be-coming-to-windows-10-after-all.html'>[PC World]</a>. Microsoft also has plans to integrate AI-powered features into built-in Windows apps, such as Photos, Snipping Tool, and Paint <a href='https://www.ft.com/content/81db7c36-f9ae-496b-9dd4-971aefe6f9a9'>[Financial Times]</a>."
        }},
        {{
            "title": "Product Releases and Discontinuations",
            "summary": "Microsoft has recently released a slew of new products. They have integrated Python into Excel, enabling users to manipulate data with code <a href='https://www.pcworld.com/article/2041963/you-can-now-use-python-in-microsoft-excel.html'>[PC World]</a>. Meanwhile, Microsoft has also announced that is is discontinuing the Kinect sensor, which transitioned from a gaming device to a tool for hobbyist and research projects <a href='https://www.theverge.com/2023/8/21/23840327/microsoft-azure-kinect-developer-kit-discontinued'>[The Verge]</a>."
        }}
        ]
    }}
    ---
    Helpful Answer:"""
    reduce_prompt = PromptTemplate.from_template(reduce_template)

    # Run chain
    reduce_chain = LLMChain(llm=llm, prompt=reduce_prompt, verbose=True)

    reduce_res = reduce_chain.run(docs_info=mapped_res, query_string=query)

    return reduce_res


# run query + construct summary & return object with summaries
def run_process(query):
    # time.sleep(1)
    # run query
    query_results = search(query)
    summaries = build_summary_chain(query, query_results)

    return summaries
