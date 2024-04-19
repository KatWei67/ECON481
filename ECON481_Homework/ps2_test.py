from ECON481_PS2sub import *
import numpy as np
from scipy.optimize import minimize
import re
import requests

rng = np.random.default_rng(seed=1)

X = rng.normal(scale=np.sqrt(2), size = (1000, 3))
y = 5 + X @ np.array([3.,2.,6.]) + rng.standard_normal(1000)

def test_github():
    url = github()
    repo_url = re.search('github\\.com/(.+)/blob', url).group(1)
    req = requests.get(f'https://api.github.com/repos/{repo_url}/stats/participation')
    assert req.json()['all'][-1] > 0

def test_simulation_shapes():
    assert simulate_data()[0].shape in [(1000,), (1000,1)]
    assert simulate_data()[1].shape == (1000,3)

def test_simulation_means():
    assert np.allclose(np.mean(simulate_data()[0]), 5., atol=3*np.sqrt(((9+4+36)*2+1)/1000), rtol=0)
    assert np.allclose(np.mean(simulate_data()[1]), 0., atol=3*np.sqrt(2/3000), rtol=0)

def test_simulation_vars():
    assert np.allclose(np.var(simulate_data()[0]), (9+4+36)*2+1, rtol=.1, atol=0)

def test_mle_coef_shape():
    assert estimate_mle(y,X).shape in [(4,), (4,1)]

def test_mle_coef_vals():
    assert np.allclose(estimate_mle(y,X).flatten(), np.array([5., 3., 2., 6.]), atol=0, rtol=.25)

def test_mle_coef_vals_unseen():
    beta = np.array([6., 5, -5, 2])
    y_new = beta[0] + X @ beta[1:] + rng.normal(size=1000,scale=3)
    assert np.allclose(estimate_mle(y_new, X).flatten(), beta, atol=0, rtol=.25)

def test_mle_coef_vals_unseen_2():
    beta = np.array([1., -2, -1., 2])
    y_new = beta[0] + X @ beta[1:] + rng.normal(size=1000,scale=3)
    assert np.allclose(estimate_mle(y_new, X).flatten(), beta, atol=0, rtol=.25)

def test_ols_coef_shape():
    assert estimate_ols(y,X).shape in [(4,), (4,1)]

def test_ols_coef_vals():
    assert np.allclose(estimate_ols(y,X).flatten(), np.array([5., 3., 2., 6.]), atol=0, rtol=.25)

def test_ols_coef_vals_unseen():
    beta = np.array([6., 5, -5, 2])
    y_new = beta[0] + X @ beta[1:] + rng.normal(size=1000,scale=3)
    assert np.allclose(estimate_ols(y_new, X).flatten(), beta, atol=0, rtol=.25)

def test_ols_coef_vals_unseen_2():
    beta = np.array([1., -2, -1., 2])
    y_new = beta[0] + X @ beta[1:] + rng.normal(size=1000,scale=3)
    assert np.allclose(estimate_ols(y_new, X).flatten(), beta, atol=0, rtol=.25)