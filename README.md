# score-and-rank-contributors

A command-line tool to score and rank contributors
based on their activity over a set of projects
by analyzing Git histories.


## Requirements

- Git (1.7x or newer)
- Python >= 3.7
- GitPython (installed by `pip install GitPython`)

## Usage

The usage of the tool is summarized below:

```bash
python score_and_rank_contributors.py [--since since_date] [--authors author_list] project_1 ... project_N

```

## Basic Usage

The command extracts and accumulates contributor statistics
from the Git histories in the given project directories
`project_1`, ..., `project_N`.
Each author with a unique email address is treated
as a unique contributor
and scored according to his or her contribution statistics.
The command outputs a JSON array of contributors, ranked by score.

Here is an example command.

```bash
python score_and_rank_contributors.py --since 2022-01-01 --authors contributors.txt my_project
```

Here is an example output.

```json
[
   {
      "rank": 1,
      "name": "Tom",
      "score": 1000
   },
   {
      "rank": 2,
      "name": "Jerry",
      "score": 123
   },
   {
      "rank": 3,
      "name": "Spike",
      "score": 1
   }
]
```

## Optional Arguments

An optional `since_date` argument,
in `YYYY-MM-DD` format,
may be given
so that only the commits authored since `since_date` count.

An optional `author_list` argument may be given
to specify a text file,
where each line provides some extra information
about a contributor.

```
Contributor A <name_a1@comp_a1> <name_a2@comp_a2> <name_a3@comp_a3>
Contributor B's Display Name <name_b1@comp_b1>
```

Providing the `author_list` file serves two purposes.
First,
an individual may own multiple emails.
Without any assistance,
the tool has no way of knowing
that these different email addresses
belong to the same contributor.
Second,
a contributor may prefer the tool
to use a different display name
than the one in the Git history.

## Contribution Scores

A contributor owns a point for

1. Every commit that he or she authors;
2. Every 100 lines of additions or deletions that he or she authors.
