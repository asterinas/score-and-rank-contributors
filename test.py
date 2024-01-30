import unittest
import importlib.util
from git import Repo
import tempfile
import os
from score_and_rank_contributors import calculate_scores,parse_authors_file
# score_and_rank_contributors = importlib.import_module("score-and-rank-contributors")

# calculate_scores = score_and_rank_contributors.calculate_scores
# parse_authors_file = score_and_rank_contributors.parse_authors_file

class TestScoreAndRankContributors(unittest.TestCase):

    def test_parse_authors_file(self):
        # Mock author list as a string
        mock_author_list = "Contributor A <email1@example.com> <email2@example.com>\nContributor B <email3@example.com>"

        # Expected result
        expected_result = {
            "email1@example.com": "Contributor A",
            "email2@example.com": "Contributor A",
            "email3@example.com": "Contributor B"
        }

        # Write mock_author_list to a temporary file
        with open('temp_author_list.txt', 'w') as file:
            file.write(mock_author_list)

        # Test the function
        result = parse_authors_file('temp_author_list.txt')

        # Check if the result matches the expected result
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
            authors_map = {
                "liuanmin.lam@antgroup.com": "Anmin Liu",
                "tate.thl@antgroup.com": "tatetian",
                "tatetian@gmail.com": "tatetian",
            }
            actual_scores = calculate_scores(projects,since,authors_map)
        expected_scores = {
            "Anmin Liu": 4,
            "tatetian": 8,
        }
        # Assert statements to check if the results are as expected
        self.assertEqual(expected_scores, actual_scores)

if __name__ == '__main__':
    unittest.main()
