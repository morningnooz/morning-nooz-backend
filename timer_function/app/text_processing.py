from string import Template
from types import SimpleNamespace
from app.static import (
    topic_summary_template_table,
    topic_entry_template,
    closing_message,
    style_sheet,
    error_template,
)
from urllib.parse import quote
from app.processing.process import run_process
import json
import logging


# construct letter
def build_email(topics):
    logging.info("building")
    # [{ topic, summary },...]
    summary_list = []

    for topic in topics:
        if len(topic) == 0:
            continue

        # ping API - to run process
        # summaries_object = process_query(topic)

        summaries_object = run_process(topic)
        res = json.loads(summaries_object, object_hook=lambda d: SimpleNamespace(**d))
        logging.info("after process")
        # format summary
        formatted_summary = format_summary(topic, res)

        summary_list.append(formatted_summary)

    final_text = style_sheet

    final_text += "<br>".join(summary_list)

    final_text += closing_message

    return final_text


def format_sources(sources):
    sources_str = "Sources: "
    for i, src in enumerate(sources):
        a_tag = Template("[<a href='$source'>$index</a>] ").substitute(
            source=src, index=i + 1
        )
        sources_str += a_tag

    return sources_str


def format_summary(topic, summaries_obj):
    summaries_list = summaries_obj.summaries
    logging.info("summaries list", summaries_list)
    if len(summaries_list) == 0:
        return ""

    formatted_entries = []
    for entry in summaries_list:
        title = entry.title
        summary = entry.summary

        entry_template_table = Template(topic_entry_template)
        formatted_entry = entry_template_table.substitute(title=title, summary=summary)

        formatted_entries.append(formatted_entry)

    html_template = Template(topic_summary_template_table)
    formatted_text = html_template.substitute(
        topic=topic, entries="".join(formatted_entries)
    )

    return formatted_text
