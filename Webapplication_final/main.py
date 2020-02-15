from bokeh.server.server import Server
from bokeh.plotting import figure, output_file, ColumnDataSource
from bokeh.models import Segment, HoverTool, RangeSlider, Select, TextInput, Button, TableColumn, DataTable, Panel, Tabs, Legend, LegendItem, TextInput, Dropdown, FileInput, TextAreaInput, Whisker
from bokeh.models.widgets import Div
from bokeh.models.glyphs import Segment
from bokeh.layouts import row, column, layout, widgetbox
from bokeh.io import curdoc, output_file, save
from bokeh.embed import file_html
from bokeh.transform import linear_cmap, cumsum
from bokeh.palettes import Category20c
from bokeh.command.bootstrap import main

import pandas as pd
import os.path
import numpy as np

from math import pi
# ------------------------------------------------------------------------------

# Read featureFileAsap1.tsv file as a DataFrame object
df = pd.read_csv('featureFileAsap1.tsv', sep='\t')

# Read in tsv file whiich holds the essays
df_essay = pd.read_csv('asap_essays.txt', sep='\t', encoding='cp1252')
# ------------------------------------------------------------------------------

# Create div with html code within. Will be provided to create headline and description for the application
desc = Div(text="""
    <div>
        <h3>ESANVis: Comparative Visualization of Essays</h3>
        <p>ESANVis is a browser based application to compare different essays with each other. The aim is to visually represent the essays evaluated by scoring algorithms in order to enable a new level of analysis.</p>
    </div>
""", sizing_mode='stretch_width')
# ------------------------------------------------------------------------------

# Create ColumnDataSource from dataframe
source = ColumnDataSource(df)
# ------------------------------------------------------------------------------

# Empty arrays which will be used to hold the statistical values and provide them to a data table
means = []
mins = []
maxs = []
values = []
stds = []

# This for-loop iterates through the columns of the dataframe, calculates the statistical values
# mean, minimum, maximum and standard deviation and forwards them to the corresponding list above.
# Since there is no need to calculate statistical value of the ID, this column will be skipped.
for i in df:
    if i == 'ID':
        continue
    else:
        mean = df[i].mean().round(decimals=2)
        means.append(mean)

        min = df[i].min()
        mins.append(min)

        max = df[i].max()
        maxs.append(max)

        values.append(i)

        std = df[i].std().round(decimals=2)
        stds.append(std)

# Create a dictionary from which we will build the column data source.
stats_data = dict(
    means = means,
    mins = mins,
    maxs = maxs,
    value = values,
    std = stds
)

# Create the column data source which will serve as the source in the table later
data = ColumnDataSource(stats_data)
# ------------------------------------------------------------------------------

# List of outcomes
outcomes = [2,3,4,5,6,7,8,9,10,11,12]

# This list is used as abbrevations for the features for better readability
column_list = ['Amplifier words', 'Be as main verb', 'Causative', 'Concessive', 'Conditional', 'Demonstrative words', 'Downtoner', 'Emphatic', 'Hedge words', 'Infinitive', 'Other adverbial', 'Agentless passive', 'By passive', 'Pronouns', 'That adjective', 'That verb', 'Clause words', 'Outcome']

# Safe column headlines in dictionary
head_columns = {
    'id': 'ID',
    'Amplifier words': 'nrOfMatches_AmplifierWordu46Amplifier',
    'Be as main Verb': 'nrOfMatches_BeWordu46BeAsMainVerb',
    'Causative adverbial subordinator': 'nrOfMatches_CausativeAdverbialSubordinatorWordu46CausativeAdverbialSubordinator',
    'Concessive adverbial subordinator': 'nrOfMatches_ConcessiveAdverbialSubordinatorWordu46ConcessiveAdverbialSubordinator',
    'Conditional adverbial subordinator': 'nrOfMatches_ConditionalAdverbialSubordinatorWordu46ConditionalAdverbialSubordinator',
    'Demonstrative word': 'nrOfMatches_DemonstrativeWordu46Demonstrative',
    'Downtoner': 'nrOfMatches_DowntonerWordu46Downtoner',
    'Emphatic words': 'nrOfMatches_EmphaticWordu46Emphatic',
    'Hedge words': 'nrOfMatches_HedgeWordu46Hedge',
    'Infinitive words': 'nrOfMatches_InfinitiveWordu46Infinitive',
    'Other adverbial subordinator': 'nrOfMatches_OtherAdverbialSubordinatorWordu46OtherAdverbialSubordinator',
    'Agentless passive': 'nrOfMatches_PassivesWordu46AgentlessPassive',
    'By passive': 'nrOfMatches_PassivesWordu46ByPassive',
    'Pronouns': 'nrOfMatches_PronounWordu46ItPronoun',
    'That adjective complement': 'nrOfMatches_ThatComplementWordu46ThatAdjectiveComplement',
    'That verb complement': 'nrOfMatches_ThatComplementWordu46ThatVerbComplement',
    'Clause words': 'nrOfMatches_WHClauseWordu46WH_Clause',
    'Outcome': 'outcome'
}
# ------------------------------------------------------------------------------

# Function for creating the main plot
def create_plot():

    # Add figure
    p = figure(
        title='',
        plot_width=1000,
        plot_height=700,
        x_axis_label='ID',
        toolbar_location='above',
        tools='pan, box_select, save, undo, redo, xwheel_zoom, reset'
    )

    # Save value for y-axis from select input widget within the "top" variable
    # in the glyph. It will automatically update on changing the select widget within the application.
    y_axis = head_columns[sel_yaxis.value]
    x_axis = head_columns[sel_xaxis.value]

    # Set the label on y-axis so that the glyph displayed and y-axis label match
    p.yaxis.axis_label = sel_yaxis.value
    p.xaxis.axis_label = sel_xaxis.value

    # Holds the x-axis ID values for the glyph
    id = head_columns['id']

    # compare range slider values with y-axis values
    # Manipulate the ColumnDataSource so that it only contains the values which meets
    # the conditions of the range slider
    current = df[(df[y_axis] >= num_tokens.value[0]) & (df[y_axis] <= num_tokens.value[1])].dropna()
    source.data = {
        'ID': current.ID,
        'nrOfMatches_AmplifierWordu46Amplifier': current.nrOfMatches_AmplifierWordu46Amplifier,
        'nrOfMatches_BeWordu46BeAsMainVerb': current.nrOfMatches_BeWordu46BeAsMainVerb,
        'nrOfMatches_CausativeAdverbialSubordinatorWordu46CausativeAdverbialSubordinator': current.nrOfMatches_CausativeAdverbialSubordinatorWordu46CausativeAdverbialSubordinator,
        'nrOfMatches_ConcessiveAdverbialSubordinatorWordu46ConcessiveAdverbialSubordinator': current.nrOfMatches_ConcessiveAdverbialSubordinatorWordu46ConcessiveAdverbialSubordinator,
        'nrOfMatches_ConditionalAdverbialSubordinatorWordu46ConditionalAdverbialSubordinator': current.nrOfMatches_ConditionalAdverbialSubordinatorWordu46ConditionalAdverbialSubordinator,
        'nrOfMatches_DemonstrativeWordu46Demonstrative': current.nrOfMatches_DemonstrativeWordu46Demonstrative,
        'nrOfMatches_DowntonerWordu46Downtoner': current.nrOfMatches_DowntonerWordu46Downtoner,
        'nrOfMatches_EmphaticWordu46Emphatic': current.nrOfMatches_EmphaticWordu46Emphatic,
        'nrOfMatches_HedgeWordu46Hedge': current.nrOfMatches_HedgeWordu46Hedge,
        'nrOfMatches_InfinitiveWordu46Infinitive': current.nrOfMatches_InfinitiveWordu46Infinitive,
        'nrOfMatches_OtherAdverbialSubordinatorWordu46OtherAdverbialSubordinator': current.nrOfMatches_OtherAdverbialSubordinatorWordu46OtherAdverbialSubordinator,
        'nrOfMatches_PassivesWordu46AgentlessPassive': current.nrOfMatches_PassivesWordu46AgentlessPassive,
        'nrOfMatches_PassivesWordu46ByPassive': current.nrOfMatches_PassivesWordu46ByPassive,
        'nrOfMatches_PronounWordu46ItPronoun': current.nrOfMatches_PronounWordu46ItPronoun,
        'nrOfMatches_ThatComplementWordu46ThatAdjectiveComplement': current.nrOfMatches_ThatComplementWordu46ThatAdjectiveComplement,
        'nrOfMatches_ThatComplementWordu46ThatVerbComplement': current.nrOfMatches_ThatComplementWordu46ThatVerbComplement,
        'nrOfMatches_WHClauseWordu46WH_Clause': current.nrOfMatches_WHClauseWordu46WH_Clause,
        'outcome': current.outcome
    }

    # Define colors and provide it to linear_cmap for coding different plot items respectively to
    # their outcome
    colours = ['red', 'orange', 'green']
    mapper = linear_cmap(field_name=head_columns['Outcome'], palette=colours, low=0.0, high=12.0)

    # If-statements which takes the value of the y-axis selection widget and uses
    #  it to provide the right plot type to the figure
    if sel_plot.value == 'vbar':
        p.vbar(
            x=x_axis,
            top=y_axis,
            source=source,
            width=0.8,
            color=mapper,
            hover_color='violet',
            line_alpha=0.3,
        )
    elif sel_plot.value == 'scatter':
        p.scatter(
            x=x_axis,
            y=y_axis,
            color=mapper,
            hover_color='violet',
            source=source,
        )
    elif sel_plot.value == 'line':
        out = []
        sub = source.to_df()
        for i in sub[x_axis]:
            if i in out:
                continue
            else:
                out.append(i)
        x_line = df.groupby(by=x_axis).mean()
        p.line(
            x=sorted(out),
            y=x_line[y_axis],
            color='orange'
        )
    elif sel_plot.value == 'varea':
        out = []
        sub = source.to_df()
        for i in sub[x_axis]:
            if i in out:
                continue
            else:
                out.append(i)
        area1 = df.copy().groupby(by='outcome').min()
        area2 = df.copy().groupby(by='outcome').max()
        p.varea(
            x=sorted(out),
            y1=area1[y_axis],
            y2=area2[y_axis],
            fill_alpha=0.3,
            color='orange'
        )
        p.line(
            x=sorted(out),
            y=area2[y_axis],
            color='orange'
        )

    # Create tooltips with HTML and add them to the plot
    if sel_plot.value == 'scatter' or sel_plot.value == 'vbar':
        hover = HoverTool()
        hover.tooltips = """
            <div>
                <h3><strong>ID: </strong>@ID</h3>
                <div><strong>Outcome: </strong>@outcome</div>
            </div>
        """
        p.add_tools(hover)

    # Remove vertical grid lines
    p.xgrid.grid_line_color = None

    # Remove logo
    p.toolbar.logo = None

    # Create tabs. One for the plot and another for the table view
    t1 = Panel(child=p, title='Plot')
    t2 = Panel(child=data_table, title='Table')
    tabs = Tabs(tabs=[t1, t2])

    return tabs
# ------------------------------------------------------------------------------

# Create pie chart
def create_pie():
    # Create dictionary from data frame. Use 'ID' column as key and set the features
    # of each row in an array as value
    x = df.set_index('ID').to_dict('index')

    # Create a copy of the head_columns dictionary. The keys provide more readability
    # than the feature names of the data frame. The keys will be used to create a legend
    # for the pie chart.
    dict_features = head_columns.copy()

    # Delete the keys 'id' and 'Outcome' to remove them from the legend. They
    # do not provide a feature and thus are not relevant for the pie chart.
    del dict_features['id']
    del dict_features['Outcome']

    # Safe the respective row from the dictionary 'x'
    y = x[int(inp_id.value)]

    # Safe the number of tokens for each feature in the equivalent of the 'dict_feature'
    # dictionary
    dict_features['Amplifier words'] = y['nrOfMatches_AmplifierWordu46Amplifier']
    dict_features['Be as main Verb'] = y['nrOfMatches_BeWordu46BeAsMainVerb']
    dict_features['Causative adverbial subordinator'] = y['nrOfMatches_CausativeAdverbialSubordinatorWordu46CausativeAdverbialSubordinator']
    dict_features['Concessive adverbial subordinator'] = y['nrOfMatches_ConcessiveAdverbialSubordinatorWordu46ConcessiveAdverbialSubordinator']
    dict_features['Conditional adverbial subordinator'] = y['nrOfMatches_ConditionalAdverbialSubordinatorWordu46ConditionalAdverbialSubordinator']
    dict_features['Demonstrative word'] = y['nrOfMatches_DemonstrativeWordu46Demonstrative']
    dict_features['Downtoner'] = y['nrOfMatches_DowntonerWordu46Downtoner']
    dict_features['Emphatic words'] = y['nrOfMatches_EmphaticWordu46Emphatic']
    dict_features['Hedge words'] = y['nrOfMatches_HedgeWordu46Hedge']
    dict_features['Infinitive words'] = y['nrOfMatches_InfinitiveWordu46Infinitive']
    dict_features['Other adverbial subordinator'] = y['nrOfMatches_OtherAdverbialSubordinatorWordu46OtherAdverbialSubordinator']
    dict_features['Agentless passive'] = y['nrOfMatches_PassivesWordu46AgentlessPassive']
    dict_features['By passive'] = y['nrOfMatches_PassivesWordu46ByPassive']
    dict_features['Pronouns'] = y['nrOfMatches_PronounWordu46ItPronoun']
    dict_features['That adjective complement'] = y['nrOfMatches_ThatComplementWordu46ThatAdjectiveComplement']
    dict_features['That verb complement'] = y['nrOfMatches_ThatComplementWordu46ThatVerbComplement']
    dict_features['Clause words'] = y['nrOfMatches_WHClauseWordu46WH_Clause']

    # Prepare the 'dict_feature' dictionary for the pie chart and safe in a
    # variable called 'data'. The 'angle' and 'color' keys will be added to the dictionary
    # to ensure that the wedge glyph will result in a circle and each feature got
    # a specific colour.
    data = pd.Series(dict_features).reset_index(name='value').rename(columns={'index':'v'})
    data['angle'] = data['value']/data['value'].sum() * 2*pi
    data['color'] = Category20c[len(dict_features)]

    #Add plot
    p = figure(
        plot_height=600,
        plot_width=800,
        title='Number of each feature',
        toolbar_location=None,
        tooltips='@v: @value',
        x_range=(-0.5, 1.0)
    )

    # Add glyph
    p.wedge(
        x=0,
        y=1,
        radius=0.4,
        start_angle=cumsum('angle', include_zero=True),
        end_angle=cumsum('angle'),
        line_color='white',
        fill_color='color',
        legend_field='v',
        source=data
    )

    # Remove axes and background grid from the plot
    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None

    # Return the plot
    return p
# ------------------------------------------------------------------------------

# Function to instantiate a new data frame @todo
# It is not working right now. However, it has not yet been found out why.
# It does not throw any error when performing therefore it seems that the
# function itself does not contain the error.
# It could be that the error is caused by two positions in the code
# playing off against each other.
def change_file(attr, old, new):
    # Read in new data
    dft = pd.read_csv(str(add_row.filename), sep='\t')

    # Convert the data into a DataFrame object
    # newrows = dft.DataFrame()

    # Use stream method to update the source with the new data
    source.stream(dft)

    # Call the main plot function to display it with the new data
    layout.children[1] = create_plot()
# ------------------------------------------------------------------------------

# Create boxplot chart
def create_boxplot():
    # Create the figure
    p = figure(
        title='',
        y_range=column_list,
        y_axis_location='right',
        plot_width=550,
        plot_height=730,
        toolbar_location='above',
        tools='pan, wheel_zoom'
    )

    # Create a deepcopy of the data frame to make sure that we do not
    # accidentally edit the original data frame. Delete the 'ID' columns afterwards.
    # It will not be used in the boxplot.
    df_boxplot = df.copy()
    del df_boxplot['ID']

    # Sort the new created dataframe
    sorted(df_boxplot)

    # Split the data frame at the respective quantiles
    q1 = df_boxplot.quantile(q=0.25)
    q2 = df_boxplot.quantile(q=0.5)
    q3 = df_boxplot.quantile(q=0.75)
    iqr = q3 - q1
    upper = q3 + 1.5*iqr
    lower = q1 - 1.5*iqr

    # Add glyphs. Since there is no specific boxplot glyph provided by the Bokeh module,
    # it is built from scratch by a couple of individual glyphs.
    p.segment(
        x0=mins,
        y0=column_list,
        x1=maxs,
        y1=column_list,
        line_color='black'
    )

    p.hbar(
        y=column_list,
        left=q1,
        right=q2,
        height=0.6,
        line_color='black',
        color='#E08A79'
    )
    p.hbar(
        y=column_list,
        left=q2,
        right=q3,
        height=0.6,
        line_color='black',
        color='#3B8686'
    )

    p.rect(
        x=mins,
        y=column_list,
        width=0.01,
        height=0.4,
        line_color='black',
        color='black'
    )
    p.rect(
        x=maxs,
        y=column_list,
        width=0.01,
        height=0.4,
        line_color='black',
        color='black'
    )

    # Remove unnessary logos for more readability
    p.toolbar.logo = None

    # Return plot
    return p
# ------------------------------------------------------------------------------

# This function will be used as a callback function and
# update the plot upon changes within the input controls
def update(attr, old, new):
    layout.children[1] = create_plot()
# ------------------------------------------------------------------------------

# Callback function for TextInput widget.
# Updating the TextAreaInput widget with essay of the given ID and
# calling the pie chart function to update it.
def update_pie(attr, old, new):
    essay_insert = df_essay.set_index('essay_id').to_dict('index')
    text_key = essay_insert[int(inp_id.value)]

    score = 0
    for i in text_key['essay'].split():
        score += 1

    sh_ess.value = text_key['essay']
    sh_ess.title = 'Essay %s: %d words' % (inp_id.value, score)
    indv.children[1] = create_pie()
# ------------------------------------------------------------------------------

# Add input controls
num_tokens = RangeSlider(
    title='Number of Tokens',
    start=0,
    end=40,
    value=(0, 40),
    step=1,
    format='0,0'
)

sel_yaxis = Select(
    title='Select Y Axis',
    options=sorted(head_columns.keys()),
    value='Amplifier words'
)

sel_xaxis = Select(
    title='Select X Axis',
    options=sorted(head_columns.keys()),
    value='Outcome'
)

options=['scatter', 'vbar', 'varea', 'line']

sel_plot = Dropdown(
    label='Select plot type',
    button_type='success',
    menu=options,
    value='line'
)

add_row = FileInput(
)

inp_id = TextInput(
    placeholder='Insert ID',
    value='1',
)

sh_ess = TextAreaInput(
    title='Essay %s: 338 words' % inp_id.value,
    rows=30,
    cols=50,
    value="""Dear local newspaper, I think effects computers have on people are great learning skills/affects because they give us time to chat with friends/new people, helps us learn about the globe(astronomy) and keeps us out of troble! Thing about! Dont you think so? How would you feel if your teenager is always on the phone with friends! Do you ever time to chat with your friends or buisness partner about things. Well now - there's a new way to chat the computer, theirs plenty of sites on the internet to do so: @ORGANIZATION1, @ORGANIZATION2, @CAPS1, facebook, myspace ect. Just think now while your setting up meeting with your boss on the computer, your teenager is having fun on the phone not rushing to get off cause you want to use it. How did you learn about other countrys/states outside of yours? Well I have by computer/internet, it's a new way to learn about what going on in our time! You might think your child spends a lot of time on the computer, but ask them so question about the economy, sea floor spreading or even about the @DATE1's you'll be surprise at how much he/she knows. Believe it or not the computer is much interesting then in class all day reading out of books. If your child is home on your computer or at a local library, it's better than being out with friends being fresh, or being perpressured to doing something they know isnt right. You might not know where your child is, @CAPS2 forbidde in a hospital bed because of a drive-by. Rather than your child on the computer learning, chatting or just playing games, safe and sound in your home or community place. Now I hope you have reached a point to understand and agree with me, because computers can have great effects on you or child because it gives us time to chat with friends/new people, helps us learn about the globe and believe or not keeps us out of troble. Thank you for listening."""
)
# ------------------------------------------------------------------------------

# Define functionality of controls
num_tokens.on_change('value', update)
sel_yaxis.on_change('value', update)
sel_xaxis.on_change('value', update)
sel_plot.on_change('value', update)
add_row.on_change('value', change_file)
inp_id.on_change('value', update_pie)
# ------------------------------------------------------------------------------

# Define variable which holds the different columns of our dataframe
columns = [
    TableColumn(field='ID', title='ID'),
    TableColumn(field='nrOfMatches_AmplifierWordu46Amplifier', title='Amplifier word'),
    TableColumn(field='nrOfMatches_BeWordu46BeAsMainVerb', title='Be as main verb'),
    TableColumn(field='nrOfMatches_CausativeAdverbialSubordinatorWordu46CausativeAdverbialSubordinator', title='Causative adverbial subordinator'),
    TableColumn(field='nrOfMatches_ConcessiveAdverbialSubordinatorWordu46ConcessiveAdverbialSubordinator', title='Concessive adverbial subordinator'),
    TableColumn(field='nrOfMatches_ConditionalAdverbialSubordinatorWordu46ConditionalAdverbialSubordinator', title='Conditional adverbial subordinator'),
    TableColumn(field='nrOfMatches_DemonstrativeWordu46Demonstrative', title='Demonstrative words'),
    TableColumn(field='nrOfMatches_DowntonerWordu46Downtoner', title='Downtoner'),
    TableColumn(field='nrOfMatches_EmphaticWordu46Emphatic', title='Emphatic words'),
    TableColumn(field='nrOfMatches_HedgeWordu46Hedge', title='Hedge words'),
    TableColumn(field='nrOfMatches_InfinitiveWordu46Infinitive', title='Infinitive'),
    TableColumn(field='nrOfMatches_OtherAdverbialSubordinatorWordu46OtherAdverbialSubordinator', title='Other adverbial subordinator'),
    TableColumn(field='nrOfMatches_PassivesWordu46AgentlessPassive', title='Agentless passive'),
    TableColumn(field='nrOfMatches_PassivesWordu46ByPassive', title='By passive'),
    TableColumn(field='nrOfMatches_PronounWordu46ItPronoun', title='Pronoun'),
    TableColumn(field='nrOfMatches_ThatComplementWordu46ThatAdjectiveComplement', title='That adjective'),
    TableColumn(field='nrOfMatches_ThatComplementWordu46ThatVerbComplement', title='That verb'),
    TableColumn(field='nrOfMatches_ThatComplementWordu46ThatVerbComplement', title='That verb'),
    TableColumn(field='nrOfMatches_WHClauseWordu46WH_Clause',title='Clause')
]

# Create table with the columns above
data_table = DataTable(source=source, columns=columns, width=1000, height=700)
# ------------------------------------------------------------------------------

# Define columns for the statistical values table
stats_columns = [
    TableColumn(field='value', title='value'),
    TableColumn(field='mins', title='min'),
    TableColumn(field='maxs', title='max'),
    TableColumn(field='means', title='mean'),
    TableColumn(field='std', title='standard deviation')
]

# Create data table for the statistical values
stats_table = DataTable(source=data, columns=stats_columns, width=300, height=480)
# ------------------------------------------------------------------------------

# Create widgetbox which holds the input controls and data table
widget = widgetbox(children=[num_tokens, sel_yaxis, sel_xaxis, sel_plot, add_row, stats_table])
# ------------------------------------------------------------------------------

# Create widgetbox for individual analysis
widget1 = widgetbox(children=[inp_id])
# ------------------------------------------------------------------------------

# Safe plot to Initiate it within layout variable
plot = create_plot()
pie = create_pie()
box = create_boxplot()
# ------------------------------------------------------------------------------

# Define layout of the application
l = row(desc)
layout = row(widget, plot, box)
indv = row(widget1, pie, sh_ess)
# ------------------------------------------------------------------------------

# Add layout to output document
# Set title in navigation bar
curdoc().add_root(l)
curdoc().add_root(layout)
curdoc().add_root(indv)
curdoc().title = 'Comparative Visualizations of Essays'

if __name__ == '__main__':
    main(['bokeh', 'serve', '--show', 'main.py'])
