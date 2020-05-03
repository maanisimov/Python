#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 13:49:43 2020

@author: maxim_anisimov
"""

#%%
class Bond:
    
    def __init__(self, principal, coupon_rate=None, coupon_payments=None,
                 cf_dates=None, cf_frequency=None, 
                 maturity_date=None, maturity=None,
                 last_payment_date='today',
                 type_='vanilla', days_convention=360):
        """
        This is the initializer that you can later use to instantiate objects. 
        __init__ must always be present! 
        It takes one argument: self, which refers to the object itself. 
        Inside the method, the pass keyword is used as of now, 
        because Python expects you to type something there. 
        Remember to use correct indentation!
        
        Bond definition:
        0) Principal
        1) coupon rate OR coupon payments
        2) cash flow dates OR cash flow frequency (monthy, quarterly, annual) & maturity (in years)
        3) last payment date
        """
        
        import numpy as np
        
        self.principal = principal
        
        if coupon_payments is None:
            self.coupon_rate = coupon_rate
        else:
            self.coupon_payments = coupon_payments
    
        
        today = np.datetime64('today')
        if last_payment_date == 'today':
            self.past_payment_date = today
        
        if cf_dates is not None:
            self.cf_dates = cf_dates
            self.maturity_date = self.cf_dates[-1]
            numpy_cf_dates = [np.datetime64(date) for date in self.cf_dates]
            
        elif (cf_frequency is not None) & ( (maturity_date is not None) | (maturity is not None) ):
            self.cf_frequency = cf_frequency
            
            if maturity_date is not None:
                self.maturity_date = maturity_date
            else:
                self.maturity_date = today + np.timedelta64(maturity, 'D')*days_convention
                
            if self.cf_frequency == 'monthly':
                delta = int(days_convention/12)
            elif self.cf_frequency == 'quarterly':
                delta = int(days_convention/4)
            elif self.cf_frequency == 'annual':
                delta = days_convention
            
            numpy_cf_dates = np.append([self.maturity_date])
            last_date = self.maturity_date
            while last_date > today:
                last_date -= delta
                numpy_cf_dates = np.append(last_date, numpy_cf_dates)
        
        # time difference and convert to float
        days_delta = (numpy_cf_dates - today) / np.timedelta64(1, 'D')
        self.years_delta = days_delta / days_convention
        
        dates = np.append(today, numpy_cf_dates)
        days_btw_payments = [dates[i]-dates[i-1] 
                             for i in range(1, len(dates))] / np.timedelta64(1, 'D')
        years_btw_payments = days_btw_payments / days_convention
        
        self.coupon_payments = np.array([self.coupon_rate * self.principal] *\
                                        len(self.cf_dates)*years_btw_payments)
        
        if type_ == 'vanilla':
            self.principal_payments = [0]*len(self.cf_dates)
            self.principal_payments[-1] += self.principal
            self.principal_payments = np.array(self.principal_payments)
        elif type_ == 'amortized':
            # TODO: handle amortized bonds
            pass
        
        self.cash_flows = self.coupon_payments + self.principal_payments
        
    def plot_cash_flows(self, *kwargs):
        
        import matplotlib.pyplot as plt
        import seaborn as sns
        sns.set()
        import pandas as pd
        
        df_payments = pd.DataFrame({'coupon': self.coupon_payments, 
                                    'principal': self.principal_payments},
                                    index = self.cf_dates)
        
        df_payments.plot(kind='bar', stacked=True, color=['green', 'orange'])
        plt.xlabel('Date')
        plt.ylabel('Amount')
        plt.title('Bond cash flows')
        plt.tight_layout()
        plt.show();
        
        
    def bondinfo(self):
        import pandas as pd
        df = pd.DataFrame({'Principal': self.principal,
                           'Coupon rate': self.coupon_rate},
                            index=['Parameter']).T
        return df
        
    def calculate_price(self, YTM=None, discount_rates=None, 
                        assign_price=False, days_convention=360):
        """
        Now that you have a class,
        it does have attributes, 
        but it doesn't actually do anything. 
        This is where instance methods come in.
        You can rewrite the class to now include a calculate_price() method. 
        Notice how the def keyword is used again, as well as the self argument.
        """
        import numpy as np
        
        if discount_rates is not None:
            price = np.sum( self.cash_flows/(1+discount_rates)**self.years_delta )
            if assign_price:
                self.price = price
            return price
        else:
            price = np.sum( self.cash_flows/(1+YTM)**self.years_delta )
            if assign_price:
                self.price = price
            return price
        
#%% Examples
bond = Bond(principal=100, coupon_rate=0.05, cf_dates=['2020-10-10', '2021-04-10'])
print(bond)
print(bond.principal)
print(bond.coupon_rate)
print(bond.cf_dates)
print(bond.coupon_payments)
print(bond.principal_payments)
print(bond.cash_flows)
#%%
bond.calculate_price(YTM=0.05)

#%%
bond.plot_cash_flows()

#%%
bond.cash_flows



