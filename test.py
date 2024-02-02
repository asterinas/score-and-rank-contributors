import unittest
import importlib.util
from git import Repo
import tempfile
import json
import os
from score_and_rank_contributors import calculate_scores,parse_authors_file,output_ranked_scores
class TestScoreAndRankContributors(unittest.TestCase):

    def test_parse_authors_file(self):
        # Mock author list as a string
        mock_author_list = "Contributor A <email1@example.com> <email2@example.com>\nContributor B <email3@example.com>"

        expected_result = {
            (0,"Contributor A"): ["email1@example.com","email2@example.com"],
            (1,"Contributor B"): ["email3@example.com"],
        }

        with open('temp_author_list.txt', 'w') as file:
            file.write(mock_author_list)

        # Test the function
        result = parse_authors_file('temp_author_list.txt')
        self.assertEqual(result, expected_result)

        # Clean up
        os.remove('temp_author_list.txt')
        
    def test_calculate_scores(self):
        repo_url = "https://github.com/anminliu/score-and-rank-contributors.git"
        actual_scores = None
        with tempfile.TemporaryDirectory() as tmpdirname:
            repo = Repo.clone_from(repo_url,tmpdirname)
            repo.git.checkout('6825c8c833a4946d23504ad68e7a1abb4744974c')
            projects = [tmpdirname]
            since = None
            actual_scores = calculate_scores(projects,since)
        expected_scores = {
            "liuanmin.lam@antgroup.com": 4,
            "tate.thl@antgroup.com": 4,
            "tatetian@gmail.com": 4,
        }
        # Assert statements to check if the results are as expected
        self.assertEqual(expected_scores, actual_scores)

    def test_output_ranked_scores(self):
        scores = {
            "email1@example.com": 10,
            "email2@example.com": 11,
            "email3@example.com": 20,
            "action@github.com": 100,
        }
        same_authors = {
            (0,"Contributor A"): ["email1@example.com","email2@example.com"],
            (1,"Contributor B"): ["email3@example.com"],
        }
        authors_map = {
            "email1@example.com": "alice",
            "email2@example.com": "bob",
            "email3@example.com": "candy",
            "action@github.com": "Github Action",
        }

        expected_results = json.dumps([
            {"rank": 1, "name": "Contributor A", "score": 21},
            {"rank": 2, "name": "Contributor B", "score": 20},
        ],indent=3)
        actual_results = output_ranked_scores(scores,authors_map,same_authors)
        self.assertEqual(expected_results,actual_results)

if __name__ == '__main__':
    unittest.main()
