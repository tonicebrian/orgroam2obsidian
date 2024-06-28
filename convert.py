#!/usr/bin/env python3

import os
import re
import shlex

import subprocess

INPUT_FOLDER = 'input'
OUTPUT_FOLDER = 'output'


class Note:
    def __init__(self, id, title, filename):
        self.id = id
        self.title = title
        self.filename = filename


def process_file(filename: str):
    id_pattern = r':ID:\s+([a-f0-9\-]+)'
    title_pattern = r'\#\+title:\s+(.+)'
    regexes = [id_pattern, title_pattern]
    results = []
    with open(filename, 'r') as fd:
        current_pattern = regexes.pop(0)
        for line in fd.readlines():
            match = re.search(current_pattern, line)
            if match:
                results.append(match.group(1))
                if not regexes:
                    break
                current_pattern = regexes.pop(0)

        if len(results) != 2:
            return None
        else:
            return Note(results[0], results[1], filename)


def sanitize_filename(filename):
    # Define a pattern to match invalid characters
    sanitized_filename = re.sub(r'[\'<>:"/\\|?*\x00-\x1F]', '-', filename)
    return sanitized_filename


def replace_links(second_brain, match):
    link_text = match.group(1)
    link_target = match.group(2)
    # Combine parts in a different order or transform them
    if link_target.startswith("id:"):
        target_note_id = link_target.removeprefix('id:')
        target_note = second_brain.get(target_note_id)
        if target_note:
            return f"[[{sanitize_filename(target_note.title)}]]"
        else:
            return f"[Note not found: {link_text}]({link_target})"
    else:
        return f"[{link_text}]({link_target})"


if __name__ == "__main__":
    second_brain = {}

    print("Processing files")
    for file in (f for f in os.listdir(INPUT_FOLDER) if f.endswith('org')):
        note = process_file(f"{INPUT_FOLDER}/{file}")
        if note:
            second_brain[note.id] = note

    print("Transforming Files")
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)
    for _, note in second_brain.items():
       cmd = f"pandoc -f org -t markdown --wrap=none '{note.filename}' -o '{OUTPUT_FOLDER}/{sanitize_filename(note.title)}.md'"
       subprocess.run(shlex.split(cmd))

    print("Transforming Links")
    link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    for file in (f for f in os.listdir(OUTPUT_FOLDER) if f.endswith('md')):
        print(f"Processing file: {file}")
        with open(f"{OUTPUT_FOLDER}/{file}", 'r') as fd:
            content = fd.read()
            new_content = re.sub(link_pattern, lambda m: replace_links(second_brain, m), content)
        with open(f"{OUTPUT_FOLDER}/{file}", 'w') as fd:
            fd.write(new_content)





