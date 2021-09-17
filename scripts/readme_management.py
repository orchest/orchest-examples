from datetime import datetime
from urllib.parse import urlparse
import aiohttp
import argparse
import asyncio
import json
import logging
import os
import re
import sys
import validators

MAX_DESCRIPTION_LENGTH = os.environ.get("MAX_DESCRIPTION_LENGTH", 280)
MAX_TAGS = os.environ.get("MAX_TAGS", 5)
MIN_TAGS = os.environ.get("MIN_TAGS", 1)
TOKEN = os.environ.get("GITHUB_TOKEN")
_ENTRY_ANCHOR = "<!--o-->"
_EXAMPLES_BEGIN_ANCHOR = "<!-- EXAMPLES_BEGIN -->"

logging.basicConfig(format="%(levelname)s:\n%(message)s")

# See https://github.com/actions/github-script/issues/1 :(.
def log_escaped_error(obj: any) -> str:
    string = str(obj)
    string = string.replace("'", "\\'")
    logging.error(string)


async def fetch(session, url):
    async with session.get(url) as response:
        json = await response.json()
        code= response.status
        return code, json


async def fetch_all(urls):
    headers = None
    if TOKEN is not None:
        headers = {"Authorization": f"token {TOKEN}"}

    async with aiohttp.ClientSession(headers=headers) as session:
        results = await asyncio.gather(
            *[fetch(session, url) for url in urls]
        )
        return results


def _parse_tags(tags: str):
    parsed_tags = []
    tags = tags.lstrip()
    if not tags.startswith("- "):
        log_escaped_error(f'Invalid tags (missing initial "- "):\n{tags}')
        sys.exit(1)
    tags = tags[2:].strip()
    if not re.match(r"^(`([^`]+)` )*(`([^`]+)`)?$", tags):
        log_escaped_error(f"Invalid tags:\n{tags}")
        sys.exit(1)
    parsed_tags = re.findall(r"`([^`]+)`", tags)

    if len(parsed_tags) < MIN_TAGS:
        log_escaped_error(f"Too few tags (at least {MIN_TAGS}): {parsed_tags}")
        sys.exit(1)
    if len(parsed_tags) > MAX_TAGS:
        log_escaped_error(f"Too many tags (max {MAX_TAGS}): {parsed_tags}")
        sys.exit(1)
    return parsed_tags


def _parse_title_url(title_url: str):
    title_url = title_url.strip()
    if not title_url.startswith("- "):
        log_escaped_error(f'Invalid title-url (missing initial "- "):\n{title_url}')
        sys.exit(1)
    title_url = title_url[2:]
    if not title_url.endswith(" -"):
        log_escaped_error(f'Invalid title-url (missing initial "- "):\n{title_url}')
        sys.exit(1)
    title_url = title_url[:-2].strip()

    title_re = r"\[([^(\[|\])]+)\]"
    email_re = r"\(.*\)$"
    title_url_re = fr"^{title_re}{email_re}"
    if not re.match(title_url_re, title_url):
        log_escaped_error(f"Invalid [title](url):\n{title_url}")
        sys.exit(1)

    parsed_title = re.findall(title_re, title_url)
    if len(parsed_title) > 1:
        log_escaped_error(f"Invalid [title](url):\n{title_url}")
        sys.exit(1)
    parsed_title = parsed_title[0]

    parsed_url = re.findall(email_re, title_url)
    if len(parsed_url) > 1:
        log_escaped_error(f"Invalid [title](url):\n{title_url}")
        sys.exit(1)
    parsed_url = parsed_url[0]
    # Remove parenthesis.
    parsed_url = parsed_url[1:-1]
    if not validators.url(parsed_url) or urlparse(parsed_url).netloc != "github.com":
        log_escaped_error(f"Invalid url:\n{parsed_url}")
        sys.exit(1)

    return parsed_title, parsed_url


def parse_entry(entry: str):
    if not entry.startswith("- "):
        log_escaped_error(f'Invalid entry (missing initial "- "):\n{entry}')
        sys.exit(1)
    anchor_indexes = [m.start() for m in re.finditer(_ENTRY_ANCHOR, entry)]
    if len(anchor_indexes) != 2:
        log_escaped_error(
            f'Invalid entry (must have exactly 2 "{_ENTRY_ANCHOR}")' f"\n{entry}"
        )
        sys.exit(1)

    idx1 = anchor_indexes[0]
    idx2 = anchor_indexes[1]

    title_url = entry[:idx1]
    title, url = _parse_title_url(title_url)
    description = entry[idx1:idx2].replace(_ENTRY_ANCHOR, "").strip()
    if len(description) > MAX_DESCRIPTION_LENGTH:
        log_escaped_error(
            "Description is longer than the max allowed value "
            f"{MAX_DESCRIPTION_LENGTH}:\n{description}"
        )
        sys.exit(1)

    tags = entry[idx2:].replace(_ENTRY_ANCHOR, "")
    tags = _parse_tags(tags)
    return {
        "description": description,
        "title": title,
        "url": url,
        "tags": tags,
    }


def _parse_file(file_path: str):
    parsed_entries = []
    entries = []
    with open(file_path) as file:
        found_anchor = False
        for line in file.readlines():
            if not found_anchor:
                found_anchor = _EXAMPLES_BEGIN_ANCHOR in line
                continue
            entries.append(line)

    for entry in entries:
        parsed_entries.append(parse_entry(entry))
    return parsed_entries


def _github_repo_url_to_api(url: str):
    return f"https://api.github.com/repos{urlparse(url).path}"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    help_msg = "main help"
    subparsers = parser.add_subparsers(
        title="subcommands",
        dest="command",
        description="Create or deploy Orchest AMIs.",
        help=help_msg,
    )

    help_msg = "Checks if the file is valid, returning 0 if so."
    check_file_parser = subparsers.add_parser("check_file_validity", help=help_msg)
    check_file_parser.add_argument("--file", type=str, required=True)

    help_msg = "Process the file, producing a new metadata file."
    process_file_parser = subparsers.add_parser("process_file", help=help_msg)
    process_file_parser.add_argument("--file", type=str, required=True)
    process_file_parser.add_argument("--output", type=str, required=True)
    args = parser.parse_args()

    if args.command == "check_file_validity":
        file_path = args.file
        _parse_file(file_path)
    elif args.command == "process_file":
        file_path = args.file
        output_path = args.output

        output_json = {"creation_time": datetime.utcnow().isoformat(), "entries": []}
        parsed_entries = _parse_file(file_path)
        # Don't make github angry.
        chunk_size = 5
        for i in range(0, len(parsed_entries), chunk_size):
            chunk = parsed_entries[i : i + chunk_size]
            urls = [_github_repo_url_to_api(e["url"]) for e in chunk]
            api_data = asyncio.run(fetch_all(urls))
            for entry, (code, api_data) in zip(chunk, api_data):
                
                if code != 200:
                    log_escaped_error(f"{entry} had an unexpected status code: "
                    f"{code}. Data: {api_data}.")
                    continue

                entry["owner"] = api_data["owner"]["login"]
                entry["forks_count"] = api_data["forks_count"]
                entry["stargazers_count"] = api_data["stargazers_count"]
                output_json["entries"].append(entry)
        with open(output_path, "w") as f:
            json.dump(output_json, f, sort_keys=True, indent=4)
