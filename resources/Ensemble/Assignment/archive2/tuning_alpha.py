import ipywidgets as widgets

tuning_alpha_quiz = widgets.Dropdown(
    value = None,
    options=['0', '0.4', '1', '5', '10'],
    description='Ans:',
)
display(tuning_alpha_quiz);  
