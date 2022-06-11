from src.series import PriceSeries, ChangeSeries
import matplotlib
from matplotlib import pyplot as plt
from src.modeling.linear_correlation import preceding_changes, correlation_p
from datetime import date
import numpy as np
import pandas as pd

matplotlib.use('TkAgg')


def set_plt_fullscreen():
    mng = plt.get_current_fig_manager()
    mng.resize(*mng.window.maxsize())


def apply_reversion_algo(cs: ChangeSeries):
    out = pd.DataFrame(index=cs.df.index, columns=['Change'])

    include_row = True

    for i, cols in cs.df.iterrows():
        out.at[i, 'Change'] = cols[0] if include_row else 1
        include_row = cols[0] < 1

    return ChangeSeries(out)


def annual_reversion(cs: ChangeSeries):
    for year in range(1994, 2022):
        year_changes = cs.slice(date(year, 1, 1), date(year + 1, 1, 1)).df['Change']
        print(
            year,
            np.corrcoef(year_changes.iloc[:-1], year_changes.iloc[1:])[0, 1],
            correlation_p(year_changes.iloc[:-1], year_changes.iloc[1:]),
        )


def reversion_backtesting(cs: ChangeSeries, transform=lambda s: s.cumulative()):
    set_plt_fullscreen()
    plt.title(f"{cs.first_day()} to {cs.last_day()}")

    rv = apply_reversion_algo(cs)

    series = [
        (cs, 'green'),
        (cs.leverage(2), 'blue'),
        (cs.leverage(3), 'purple'),
        (rv, 'yellow'),
        (rv.leverage(2), 'orange'),
        (rv.leverage(3), 'red'),
    ]

    for s, color in series:
        cumul = transform(s).df
        plt.plot(cumul.index.get_level_values('Date'), cumul['Gain'], color=color)

    plt.show()


def reversion_scatter(cs: ChangeSeries):
    print(correlation_p(cs.df['Change'].iloc[:-1], cs.df['Change'].iloc[1:]))
    print(np.corrcoef(cs.df['Change'].iloc[:-1], cs.df['Change'].iloc[1:]))
    plt.scatter(cs.df['Change'].iloc[:-1], cs.df['Change'].iloc[1:])
    plt.show()


def reversion_by_distance(cs: ChangeSeries):
    for days in range(1, 90):
        pc = preceding_changes(cs, days)

        print(days, pc.corr().at['Daily', 'Preceding'], correlation_p(pc['Preceding'], pc['Daily']))


def leveraged_spy_vs_upro():
    ps = PriceSeries.download("SPY")
    upro = PriceSeries.download("UPRO")
    ps = ps.slice(upro.first_day())

    cs = ps.to_changes().leverage(3).cumulative()
    cu = upro.to_changes().cumulative()

    plt.plot(cs.df['Gain'])
    plt.plot(cu.df['Gain'], color='green')

    plt.show()


if __name__ == "__main__":
    ps = PriceSeries.download("SPY")
    cs = ps.to_changes()

    # reversion_backtesting(cs)

    for year in range(1993, 2018):
        print(year)
        reversion_backtesting(cs.slice(date(year, 1, 1), date(year + 7, 1, 1)), transform=lambda s: s.dca())
