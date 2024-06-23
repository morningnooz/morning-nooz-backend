from string import Template
from types import SimpleNamespace
from lib.static import (
    summary_chunk,
    email_document,
    single_topic_entry
)
from lib.processing.process import run_process, TopicSummaries
from lib.utils import send_message_to_queue
from urllib.parse import quote
import json
import logging


def process(data):
    email = data["email"]
    name = data["name"]
    topics = data["topics"]

    preferences = data["preferences"]
    sources = data["sources"]

    summary_list = ""
    counter = 0
    while len(summary_list) == 0 and counter < 10:
        try:
            logging.info(f"summary attempt {counter}")
            summary_list, unformatted_list = build(topics, preferences, sources)
        except Exception as e:
            logging.error(e)
            logging.info(f"summary attempt no. {counter} failed")
            counter += 1
    message = {
        "email": email,
        "name": name,
        "topics": topics,
        "summaries": summary_list,
    }
    unformatted_message = {
        "email": email,
        "name": name,
        "topics": topics,
        "summaries": unformatted_list,
    }
    logging.info(f"message created: {message}")
    return message, unformatted_message


# construct letter
def build(topics, preferences, sources):
    logging.info("building")
    # [{ topic, summary },...]
    summary_list = []
    unformatted_summary_list = []

    for topic in topics:
        if len(topic) == 0:
            continue

        # ping API - to run process
        # summaries_object = process_query(topic)

        summaries_object = run_process(topic, preferences, sources)
        logging.info("after process")
        # format summary
        logging.info("results:")
        logging.info(summaries_object)
        formatted_summary = format_summary(topic, summaries_object)

        summary_list.append(formatted_summary)
        unformatted_summary_list.append({ "topic": topic, "summaries": [{"title": summ.title, "summary": summ.summary} for summ in summaries_object.summaries]})

    final_text = Template(email_document)

    joined_summaries = "".join(summary_list)

    email_text = final_text.substitute(entries=joined_summaries)

    return email_text, unformatted_summary_list


def format_sources(sources):
    sources_str = "Sources: "
    for i, src in enumerate(sources):
        a_tag = Template("[<a href='$source'>$index</a>] ").substitute(
            source=src, index=i + 1
        )
        sources_str += a_tag

    return sources_str


def format_summary(topic, summaries_obj: TopicSummaries):
    summaries_list = summaries_obj.summaries
    logging.info("summaries list")
    logging.info(summaries_list)
    if len(summaries_list) == 0:
        return ""

    formatted_entries = []
    for entry in summaries_list:
        title = entry.title
        summary = entry.summary

        entry_template_table = Template(summary_chunk)
        formatted_entry = entry_template_table.substitute(title=title, summary=summary)

        formatted_entries.append(formatted_entry)

    html_template = Template(single_topic_entry)
    formatted_text = html_template.substitute(
        topic=topic, chunks="".join(formatted_entries)
    )

    return formatted_text
