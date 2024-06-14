import ipywidgets as widgets

performance_compare1 = widgets.Dropdown(
    value = None,
    options=['better than', 'worse than', 'same as'],
    description='Ans:',
)
display(performance_compare1);

