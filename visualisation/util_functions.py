from datetime import datetime

import pandas as pd

from database.database import session


def calculate_delta(value: pd.Series, from_, to_):
    # pandas counterpart, but I feel the latter will become more useful.
    # diff = value.pct_change(periods=len(value) - 1)
    first = value.loc[from_][0]
    last = value.get(to_)[0]
    return round(abs(((first - last) / first) * 100), 1)


def nearest(items, pivot):
    return min(items, key=lambda x: abs(x - pivot))


def calculate_mean_result_by_date(df: pd.DataFrame, columns):
    if df['bvo_naam'].nunique() > 1:
        bvo_naam = 'mean'
    else:
        bvo_naam = df['bvo_naam'].drop_duplicates().values[0]

    df_mean = df.groupby(['Testdatum', 'reeks_naam'])[columns].mean(numeric_only=False)
    df_mean['bvo_naam'] = bvo_naam
    df_mean['reeks_naam'], df_mean.index = df_mean.index.droplevel(0), df_mean.index.droplevel(1)
    return df_mean


def add_figure_rangeslider(fig):
    # Add range slider
    return fig.update_layout(
        xaxis=dict(
            rangeselector=dict(
                buttons=list([
                    dict(count=12,
                         label="laatste 2 metingen",
                         step="month",
                         stepmode="backward"),
                    dict(count=2.25,
                         label="laatste 5 metingen",
                         step="year",
                         stepmode="backward"),
                    dict(count=5,
                         label="laatste 10 metingen",
                         step="year",
                         stepmode="todate"),
                    dict(label="alle metingen",
                         step="all")
                ])
            ),
            rangeslider=dict(
                visible=True
            ),
            type="date"
        )
    )
