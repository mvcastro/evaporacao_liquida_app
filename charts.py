import pandas as pd
import plotly.graph_objects as go


def get_plotly_fig(df: pd.DataFrame, title: str) -> go.Figure:
    
    fig = go.Figure()
    
    for col_name in df.columns:
       fig.add_trace(
           go.Scatter(
                x=df.index,
                y=df[col_name],
                mode='lines',
                name=col_name
            )
        )
    
    fig.update_layout(title=title)
    
    return fig
        