"""
ex20180216_breakeven.py

Breakeven inflation sample calculations.

Highly approximate, ignoring things like seasonality and calculation lags.

This example is referred to in a blog posting on BondEconomics.com, which will appear on 2018-02-21.
It will also be referred to in the upcoming report "Inflation Breakeven Analysis" by Brian Romanchuk. That
text explains what the calculations here are supposed to do.


Copyright 2018 Brian Romanchuk

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""


from simplepricers.Quick2DPlot import Quick2DPlot
from simplepricers.bonds_curves import CouponBond, ZeroCurve, InflationLinkedBond

# Have a simple zero curve
ZC = ZeroCurve([0., 10.], [.04, .06])

Quick2DPlot(ZC.Maturities, ZC.ZC, 'Zero Curve', output_directory='figures', filename='fig_breakeven01.png')

# All bonds are annual coupon
# Conventional bond, coupon = 8%
nom8 = CouponBond(10., .08, coupon_freq=1)
price8 = nom8.GetPriceFromZeroCurve(0., ZC, price_type='dirty')
print('Price of 8% coupon 10-year conventional = ', price8)
yield8 = nom8.GetYield(0., price8, price_type='dirty')
print('Yield of 8% conventional = {0:.4f}'.format(100.*yield8))

# Get the par coupon rate
par10 = ZC.CalcParCoupon(10)
print('10-year par coupon rate: {0:.3f}'.format(par10*100.))

linker = InflationLinkedBond(10., .04)
# Calculate the economic breakeven
break10 = linker.CalcEconomicBreakeven(0, 100., ZC, price_type='dirty')
print('Economic breakeven of 4% par linker = {0:.3}'.format(100.*break10))
print('Simple breakeven vs 8% coupon = {0:.3}'.format(100.*(yield8-.04)))
print('Simple breakeven vs nominal par coupon = {0:.3}'.format(100.*(par10-.04)))

# Look at off-par linker, with a yield of 4%
linker2 = InflationLinkedBond(10., .02)
price2 = linker2.GetPrice(.04, now=0.0, price_type='dirty')
break_2 = linker2.CalcEconomicBreakeven(0., price2, ZC, price_type='dirty')
print('Price of 2% coupon linker at 4% yield = {0:.4}'.format(price2))
print('Economic breakeven of 2% linker = {0:.3}'.format(100.*break_2))
