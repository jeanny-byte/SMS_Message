import openpyxl
import requests


def send_sms_with_unique_values(file_path, sheet_name, column_index, message):
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook[sheet_name]

    printed_values = set()

    for row in sheet.iter_rows(values_only=True):
        first_column_value = row[column_index]
        Fname = row[1]



        if first_column_value not in printed_values:
            # Replace placeholders in the message with row values
            formatted_message = message.format(*row)

            def replace_first_number(data):
                if len(data) > 0:
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

                        return replaced_data
                return data

            original_data = first_column_value
            ModNum_data = replace_first_number(original_data)

            # Send the SMS using the MNOTIFY API

            endPoint = 'https://api.mnotify.com/api/sms/quick'
            apiKey = 'LyoYyQPI2cmCQAPFuK1xN7UMd'
            data = {
                'recipient[]': ModNum_data,
                'sender': 'GEC Shalom',
                'message': "Hello " + Fname + " "+ " Calvary greetings in the name of our Lord Jesus Christ. From the leadership of Global Evangelical Church Michel Camp, a Happy New Month to you. God has been so good ushering us into this second half of the year. We humbly invite you as our special guest to our special thanksgiving celebration to experience God's love and glory on 9th July, 2023 at 4:00pm at church auditorium. It is all about thanksgiving. We pray God keep and watch over you. Shalom!!!",
                'is_schedule': False,
                'schedule_date': ''
            }
            url = endPoint + '?key=' + apiKey
            response = requests.post(url, data)
            data = response.json()

            # print(data)
            print(ModNum_data+ ' sent ' + data["status"] )

            # if response.status_code == 200:
            #     print("SMS sent successfully.")
            # else:
            #     print("SMS sending failed.")

            # Add the first column value to the set of printed values
            printed_values.add(first_column_value)

# Example usage
file_path = "F:\\JEAN FILES\\DOCUMENTS\\GEC CONTACT LL JULY.xlsx"
sheet_name = "Sheet1"
column_index = 0
message = "The values are: {}"

send_sms_with_unique_values(file_path, sheet_name, column_index, message)
