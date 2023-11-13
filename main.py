import openpyxl
import requests

def send_sms_with_unique_values(file_path, sheet_name, column_index, message):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]

    printed_values = set()
    logs = []

    for row in sheet.iter_rows(values_only=True):
        first_column_value = row[column_index]
        Fname = row[1]

        if first_column_value not in printed_values:
            # Replace placeholders in the message with row values
            formatted_message = message.format(*row)

            def replace_first_number(data):
                # Check if the first character is a digit
                if len(str(data)) > 0:
                    # Convert the data to a list
                    data_list = list(data)

                    # Check if the first character is a digit
                    if data_list[0].isdigit():
                        # Replace the first character with '2' followed by '33'
                        data_list[0] = '2'
                        data_list.insert(1, '3')
                        data_list.insert(2, '3')

                        # Convert the list back to a string
                        replaced_data = ''.join(data_list)
                        # Returned Data
                        return replaced_data

                return data

            original_data = first_column_value
            ModNum_data = replace_first_number(original_data)
            if ModNum_data == None:
                continue

            # Send the SMS using the MNOTIFY API
            endPoint = 'https://apps.mnotify.net/smsapi'
            apiKey = 'Wdj7EExbzUdYPw4WAXb96jMcf'
            url = endPoint + '?key=' + apiKey + '&to=' + ModNum_data + '&msg=' + formatted_message + '&sender_id=xxxxx'
            response = requests.get(url)

            # Print the request status, number sent to, and message
            log = f"Status: {response.status_code}, Number: {ModNum_data}, Message: {formatted_message}"
            print(log)
            logs.append(log)

            # Add the first column value to the set of printed values
            printed_values.add(first_column_value)

    # Save the logs as a text file
    with open("sms_logs.txt", "w") as file:
        for log in logs:
            file.write(log + "\n")

    # Prompt the user to save the log text file
    user_input = input("Do you want to save the log text file? (Y/N): ")
    if user_input.lower() == "y":
        print("Log text file saved.")
    else:
        print("Log text file not saved.")

# Example usage
file_path = "ME.xlsx"
sheet_name = "Sheet1"
column_index = 0
message = "{Fname}!, In His Presence 2024 is approaching. Get ready to groove, sing, and fellowship. Spread the word and invite your friends for a memorable time!"

send_sms_with_unique_values(file_path, sheet_name, column_index, message)
