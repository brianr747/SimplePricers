"""
ex_20161016_discount_factors.py

Example code for discount factors.

"""


try:
    from simplepricers.utils import create_grid
    import simplepricers.yieldcalculations as yc
except ImportError:
    print('If these imports fail, put the base directory above onto the PYTHONPATH')
    raise

from plot_for_examples import Quick2DPlot

# ------------------------------------------------------
# Show discount factors
t = create_grid(0., 10., 1)
# Create flat zero curve
r = [0.05, ] * len(t)

df = yc.DF(t, r)
Quick2DPlot(t, df, 'Discount Factor For Flat 5% Curve')
# --------------------------------------------------------
print('Second example: calculate the NPV of a 2-year bond (4% annual coupon)')
# Time axis

t = create_grid(1., 2., 1)
# 4% zero rate
r = [.04, .04]
df = yc.DF(t, r)
CF = [4., 104.]
NPV = 0.
for i in range(0, len(t)):
    NPV += CF[i] * df[i]
print('NPV=', round(NPV, 4))

print('Cash flow Grid')
print('t', 'zerorate', 'DF', 'CF', 'NPV of CF')
for mat, zr, disc, c_f in zip(t, r, df, CF):
    print(mat, zr, disc, c_f, c_f * disc)
# --------------------------------------------------------
print('Third example: calculate the NPV of a 2-year bond (4% semi-annual coupon)')
print('Use same 4% zero rate.')
# Time axis
t = create_grid(.5, 2., 2)
# 4% zero rate
r = [.04, .04, .04, .04]
df = yc.DF(t, r)
CF = [2., 2., 2., 102.]
NPV = 0.
for i in range(0, len(t)):
    NPV += CF[i] * df[i]
print('NPV=', round(NPV, 4))

print('Cash flow Grid')
print('t', 'zerorate', 'DF', 'CF', 'NPV of CF')
for mat, zr, disc, c_f in zip(t, r, df, CF):
    print(mat, zr, disc, c_f, c_f * disc)
# --------------------------------------------------------
print('Fourth example: calculate the NPV of a 2-year bond (4% semi-annual coupon)')
print('Map the discount rate to semi-annual convention.')
# Time axis
t = create_grid(.5, 2., 2)
# Convert 4% semi-annual yield -> annual
r_a = pow(1.02, 2.) - 1.
print('4% semi-annual rate =', round(r_a, 5), '% annual rate')
r = [r_a, r_a, r_a, r_a]
df = yc.DF(t, r)
CF = [2., 2., 2., 102.]
NPV = 0.
for i in range(0, len(t)):
    NPV += CF[i] * df[i]
print('NPV=', round(NPV, 4))

print('Cash flow Grid')
print('t', 'zerorate', 'DF', 'CF', 'NPV of CF')
for mat, zr, disc, c_f in zip(t, r, df, CF):
    print(mat, zr, disc, c_f, c_f * disc)
# --------------------------------------------------------
print('Fifth example: calculate the NPV of a 2-year bond (4% annual coupon)')
print('Use a 4% exponential discount rate')
# Time axis
t = create_grid(1., 2., 1)
# 4% zero rate
r = [.04, .04]
df = yc.DF_exponential(t, r)
CF = [4., 104.]
NPV = 0.
for i in range(0, len(t)):
    NPV += CF[i] * df[i]
print('NPV=', round(NPV, 4))

print('Cash flow Grid')
print('t', 'zerorate', 'DF', 'CF', 'NPV of CF')
for mat, zr, disc, c_f in zip(t, r, df, CF):
    print(mat, zr, disc, c_f, c_f * disc)
