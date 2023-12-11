import unittest
from gradescope_utils.autograder_utils.json_test_runner import JSONTestRunner

# This will run any testing scripts it can find and then writes all the results to the 
# results.json 
if __name__ == '__main__':
    suite = unittest.defaultTestLoader.discover('tests')
    with open('/autograder/results/results.json', 'w') as f:
        JSONTestRunner(visibility='visible', stream=f).run(suite)
