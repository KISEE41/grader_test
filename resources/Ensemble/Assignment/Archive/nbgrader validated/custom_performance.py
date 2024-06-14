import ipywidgets as widgets
from IPython.display import clear_output



custom_performance = widgets.Dropdown(
    value = None,
    options=['improved', 'degraded', 'remained same'],
    description='Ans:',
)

def on_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        if(change.new) == 'improved':
            clear_output()
            print("\nCorrect !! The best performance the plot between actual and predicted value should be a diagobal line. With each base model added, the the plot is getting alligned in diagonal line.")
        if(change.new) == 'degraded':
            clear_output()
            print("\nIncorrect!!")
        if(change.new) == 'remained same':
            clear_output()
            print("\nIncorrect!!")

custom_performance.observe(on_change)



display(custom_performance);
