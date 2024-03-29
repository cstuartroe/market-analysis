import datetime

from src.series import PriceSeries, ChangeSeries
import matplotlib
from matplotlib import pyplot as plt
from src.modeling.linear_correlation import preceding_changes, correlation_p
from datetime import date
import numpy as np
import pandas as pd
from tabulate import tabulate

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
    plt.title(f"{cs.first_day()} to {cs.last_day()}")

    rv = apply_reversion_algo(cs)

    series = [
        # (cs.leverage(0), 'gray'),
        # (cs, 'green'),
        (cs.leverage(2), 'blue'),
        # (cs.leverage(3), 'purple'),
        # (rv, 'yellow'),
        (rv.leverage(2), 'orange'),
        # (rv.leverage(3), 'red'),
    ]

    for s, color in series:
        cumul = transform(s).df
        plt.plot(cumul.index.get_level_values('Date'), cumul['Gain'], color=color)

    # level_line = 2000000
    # plt.plot((cs.first_day(), cs.last_day()), (level_line, level_line), color='black')


def reversion_scatter(cs: ChangeSeries):
    print(correlation_p(cs.df['Change'].iloc[:-1], cs.df['Change'].iloc[1:]))
    print(np.corrcoef(cs.df['Change'].iloc[:-1], cs.df['Change'].iloc[1:]))
    plt.scatter(cs.df['Change'].iloc[:-1], cs.df['Change'].iloc[1:])


def reversion_by_distance(cs: ChangeSeries):
    for days in range(1, 90):
        pc = preceding_changes(cs, days)

        print(
            days,
            round(pc.corr().at['Daily', 'Preceding'], 3),
            correlation_p(pc['Preceding'], pc['Daily']),
        )


def reversion_by_asset(assets: list[str]):
    rows = [("Asset", "Correlation", "p-value")]

    for asset in assets:
        ps = PriceSeries.download(asset)
        cs = ps.to_changes()

        pc = preceding_changes(cs, 1)

        rows.append((
            asset,
            round(pc.corr().at['Daily', 'Preceding'], 3),
            correlation_p(pc['Preceding'], pc['Daily']),
        ))

    print(tabulate(rows))


def rolling_reversion(cs: ChangeSeries):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    cumul = cs.cumulative()
    ax1.plot(cumul.df.index.get_level_values("Date"), cumul.df['Gain'], color='black')

    def reversion_correlation(df):
        pc = preceding_changes(ChangeSeries(df), 1)
        return pc.corr().at['Daily', 'Preceding']

    rolling_reversions = cs.rolling_stat(reversion_correlation, window=260)

    ax2.plot(
        rolling_reversions.index.get_level_values('Date'),
        rolling_reversions['Transformed'],
        color='red',
    )


def leveraged_spy_vs_upro():
    ps = PriceSeries.download("SPY")
    upro = PriceSeries.download("UPRO")
    ps = ps.slice(upro.first_day())

    cs = ps.to_changes().leverage(3).cumulative()
    cu = upro.to_changes().cumulative()

    plt.plot(cs.df['Gain'])
    plt.plot(cu.df['Gain'], color='green')


def long_term_reversion(cs: ChangeSeries, lookback: int, lookforward: int, jump: int):
    fd, ld = cs.first_day(), cs.last_day()
    day_delta = (ld - fd).days

    changes_before = []
    changes_after = []

    for i in range(lookback, day_delta - lookforward + 1, jump):
        midpoint = fd + datetime.timedelta(days=i)
        start = midpoint - datetime.timedelta(days=lookback)
        end = midpoint + datetime.timedelta(days=lookforward)
        cb = cs.slice(start, midpoint).cumulative().total_gain()
        ca = cs.slice(midpoint, end).cumulative().total_gain()
        print(start, cb, midpoint, ca, end)

        changes_before.append(cb)
        changes_after.append(ca)

    plt.scatter(changes_before, changes_after)


ASSETS = [
    "SPY",
    "UPRO",
    "QQQ",
    "TQQQ",
    "VOO",
    "VT",
    "VTI",
    "GOOG",
    "AMZN",
    "TSLA",
    "AMD",
    "AAPL",
    "BABA",
    "MSFT",
    "JNJ",
    "META",
    "V",
    "WMT",
    "MA",
    "CVX",
    "F",
    "HD",
    "LLY",
    "SCHW",
    "CVS",
    "TD",
    "IBM",
]


if __name__ == "__main__":
    ps = PriceSeries.download("SPY")
    cs = ps.to_changes()

    long_term_reversion(cs, 365, 365, 181)

    set_plt_fullscreen()
    plt.show()

    # for year in range(1993, 2017):
    #     set_plt_fullscreen()
    #     sliced_changes = cs.slice(date(year, 1, 1))
    #     reversion_backtesting(sliced_changes, transform=lambda s: s.dca(250))
    #     plt.show()

