#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 18:57:51 2020

@author: maxim_anisimov
"""

#%% LIBRARIES
import numpy as np

"""
Few specifications of numpy.dot:

If both a and b are 1-D (one dimensional) arrays -- Inner product of two vectors (without complex conjugation)
If both a and b are 2-D (two dimensional) arrays -- Matrix multiplication
If either a or b is 0-D (also known as a scalar) -- Multiply by using numpy.multiply(a, b) or a * b.
If a is an N-D array and b is a 1-D array -- Sum product over the last axis of a and b.
If a is an N-D array and b is an M-D array provided that M>=2 -- Sum product over the last axis of a and the second-to-last axis of b:
Also, dot(a, b)[i,j,k,m] = sum(a[i,j,:] * b[k,:,m])
"""

#%%
def GMV_portfolio(returns_cov_matrix):
    
    iota = np.ones((returns_cov_matrix.shape[0],1))

    scaling_factor = 1/(iota.T @ np.linalg.inv(returns_cov_matrix) @ iota)[0,0]
    weights = scaling_factor * np.dot(np.linalg.inv(returns_cov_matrix), iota)
    
    return weights

# Example
Sigma = np.matrix([[1, 2],
                   [2, 9]])
GMV_portfolio(Sigma)


def MV_portfolio(target_excess_return, excess_ret_mean, excess_ret_cov_matrix):

    scaling_factor = target_excess_return/\
    (excess_ret_mean.T @ np.linalg.inv(excess_ret_cov_matrix) @ excess_ret_mean)[0,0]
    weights = scaling_factor * np.dot(np.linalg.inv(excess_ret_cov_matrix), excess_ret_mean)
    
    return weights

# Example
Sigma_excess = np.matrix([[1, 2],
                          [2, 9]])
mu_excess = np.matrix([[3], 
                       [5]])
MV_portfolio(10, mu_excess, Sigma_excess)


def Tan_portfolio(excess_ret_mean, excess_ret_cov_matrix):
    
    iota = np.ones((excess_ret_cov_matrix.shape[0],1))

    scaling_factor = 1/(iota.T @ np.linalg.inv(excess_ret_cov_matrix) @ excess_ret_mean)[0,0]
    weights = scaling_factor * np.dot(np.linalg.inv(excess_ret_cov_matrix), excess_ret_mean)
    
    return weights

# Example
Sigma_excess = np.matrix([[1, 2],
                          [2, 9]])
mu_excess = np.matrix([[3], 
                       [5]])
Tan_portfolio(mu_excess, Sigma_excess)
