from bokeh.plotting import figure, curdoc
from bokeh.models import ColumnDataSource, Select, TextInput, Button, DataTable, TableColumn, Paragraph, Div
from bokeh.layouts import column, row
import pandas as pd
import numpy as np

# Global data file
DATA_FILE = "clean.csv"

def load_data():
    try:
        return pd.read_csv(DATA_FILE)
    except:
        return pd.DataFrame({
            'x': np.random.randn(1000),
            'y': np.random.randn(1000),
            'z': np.random.randn(1000)
        })

# Load initial data
df = load_data()
current_start = 0
num_samples = 100

# Data source
source = ColumnDataSource(data=dict(index=[], x=[], y=[], z=[]))

# Widgets
chart_type = Select(title="Chart Type", value="Line", options=["Line", "Scatter", "Histogram"])
variable_select = Select(title="Variable", value="x", options=["x", "y", "z", "All"])
samples_input = TextInput(title="Samples to Show", value="100")
prev_button = Button(label="Previous", button_type="default")
next_button = Button(label="Next", button_type="default")
status_text = Paragraph(text=f"Showing samples {current_start} to {current_start+num_samples} of {len(df)}")
title_div = Div(text="<h1>Gyroscope Data Dashboard</h1>")

# Plot
p = figure(title="Gyroscope Data", width=800, height=400, tools="pan,box_zoom,reset,save")

# Data table
columns = [
    TableColumn(field="index", title="Index"),
    TableColumn(field="x", title="X"),
    TableColumn(field="y", title="Y"),
    TableColumn(field="z", title="Z"),
]
data_table = DataTable(source=source, columns=columns, width=800, height=200)

# Update function
def update_data():
    global df, current_start, num_samples
    try:
        df = load_data()  # reload each time
        num_samples = int(samples_input.value)
        if num_samples < 1:
            num_samples = 1
        elif num_samples > len(df):
            num_samples = len(df)

        if current_start + num_samples > len(df):
            current_start = len(df) - num_samples

        end_idx = current_start + num_samples
        new_data = dict(
            index=df.index[current_start:end_idx],
            x=df['x'][current_start:end_idx],
            y=df['y'][current_start:end_idx],
            z=df['z'][current_start:end_idx]
        )
        source.data = new_data
        status_text.text = f"Showing samples {current_start} to {end_idx} of {len(df)}"
        update_chart(None, None, None)
    except Exception as e:
        status_text.text = f"Error updating data: {str(e)}"

def update_chart(attr, old, new):
    p.renderers.clear()
    p.legend.items = []

    if chart_type.value == "Line":
        if variable_select.value == "All":
            p.line('index', 'x', source=source, color="blue", legend_label="X")
            p.line('index', 'y', source=source, color="red", legend_label="Y")
            p.line('index', 'z', source=source, color="green", legend_label="Z")
        else:
            p.line('index', variable_select.value, source=source, color="blue")
    elif chart_type.value == "Scatter":
        if variable_select.value == "All":
            p.scatter('index', 'x', source=source, color="blue", size=4, legend_label="X")
            p.scatter('index', 'y', source=source, color="red", size=4, legend_label="Y")
            p.scatter('index', 'z', source=source, color="green", size=4, legend_label="Z")
        else:
            p.scatter('index', variable_select.value, source=source, color="blue", size=4)
    elif chart_type.value == "Histogram":
        if variable_select.value == "All":
            for col, color in zip(['x', 'y', 'z'], ["blue", "red", "green"]):
                hist, edges = np.histogram(source.data[col], bins=20)
                p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                       fill_color=color, line_color="white", alpha=0.5, legend_label=col.upper())
        else:
            hist, edges = np.histogram(source.data[variable_select.value], bins=20)
            p.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:],
                   fill_color="navy", line_color="white", alpha=0.5)

def prev_callback():
    global current_start
    current_start = max(0, current_start - num_samples)
    update_data()

def next_callback():
    global current_start
    current_start = min(len(df) - num_samples, current_start + num_samples)
    update_data()

# Attach callbacks
chart_type.on_change('value', update_chart)
variable_select.on_change('value', update_chart)
samples_input.on_change('value', lambda attr, old, new: update_data())
prev_button.on_click(prev_callback)
next_button.on_click(next_callback)

# Periodic reload for live data (every 10 seconds)
curdoc().add_periodic_callback(update_data, 10000)

# Init
update_data()

# Layout
controls = column(chart_type, variable_select, samples_input, row(prev_button, next_button), status_text)
layout = column(title_div, row(controls, p), data_table)

curdoc().add_root(layout)
curdoc().title = "Gyroscope Data Dashboard"
