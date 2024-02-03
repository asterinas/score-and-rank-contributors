#! /bin/env bash
set -e

echo '''Alice <alice@comp.com>
Lam <lam@comp1.com> <lam@comp2.com>''' > author_list.txt

./score-and-rank-contributors --authors author_list.txt --since 2023-10-10 ./alice-and-lam > actual.txt

echo '''[
   {
      "rank": 1,
      "name": "Alice",
      "score": 17
   },
   {
      "rank": 2,
      "name": "Lam",
      "score": 6
   }
]'''  > expected.txt

diff actual.txt expected.txt

rm author_list.txt actual.txt expected.txt