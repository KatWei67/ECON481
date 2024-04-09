from ECON481_PS1 import *
import numpy as np
import re
import requests

def test_github():
    url = github()
    repo_url = re.search('github\\.com/(.+)/blob', url).group(1)
    req = requests.get(f'https://api.github.com/repos/{repo_url}/stats/participation')
    assert req.json()['all'][-1] > 0

def test_evens_odds_names():
    assert len(evens_and_odds(4).keys()) == len(['evens', 'odds'])
    assert sorted(evens_and_odds(4).keys()) == sorted(['evens', 'odds'])

def test_evens_odds_4():
    assert evens_and_odds(4)['evens'] == 2
    assert evens_and_odds(4)['odds'] == 4

def test_evens_odds_20():
    assert evens_and_odds(20)['evens'] == 90
    assert evens_and_odds(20)['odds'] == 100

def test_reverse_a_b_c():
    assert reverse(['a', 'b', 'c']) == ['c', 'b', 'a']

def test_reverse_1_10():
    assert reverse(list(range(10))) == [9,8,7,6,5,4,3,2,1,0]

def test_time_diff_ps():
    assert time_diff('2020-01-01', '2020-01-02', 'float') == 1

def test_time_diff_ps_default():
    assert time_diff('2020-01-01', '2020-01-02') == 1

def test_time_diff_ps_2():
    assert time_diff('2020-01-03', '2020-01-01', 'string') == "There are 2 days between the two dates"

def test_binom():
    assert np.allclose(prob_k_heads(1,1), .5)

def test_binom_2():
    assert np.allclose(prob_k_heads(4,2), 6 * .5**4)

def test_binom_sum():
    assert np.allclose(np.sum([prob_k_heads(10,x) for x in range(11)]), 1.)

def test_binom_sum2():
    assert np.allclose(np.sum([prob_k_heads(100,x) for x in range(101)]), 1.)
