from src.series import PriceSeries
from src.utils.date_utils import get_quarters
from tabulate import tabulate
from src.utils.display_utils import as_percent
from tqdm import tqdm

if __name__ == "__main__":
    ps = PriceSeries.download("SPY")
    cs = ps.to_changes()
    ls = [cs.leverage(i) for i in range(1, 4)]
    gs = [l.cumulative() for l in ls]

    rows = [(
        'Quarter',
        '1x returns', '1x ATH',
        '2x returns', '2x ATH',
        '3x returns', '3x ATH',
        # '1x 1Q change', '2x 1Q change', '3x 1Q change',
    )]

    total_quarters = 0
    quarters_losing = 0
    quarters_losing_leveraged = 0
    quarters_losing_against_unleveraged = 0
    cumulative_losing_against_spy = 0
    cumulative_2x_beats_3x = 0

    for qstart, qend, qname in tqdm(list(get_quarters(cs.first_day()))):
        qgs = [g.slice(ps.first_day(), qend) for g in gs]
        g1, g2, g3 = [c.slice(qstart, qend).gain() for c in ls]
        c1, c2, c3 = [float(qg.seek_date(qg.last_day())['Gain']) for qg in qgs]
        a1, a2, a3 = [qg.max() for qg in qgs]

        rows.append((
            qname,
            *[
                as_percent(x)
                for x in (c1, a1, c2, a2, c3, a3)
            ]
        ))

        total_quarters += 1
        if g1 < 1:
            quarters_losing += 1
        if g3 < 1:
            quarters_losing_leveraged += 1
        if g3 < g1:
            quarters_losing_against_unleveraged += 1
        if c2 > c3:
            cumulative_2x_beats_3x += 1

    print(tabulate(rows))

    print(f"There were {total_quarters} quarters.")
    print(f"There were {quarters_losing} quarters in which SPY lost value.")
    print(f"There were {quarters_losing_leveraged} quarters in which the leveraged ETF lost value.")
    print(f"There were {quarters_losing_against_unleveraged} quarters in which the leveraged ETF underperformed SPY.")
    print(f"2x cumulatively outperformed 3x in {cumulative_2x_beats_3x} quarters.")

    for i in range(1, 4):
        print(i, as_percent(cs.leverage(i).gain()))
