"""
Example code for linker indexation calculations.


CPI Data

September 2017: 100.0
October 2017: 100.0
November 2017: 101.0
December 2017: 102.0


"""

import simplepricers.simple_calendar as simple_calendar

cal = simple_calendar.SimpleCalendar360()

import simplepricers.Quick2DPlot as Q2D


d = cal.GetDate(2017, 9, 1)
raw_dates = [d,]
for i in range(0,3):
    d = cal.AddMonths(d, 1)
    raw_dates.append(d)

# Now, add 3 months to incorporate lag
dates = [cal.AddMonths(x,3) for x in raw_dates]

valz = [100., 100., 101., 103.]

index = simple_calendar.Indexation()
index.SetIndexValues(dates, valz)

# Generate daily date vector
d = dates[0]
days = [d,]
for i in range(0, 80):
    d += 1./360.
    days.append(d)

daily_values = [index.GetValue(x) for x in days]

# Need to clean up x-axis
x_ticks = dates
x_labels = ['%.3f' % (x,) for x in x_ticks]
x_axis = [x_ticks, x_labels]

plt = Q2D.Quick2DPlot(days, daily_values, 'Daily Index Values', run_now=False)
plt.XTicks = x_axis
plt.DoPlot()

# Create annualised change
annual = []
for i in range(1, len(daily_values)):
    pchange = daily_values[i]/daily_values[i-1]
    pchange = pow(pchange, 360.) - 1.
    annual.append(pchange)
    print(pchange)


plt = Q2D.Quick2DPlot(days[1:], annual, 'Annualised Rate Of Change', run_now=False)
plt.XTicks = x_axis
plt.DoPlot()

