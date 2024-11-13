# layouts.py
# import dash_core_components as dcc
# import dash_html_components as html


import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import index
import us_map, state_comparison, custom_rate, index


index_layout = index.layout

us_map_layout = us_map.layout


state_comparison_layout = state_comparison.layout
custom_rate_layout = custom_rate.layout