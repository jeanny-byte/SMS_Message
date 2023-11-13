import csv
import requests

def send_sms_with_unique_values(file_path, column_index):
    printed_values = set()
    logs = []

    def replace_first_number(data):
        # Check if the data is not empty and the first character is a digit
        if data and str(data)[0].isdigit():
            # Get the first character of the phone number
            first_digit = str(data)[0]

            # Replace the first digit with a valid prefix
            if first_digit == '0':
                replaced_data = '233' + str(data)[1:]
            else:
                replaced_data = '233' + str(data)

            return replaced_data

        return data

    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        header = next(reader)  # Skip the header row

        for row in reader:
            first_column_value = row[column_index]
            firstname = row[1]  # Update the index to access the 'Fname' column
            message = f"{firstname}, In His Presence 2024 is approaching. Get ready to groove, sing, and worship. Spread the word and invite your friends for a memorable time!"


            ModNum_data = replace_first_number(first_column_value)
            if ModNum_data is None:
                continue

            # Replace placeholders in the message with row values
            formatted_message = message.format(*row)

            # Send the SMS using the MNOTIFY API
            endPoint = 'https://apps.mnotify.net/smsapi'
            apiKey = 'WdjdYPw4WAXb96jMcf'
            url = endPoint + '?key=' + apiKey + '&to=' + ModNum_data + '&msg=' + formatted_message + '&sender_id=IHP24'  # Fix: Use formatted_message instead of message
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Error in API request. Status Code: {response.status_code}")

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
file_path = "IHP'24.csv"
column_index = 0

send_sms_with_unique_values(file_path, column_index)
