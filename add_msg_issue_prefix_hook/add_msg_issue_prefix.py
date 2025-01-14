#!/usr/bin/env python3

import argparse
import re
import subprocess


def get_ticket_id_from_branch_name(branch):
    matches = re.findall("[a-zA-Z]{1,10}-[0-9]{1,5}", branch)
    if len(matches) > 0:
        return matches[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("commit_msg_filepath")
    args = parser.parse_args()
    commit_msg_filepath = args.commit_msg_filepath

    branch = ""
    try:
        branch = subprocess.check_output(["git", "symbolic-ref", "--short", "HEAD"], universal_newlines=True).strip()
    except Exception as e:
        print(e)

    if result := get_ticket_id_from_branch_name(branch):
        issue_number = result.upper()
    else:
        issue_number = ""
    with open(commit_msg_filepath, "r+") as f:
        content = f.read()
        content_subject = content.split("\n", maxsplit=1)[0].strip()
        f.seek(0, 0)
        if issue_number and issue_number not in content_subject:
            content_list = content.split(":", 1)
            if len(content_list) == 1:
                content_list.insert(0, "")

            f.write(f"{content_list[0]}({issue_number}):{content_list[1]}")
        else:
            f.write(content)


if __name__ == "__main__":
    exit(main())
