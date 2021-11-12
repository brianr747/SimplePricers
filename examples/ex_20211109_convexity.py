"""
ex_20211109_convexity.py

Example code for "convexity" discussion.

As is discussed in the article that will be posted on my blog/substack around 2021-11-09, I am calculating
the change in the duration for 100 basis point shifts in yields. This shows the sensitivity of duration to
yield in an easier to interpret fashion than convexity. (Easier for me, anyway.)

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
# Work with a flat curve at "starting_yield" for maturities 1-50, bonds start as par coupons.

starting_yield = .03

maturities = [1,2,3,4,5,6,7,8,9,10,15,20,25,30,40,50]
durations = []
for i in maturities:
    cpn = bonds.CouponBond(mat=i, coupon=starting_yield, coupon_freq=1)
    durations.append(cpn.CalcDuration(starting_yield))

obj = Quick2DPlot(maturities, durations,  'Duration/Maturity For 3% Par Coupon', run_now=False,
                  filename='c20211109_convexity_1.png')
obj.XLabel = 'Maturity (Years)'
obj.YLabel = 'Duration'
obj.OutputDirectory = 'figures'
obj.DPI = 90
obj.DoPlot()

duration_up = []
duration_down = []
for i in range(0,len(maturities)):
    m = maturities[i]
    cpn = bonds.CouponBond(mat=m, coupon=starting_yield, coupon_freq=1)
    duration_up.append(cpn.CalcDuration(starting_yield+.01)-durations[i])
    duration_down.append(cpn.CalcDuration(starting_yield-.01)-durations[i])

obj = Quick2DPlot([maturities, maturities], [duration_up, duration_down],
                  'Duration/Maturity After Shocks', run_now=False,
                  filename='c20211109_convexity_2.png')
obj.XLabel = 'Maturity (Years)'
obj.YLabel = 'Duration Change'
obj.Legend = ['Shock +100 BPs.','Shock -100 BPs.']
obj.OutputDirectory = 'figures'
obj.DPI = 90
obj.DoPlot()

# calculate change per unit duration
unit_convexity = []
for i in range(0, len(maturities)):
    unit_convexity.append(duration_down[i]/durations[i])


obj = Quick2DPlot(maturities, unit_convexity,  'Duration Change Divided By Duration', run_now=False,
                  filename='c20211109_convexity_3.png')
obj.XLabel = 'Maturity (Years)'
obj.YLabel = 'Duration Change/Duration'
obj.OutputDirectory = 'figures'
obj.DPI = 90
obj.DoPlot()


