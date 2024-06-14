import ipywidgets as widgets
from IPython.display import clear_output


is_overfitted = widgets.Dropdown(
    value = None,
    options=['optimally fitted', 'overfitted', 'underfitted'],
    description='Ans:',
)

def on_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        if(change.new) == 'overfitted':
            clear_output()
            print("\nIncorrect !! The performance of overfitted model is very good on training data but worse on test data.")
        if(change.new) == 'optimally fitted':
            clear_output()
            print("\nIncorrect!! You are close. Since both training and test f1-score are almost same, we can't say the model is optimally fitted. There might be space for further improvement on test data.")
        if(change.new) == 'underfitted':
            clear_output()
            print("\nCorrect!! The performance on both training and test data is poorer compared to bagging and random forest.")

is_overfitted.observe(on_change)



display(is_overfitted);

