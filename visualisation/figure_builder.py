import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def calculate_delta(value: pd.Series, from_, to_):
    diff = value.pct_change(
        periods=len(value) - 1)  # - pandas counterpart, but I feel the latter will become more useful.
    first = value.loc[from_][0]
    last = value.get(to_)[0]
    d = abs(((first - last) / first) * 100)
    return round(d, 1)


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


def line_figure_builder(df: pd.DataFrame, x: list, y: list, color: str):
    # TODO: fix colours, fill area between lines if they're a pair
    return go.Line(
        df,
        x=x,
        y=y,
        hue=color,
        # markers=True,
        # line_shape='spline'
    )


def indicator_builder(df, delta, name):
    s = df[delta]
    delta = calculate_delta(s, from_=s.iloc[:1].index, to_=s.iloc[-1:].index)
    return go.Indicator(
        mode='number+delta',
        value=delta,
        number={'suffix': " %"},
        title={'text': f"<br><span style='font-size:0.7em;color:gray'>{name}</span>"},
        # delta={'position': "bottom", 'reference': delta, 'relative': False}
    )
