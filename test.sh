#! /bin/env bash
set -e

echo '''Alice <alice@comp.com>
Lam <lam@comp1.com> <lam@comp2.com>''' > author_list.txt

./score-and-rank-contributors --authors author_list.txt --since 2023-10-10 ./test-score-and-rank-contributors > actual.txt

echo '''[
   {
      "rank": 1,
      "name": "Alice",
      "score": 12
   },
   {
      "rank": 2,
      "name": "Lam",
      "score": 4
   }
]'''  > expected.txt

diff actual.txt expected.txt

rm author_list.txt actual.txt expected.txt