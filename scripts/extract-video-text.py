#!/usr/bin/env python3
"""
Extract the summaries and transcripts from GEMIS_case_study_videos.md verbatim.

The implementation prompt says the transcript on each story page must be copied
exactly and never edited. Typing them by hand does not survive that: a first pass
silently turned eight straight apostrophes into curly ones. So they are extracted
mechanically into scripts/video-text.json, which scripts/stories.py then reads.

    python3 scripts/extract-video-text.py path/to/GEMIS_case_study_videos.md

Writes scripts/video-text.json keyed by the video file stem.
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def extract(doc):
    out = {}
    for m in re.finditer(r'\n## \d+\. (.+?)\n(.*?)(?=\n## |\n---\n\n## Structured data)', doc, re.S):
        body = m.group(2)
        summary = re.search(r'\*\*Summary\.\*\*\s*(.+?)\n\n', body, re.S)
        transcript = re.search(r'\*\*Transcript\*\*\n\n> (.+?)\n', body, re.S)
        stem = re.findall(r'`([A-Za-z_]+)_web\.mp4`', body)
        if not (summary and transcript and stem):
            raise SystemExit(f'could not parse the section for {m.group(1)!r}')
        out[stem[0]] = {
            'title': m.group(1).strip(),
            'summary': summary.group(1).strip(),
            'transcript': transcript.group(1).strip(),
            'stem': stem[0],
        }
    if len(out) != 7:
        raise SystemExit(f'expected 7 videos, parsed {len(out)}')
    return out


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    data = extract(open(sys.argv[1], encoding='utf-8').read())
    path = os.path.join(HERE, 'video-text.json')
    json.dump(data, open(path, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print(f'wrote {path} — {len(data)} videos, verbatim')
