import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, MultiSelect, RangeSlider, CheckboxGroup, Select, Button, Div
from bokeh.layouts import column, row
from bokeh.io import curdoc

# Baca data dari CSV
df = pd.read_csv('combined_data.csv')
data = df
data.dropna(inplace=True)

# Sumber data
source = ColumnDataSource(data)

# Fungsi untuk membuat plot
def create_plot(x_axis, y_axis, title):
    plot = figure(title=title, x_axis_label=x_axis, y_axis_label=y_axis)
    plot.scatter(x=x_axis, y=y_axis, source=source,
                 size=8, color='blue', alpha=0.6)
    plot.add_tools(HoverTool(tooltips=[
        ('Name', '@Name'),
        ('Nationality', '@Nationality'),
        ('Age', '@Age'),
        ('Overall Rating', '@{Overall Rating}'),
        ('Potential', '@Potential'),
        ('Value', '@Value'),
        ('Team', '@Team')
    ]))
    return plot

# Membuat plot
plot_overall = create_plot('Age', 'Overall Rating', 'Overall Rating vs Age')
plot_potential = create_plot('Age', 'Potential', 'Potential vs Age')
plot_value = create_plot('Overall Rating', 'Value', 'Value vs Overall Rating')

# Widget untuk filter
positions = sorted(list(data['Positions'].unique()))
position_multi_select = MultiSelect(
    title='Positions', value=[positions[0]], options=positions)

nationality = sorted(list(data['Nationality'].unique()))
nationality_multi_select = MultiSelect(title='Nationality', value=[
                                       nationality[0]], options=nationality)

age_min, age_max = data['Age'].min(), data['Age'].max()
range_slider = RangeSlider(start=age_min, end=age_max, value=(
    age_min, age_max), step=1, title='Age Range')

foot_options = ['Left', 'Right']
checkbox_foot = CheckboxGroup(labels=foot_options, active=[0, 1])

plot_options = {'Overall Rating vs Age': plot_overall,
                'Potential vs Age': plot_potential, 'Value vs Overall Rating': plot_value}
select_plot = Select(title='Plot Type', value='Overall Rating vs Age',
                     options=list(plot_options.keys()))

# Label untuk menampilkan jumlah data yang dipilih
data_count_div = Div(text=f"<b>Data Count:</b> {len(data)}")

# Fungsi untuk memperbarui data
def update_data(attr, old, new):
    selected_positions = position_multi_select.value
    selected_nationality = nationality_multi_select.value
    age_start, age_end = range_slider.value
    selected_foot = [foot_options[i] for i in checkbox_foot.active]

    new_data = data[
        (data['Positions'].apply(lambda x: any(pos in x for pos in selected_positions))) &
        (data['Nationality'].apply(lambda x: any(nat in x for nat in selected_nationality))) &
        (data['Age'] >= age_start) & (data['Age'] <= age_end) &
        (data['foot'].isin(selected_foot))
    ]
    source.data = ColumnDataSource.from_df(new_data)

    # Perbarui teks jumlah data
    data_count_div.text = f"<b>Data Count:</b> {len(new_data)}"

position_multi_select.on_change('value', update_data)
nationality_multi_select.on_change('value', update_data)
range_slider.on_change('value', update_data)
checkbox_foot.on_change('active', update_data)

# Fungsi untuk memperbarui plot
def update_plot(attr, old, new):
    selected_plot = select_plot.value
    layout.children[1] = plot_options[selected_plot]

select_plot.on_change('value', update_plot)

# Button untuk memilih semua posisi
select_all_positions_button = Button(
    label="Select All Positions", button_type="success")

def select_all_positions():
    position_multi_select.value = positions

select_all_positions_button.on_click(select_all_positions)

# Button untuk memilih semua nasionalitas
select_all_nationalities_button = Button(
    label="Select All Nationalities", button_type="success")

def select_all_nationalities():
    nationality_multi_select.value = nationality

select_all_nationalities_button.on_click(select_all_nationalities)

# Fungsi untuk membuat plot pemain terbaik dan terburuk
def create_top_bottom_plot(title, data):
    plot = figure(title=title, x_axis_label='Name',
                  y_axis_label='Overall Rating', x_range=data['Name'])
    plot.vbar(x='Name', top='Overall Rating',
              source=ColumnDataSource(data), width=0.9)
    plot.add_tools(HoverTool(tooltips=[
        ('Name', '@Name'),
        ('Overall Rating', '@{Overall Rating}')
    ]))
    plot.xaxis.major_label_orientation = "vertical"
    return plot

# Button dan fungsi untuk menampilkan 10 pemain terbaik
best_players_button = Button(
    label="Show Top 10 Players", button_type="success")

def show_best_players():
    top_10_players = data.nlargest(10, 'Overall Rating')
    best_players_plot = create_top_bottom_plot(
        'Top 10 Players', top_10_players)
    layout.children[1] = best_players_plot

best_players_button.on_click(show_best_players)

# Button dan fungsi untuk menampilkan 10 pemain terburuk
worst_players_button = Button(
    label="Show Bottom 10 Players", button_type="warning")

def show_worst_players():
    bottom_10_players = data.nsmallest(10, 'Overall Rating')
    worst_players_plot = create_top_bottom_plot(
        'Bottom 10 Players', bottom_10_players)
    layout.children[1] = worst_players_plot

worst_players_button.on_click(show_worst_players)

# Button dan fungsi untuk menampilkan 10 pemain terlincah
agile_players_button = Button(
    label="Show Top 10 Agile Players", button_type="success")

def show_agile_players():
    top_10_agile = data.nlargest(
        10, ['Sprint Speed', 'Acceleration', 'Movement'])
    agile_plot = create_top_bottom_plot('Top 10 Agile Players', top_10_agile)
    layout.children[1] = agile_plot

agile_players_button.on_click(show_agile_players)

# Button dan fungsi untuk menampilkan 10 pemain terskillful
skillful_players_button = Button(
    label="Show Top 10 Skillful Players", button_type="success")

def show_skillful_players():
    top_10_skillful = data.nlargest(10, ['Dribbling', 'Skill'])
    skillful_plot = create_top_bottom_plot(
        'Top 10 Skillful Players', top_10_skillful)
    layout.children[1] = skillful_plot

skillful_players_button.on_click(show_skillful_players)

# Button dan fungsi untuk menampilkan 10 pemain tersolid
solid_players_button = Button(
    label="Show Top 10 Solid Players", button_type="success")

def show_solid_players():
    top_10_solid = data.nlargest(
        10, ['Balance', 'Power', 'Stamina', 'Strength', 'Defending'])
    solid_plot = create_top_bottom_plot('Top 10 Solid Players', top_10_solid)
    layout.children[1] = solid_plot

solid_players_button.on_click(show_solid_players)

# Button dan fungsi untuk menampilkan 10 pemain dengan nilai tertinggi
most_value_players_button = Button(
    label="Show Top 10 Most Valuable Players", button_type="success")

def show_most_value_players():
    top_10_value = data.nlargest(10, 'Value')
    value_plot = create_top_bottom_plot('Top 10 Most Valuable Players', top_10_value)
    layout.children[1] = value_plot

most_value_players_button.on_click(show_most_value_players)

# Button dan fungsi untuk menampilkan 10 pemain dengan potensi tertinggi
potential_players_button = Button(
    label="Show Top 10 Potential Players", button_type="success")

def show_potential_players():
    top_10_potential = data.nlargest(10, 'Potential')
    potential_plot = create_top_bottom_plot('Top 10 Potential Players', top_10_potential)
    layout.children[1] = potential_plot

potential_players_button.on_click(show_potential_players)

# Div untuk informasi kelompok
group_info = Div(text="""
    <b>Kelompok 7</b><br>
    Daffa Afia Rizfazka    - 1301213215<br>
    Hadid Pilar Gautama    - 1301213297<br>
    Raihan abdurrahman     - 1301210340<br>
    Raden Ananta Mahardika - 1301213326<br>
    Virdi Rizky Elnanda    - 1301210490<br>
""")

# Layout
widgets = column(group_info, position_multi_select, select_all_positions_button, nationality_multi_select,
                 select_all_nationalities_button, range_slider, checkbox_foot, select_plot, data_count_div,
                 best_players_button, worst_players_button, agile_players_button, skillful_players_button, solid_players_button,
                 most_value_players_button,  potential_players_button)
layout = row(widgets, plot_overall)

curdoc().add_root(layout)
