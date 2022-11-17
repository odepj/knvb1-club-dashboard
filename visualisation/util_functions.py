from datetime import datetime

import pandas as pd

from database.database import session


def calculate_delta(value: pd.Series, from_, to_):
    # pandas counterpart, but I feel the latter will become more useful.
    # diff = value.pct_change(periods=len(value) - 1)
    first = value.loc[from_][0]
    last = value.get(to_)[0]
    return round(abs(((first - last) / first) * 100), 1)


def calculate_mean_result_by_date(df: pd.DataFrame):
    if df['club_code'].nunique() > 1:
        club_code = 'mean'
    else:
        club_code = df['club_code'].drop_duplicates().values[0]

    df_mean = df.groupby(['datum', 'meting']).mean(numeric_only=False)
    df_mean['club_code'] = club_code
    df_mean['meting'], df_mean.index = df_mean.index.droplevel(0), df_mean.index.droplevel(1)
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
