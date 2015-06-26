import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


def supernova_light_curve(supernova):
    x = [snm.time.date() for snm in supernova.supernovamagnitude_set.all()]
    y = [snm.magnitude for snm in supernova.supernovamagnitude_set.all()]
    plt.title("{0} Observations".format(supernova))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    plt.gca().xaxis.set_minor_locator(mdates.DayLocator(bymonthday=range(2, 32), interval=7))
    # plt.gca().xaxis.set_minor_locator(ticker.IndexLocator(1, 0))
    plt.gca().xaxis.set_minor_formatter(mdates.DateFormatter('%d'))
    plt.gca().grid(True)
    plt.xlabel("Date")
    plt.ylabel("Magnitude")
    plt.plot(x, y, 'o')
    plt.ylim([0, max(y) + 5])
    plt.xlim([min(x) - datetime.timedelta(days=31), max(x) + datetime.timedelta(days=31)])
    plt.gca().invert_yaxis()
    plt.gcf().autofmt_xdate()
    return plt
