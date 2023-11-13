import csv
import requests
import PySimpleGUI as sg

def replace_first_number(data):
    if data and str(data)[0].isdigit():
        first_digit = str(data)[0]
        if first_digit == '0':
            replaced_data = '233' + str(data)[1:]
        else:
            replaced_data = '233' + str(data)
        return replaced_data
    return data

def send_sms_with_unique_values(file_path, column_index, api_key, custom_message):
    printed_values = set()
    logs = []

    layout = [
        [sg.Text('Enter API Key:'), sg.Input(key='-API_KEY-', default_text=api_key)],
        [sg.FileBrowse('Import CSV File', key='-CSV_FILE-', file_types=(("CSV Files", "*.csv"),))],
        [sg.Text('Enter Custom Message:')],
        [sg.Multiline(key='-CUSTOM_MESSAGE-', default_text=custom_message, size=(60, 5))],
        [sg.Button('Send SMS')],
        [sg.Text('', size=(60, 1), key='-UPDATE_TEXT-', background_color='white')],
        [sg.Output(size=(60, 10))]
    ]

    window = sg.Window('SMS Sender', layout)

    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

        if event == 'Send SMS':
            api_key = values['-API_KEY-']
            if not api_key:
                sg.popup_error('API Key cannot be empty!')
                continue

            file_path = values['-CSV_FILE-']
            if not file_path:
                sg.popup_error('Please select a CSV file!')
                continue

            custom_message = values['-CUSTOM_MESSAGE-']
            if not custom_message:
                sg.popup_error('Custom Message cannot be empty!')
                continue

            for row in read_csv(file_path, column_index):
                first_column_value = row[column_index]
                firstname = row[1]

                mod_num_data = replace_first_number(first_column_value)
                if mod_num_data is None:
                    continue

                formatted_message = custom_message.format(*row)

                end_point = 'https://apps.mnotify.net/smsapi'
                url = end_point + '?key=' + api_key + '&to=' + mod_num_data + '&msg=' + formatted_message + '&sender_id=IHP24'
                response = requests.get(url)

                log = f"Status: {response.status_code}, Number: {mod_num_data}, Message: {formatted_message}"
                logs.append(log)
                printed_values.add(first_column_value)

                window['-UPDATE_TEXT-'].update(f'Updating: {mod_num_data}')

            with open("sms_logs.txt", "w") as file:
                for log in logs:
                    file.write(log + "\n")

            print("SMS sent and logs saved.")
            window['-UPDATE_TEXT-'].update('Update complete.')
    
    window.close()

def read_csv(file_path, column_index):
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row
        for row in reader:
            yield row

# Example usage
column_index = 0
api_key = 'Your_Predefined_API_Key'
custom_message = 'Hello {1}, In His Presence 2024 is approaching. Get ready to groove, sing, and worship. Spread the word and invite your friends for a memorable time.'

send_sms_with_unique_values(None, column_index, api_key, custom_message)
