# src/visualization.py
import plotly.graph_objects as go

def animated_ci_band(ci_df):
    """
    Animated rolling CI band for mean returns.
    """
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=ci_df.index,
        y=ci_df["upper"],
        line=dict(width=0),
        showlegend=False,
        hoverinfo="skip"
    ))

    fig.add_trace(go.Scatter(
        x=ci_df.index,
        y=ci_df["lower"],
        fill="tonexty",
        fillcolor="rgba(0, 100, 255, 0.2)",
        line=dict(width=0),
        name="95% CI"
    ))

    fig.add_trace(go.Scatter(
        x=ci_df.index,
        y=ci_df["mean"],
        line=dict(color="blue", width=2),
        name="Rolling Mean"
    ))

    fig.update_layout(
        title="Rolling Mean Return with Bootstrap CI",
        xaxis_title="Date",
        yaxis_title="Mean Return",
        height=450
    )

    return fig
