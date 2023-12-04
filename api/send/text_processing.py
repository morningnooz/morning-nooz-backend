
from string import Template
from types import SimpleNamespace
from static import topic_summary_template_table, topic_entry_template, closing_message, style_sheet, error_template
from urllib.parse import quote
import requests
import json

def process_query(topic):
    url = 'http://nginx:80/search/' + quote(topic)
    response = requests.get(url)

    if response.status_code == 200:
        res = json.loads(response.text, object_hook=lambda d: SimpleNamespace(**d))
        print('response', res)
        return res
    else:
        return {
            'summaries': []
        }

# construct letter
def build_email(topics):
    print('building')
    # [{ topic, summary },...]
    summary_list = []

    # yesterday_string = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    for topic in topics:
        if len(topic) == 0:
            continue

        # ping API - to run process
        summaries_object = process_query(topic)
        print('after process')
        # format summary
        formatted_summary = format_summary(topic, summaries_object)

        summary_list.append(formatted_summary)

    final_text = style_sheet

    final_text += '<br>'.join(summary_list)

    final_text += closing_message

    return final_text

# def build_string(articles):

#     string_to_summarize = '    '

#     for data in articles['articles']:
#         print(data)
#         new_string = '\nTITLE: '
#         new_string += data['title']

#         new_string += '\nCONTENT: '
#         new_string += data['content']

#         new_string += '\nLINK: '
#         new_string += data['url']

#         new_string += '\n--------- '

#         if len(string_to_summarize) + len(new_string) > 4090:
#             break

#         string_to_summarize += new_string

#         string_to_summarize = string_to_summarize.replace('\n', '    ')

#     return string_to_summarize

def format_sources(sources):
    sources_str = 'Sources: '
    for i, src in enumerate(sources):
        a_tag = Template("[<a href='$source'>$index</a>] ").substitute(source=src, index=i+1)
        sources_str += a_tag

    return sources_str

def format_summary(topic, summaries_obj):
    summaries_list = summaries_obj.summaries
    print('summaries list', summaries_list)
    if len(summaries_list) == 0:
        return ''

    formatted_entries = []
    for entry in summaries_list:

        title = entry.title
        summary = entry.summary

        entry_template_table = Template(topic_entry_template)
        formatted_entry = entry_template_table.substitute(title=title, summary=summary)

        formatted_entries.append(formatted_entry)
    

    html_template = Template(topic_summary_template_table)
    formatted_text = html_template.substitute(topic=topic, entries=''.join(formatted_entries))

    return formatted_text