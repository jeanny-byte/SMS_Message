import PySimpleGUI as sg

# Define the layout for the splash screen
splash_layout = [[sg.Text('Welcome to the Application!', font=('Arial', 16))]]

# Create the splash screen window
splash_window = sg.Window('Splash Screen', splash_layout, element_justification='center', finalize=True)

# Show the splash screen for a duration of 2 seconds
sg.popup_auto_close(splash_window, auto_close_duration=200)

# Define the layout for the main window with tabs
tab1_layout = [[sg.Text('Content for Tab 1')]]
tab2_layout = [[sg.Text('Content for Tab 2')]]
tab3_layout = [[sg.Text('Content for Tab 3')]]

layout = [[sg.TabGroup([[sg.Tab('Tab 1', tab1_layout), sg.Tab('Tab 2', tab2_layout), sg.Tab('Tab 3', tab3_layout)]])]]

# Create the main window
window = sg.Window('Tabbed Interface', layout)

# Event loop to handle window events
while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break

# Close the windows
window.close()
splash_window.close()
