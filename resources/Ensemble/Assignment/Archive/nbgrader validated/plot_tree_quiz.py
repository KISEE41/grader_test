import ipywidgets as widgets

plot_tree_quiz = widgets.Dropdown(
    value = None,
    options=['deposit_type', 'adr', 'net_booking_cancelled', 'required_car_parking_spaces', 'total_of_special_requests'],
    description='Ans:',
)
display(plot_tree_quiz);
