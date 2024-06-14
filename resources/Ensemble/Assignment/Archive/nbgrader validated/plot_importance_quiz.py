import ipywidgets as widgets
from IPython.display import clear_output


plot_importance_quiz = widgets.Dropdown(
    value = None,
    options=['lead_time', 'country', 'adr', 'net_booking_cancelled', 'required_car_parking_spaces', 'deposit_type'],
    description='Ans:',
)


def on_change(change):
    if change['type'] == 'change' and change['name'] == 'value':
        if(change.new) == 'deposit_type':
            clear_output()
            print("\nCorrect !! With importance_type set to gain, we will obtain deposit_type as most important feature. ")
        if(change.new) == 'lead_time':
            clear_output()
            print("\nIncorrect !! You are close. lead_time appears most frequently in the splitting.")
        if(change.new) == 'country':
            clear_output()
            print("\nIncorrect!! Please plot the feature importance of model xgb to identify most important feature")
        if(change.new) == 'adr':
            clear_output()
            print("\nIncorrect!! Please plot the feature importance of model xgb to identify most important feature")
        if(change.new) == 'net_booking_cancelled':
            clear_output()
            print("\nIncorrect!! Please plot the feature importance of model xgb to identify most important feature")
        if(change.new) == 'required_car_parking_spaces':
            clear_output()
            print("\nIncorrect!! Please plot the feature importance of model xgb to identify most important feature")
         

plot_importance_quiz.observe(on_change)


display(plot_importance_quiz);

