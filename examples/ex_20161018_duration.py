"""
ex_20161018_duration.py

Example code for duration.

"""

try:
    from simplepricers.utils import create_grid
    import simplepricers.yieldcalculations as yc
    import simplepricers.bonds_curves as bonds
except ImportError:
    print('If these imports fail, put the base directory above onto the PYTHONPATH')
    raise

from plot_for_examples import Quick2DPlot

# ------------------------------------------------------
# price/yield for consols vs. coupon bond

yield_grid = create_grid(.001, .05, 1000)
consol = bonds.Consol(.05)
consol_price = [None, ] * len(yield_grid)
# 5% 10-year annual coupon bond
cpn = bonds.CouponBond(10., .05, 1)
coupon_price = [None, ] * len(yield_grid)
for i in range(0, len(yield_grid)):
    consol_price[i] = consol.GetPrice(yield_grid[i])
    coupon_price[i] = cpn.GetPrice(yield_grid[i], price_type='dirty')

obj = Quick2DPlot(yield_grid, consol_price,  'Price-Yield Curve For 5% Consol', run_now=False)
obj.XLabel = 'Yield'
obj.YLabel = 'Price'
obj.DoPlot()

obj = Quick2DPlot(yield_grid, coupon_price,  'Price-Yield Curve For 10-year 5% Coupon Bond', run_now=False)
obj.XLabel = 'Yield'
obj.YLabel = 'Price'
obj.DoPlot()

obj = Quick2DPlot([yield_grid, yield_grid], [consol_price, coupon_price], 'Price-Yield Curves For Consol And 10-Year',
                  run_now=False)
obj.XLabel = 'Yield'
obj.YLabel = 'Price'
obj.Legend = ['5% Consol', '10-Year 5% coupon bond']
obj.DoPlot()

# -------------------------------------------------------
# duration yield relationship

yield_grid = create_grid(.01, .05, 1000)
consol = bonds.Consol(.05)
consol_dur = [None, ] * len(yield_grid)
# 5% 10-year annual coupon bond
cpn = bonds.CouponBond(10., .05, 1)
coupon_dur = [None, ] * len(yield_grid)
for i in range(0, len(yield_grid)):
    consol_dur[i] = consol.CalcDuration(yield_grid[i])
    coupon_dur[i] = cpn.CalcDuration(yield_grid[i])

obj = Quick2DPlot(yield_grid, coupon_dur,  'Duration of 10-year 5% Coupon Bond', run_now=False)
obj.XLabel = 'Yield'
obj.YLabel = 'Duration'
obj.DoPlot()

obj = Quick2DPlot([yield_grid, yield_grid], [consol_dur, coupon_dur], 'Duration For Consol And 10-Year',
                  run_now=False)
obj.XLabel = 'Yield'
obj.YLabel = 'Duration'
obj.Legend = ['5% Consol', '10-Year 5% coupon bond']
obj.DoPlot()