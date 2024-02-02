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

def extract_author_map(projects, since_date):
    git_authors_map = {}
    for project in projects:
        repo = Repo(project)
        for commit in repo.iter_commits(since=since_date):
            # use the latest name
            git_authors_map[commit.author.email] = commit.author.name
    return git_authors_map

# Define a function to calculate scores
def calculate_scores(projects, since_date):
    scores = defaultdict(int)
    for project in projects:
        repo = Repo(project)
        for commit in repo.iter_commits(since=since_date):
            if "Merge pull request #" in commit.message: 
                continue
            email = commit.author.email
            scores[email] += 1  # score for a commit
            scores[email] += math.ceil(commit.stats.total['lines'] / 100)  # score for line changes
    return scores

# Define a function to parse the authors file
def parse_authors_file(file_path):
    is_email_appeared = {} # we mush check there is no same email in the whole file.
    authors_map = {}
    with open(file_path, 'r') as file:
        for lid, line in enumerate(file):
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
            assert emailIdx > 0, "there must be at least one emails"

            #deal with email
            authors_map[(lid,name)] = []
            for part in parts[emailIdx:]:
                matched = re.match(r"<(.+?)>",part)
                assert matched
                email = matched.group(1)

                # check email has never appeared before.
                assert email not in is_email_appeared
                is_email_appeared[email] = 1

                authors_map[(lid,name)].append(email)
    return authors_map

# Define a function to rank and output data
def output_ranked_scores(scores, authors_map, same_authors):
    # merge the same contributors
    for (_, name), emails in same_authors.items():
        final_email = emails[0]
        for email in emails:
            authors_map[email] = name
            if email != final_email:
                scores[final_email] += scores[email]
                scores.pop(email,None)
    # blacklist
    scores.pop("action@github.com", None)

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    output = []
    for rank, (email, score) in enumerate(ranked, start=1):
        output.append({'rank': rank, 'name': authors_map[email], 'score': score})
    return json.dumps(output, indent=3)

def main():
    args = parse_args()
    authors_map = extract_author_map(args.projects, args.since)
    same_authors = parse_authors_file(args.authors) if args.authors else {}
    scores = calculate_scores(args.projects, args.since)
    print(output_ranked_scores(scores, authors_map, same_authors))

if __name__ == "__main__":
    main()
