#! /usr/bin/env python

# Import required libraries
import argparse
import math
import json
import re
from git import Repo
from collections import defaultdict

# Define a function to parse command-line arguments
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--since', type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('--authors', type=str, help='Path to authors file')
    parser.add_argument('projects', nargs='+', help='List of project directories')
    return parser.parse_args()

# Define a function to calculate scores
def calculate_scores(projects, since_date, authors_map):
    scores = defaultdict(int)
    for project in projects:
        repo = Repo(project)
        for commit in repo.iter_commits(since=since_date):
            email = commit.author.email
            author = authors_map.get(email, email)
            scores[author] += 1  # score for a commit
            scores[author] += math.ceil(commit.stats.total['lines'] / 100)  # score for line changes
    return scores

# Define a function to parse the authors file
def parse_authors_file(file_path):
    authors_map = {}
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split()
            name = []
            emailIdx = 0
            # deal with name
            for idx, part in enumerate(parts):
                matched = re.match(r"<(.+?)>",part)
                if matched:
                    emailIdx = idx
                    break
                name.append(part)
            name = " ".join(name)
            #deal with email
            for part in parts[emailIdx:]:
                matched = re.match(r"<(.+?)>",part)
                assert matched
                authors_map[matched.group(1)] = name
    return authors_map

# Define a function to rank and output data
def output_ranked_scores(scores):
    # blacklist
    scores.pop("Github Action", None)
    scores.pop("action@github.com", None)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    output = []
    for rank, (name, score) in enumerate(ranked, start=1):
        output.append({'rank': rank, 'name': name, 'score': score})
    return json.dumps(output, indent=3)

def main():
    args = parse_args()
    # create a email-name map in advance and update it use args.authors
    authors_map = parse_authors_file(args.authors) if args.authors else {}
    scores = calculate_scores(args.projects, args.since, authors_map)
    print(output_ranked_scores(scores))

if __name__ == "__main__":
    main()
