# Introduction

This is a small script that ports your [Org Roam](https://www.orgroam.com/) notes to [Obsidian](https://obsidian.md/). It is inspired by https://github.com/goshatch/orgroam_to_obsidian but this doesn't rely on the sqlite DB, it just processes files. Feel free to add PRs or sugest improvements.

# Usage

2. Copy all org files of your Org Roam to the `input` folder
3. Run `poetry run python convert.py` 
4. Copy contents of `output` in a folder in Obsidian
