import csv
import time
import requests

api = "ENTER YOUR API KEY OF NUMVERIFY.COM"

def validate_number(number):
    try:
        url = f"https://apilayer.net/api/validate?access_key={api}&number={number}&country_code=&format=1"
        print(f"Processing number: {number}")
        response = requests.get(url)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Failed to process number {number}: {e}")
        return None

def display_formatted_response(json_response):
    print(" ")
    print("-" * 40)
    print(" ")
    print(f"Number Status: {'Valid' if json_response.get('valid') else 'Invalid'}")
    print(f"Number: {json_response.get('number')}")
    print(f"Local Format: {json_response.get('local_format')}")
    print(f"International Format: {json_response.get('international_format')}")
    print(f"Country Prefix: {json_response.get('country_prefix')}")
    print(f"Country Code: {json_response.get('country_code')}")
    print(f"Country Name: {json_response.get('country_name')}")
    print(f"Location: {json_response.get('location') or 'Not Found'}")
    print(f"Carrier: {json_response.get('carrier') or 'Not Found'}")
    print(f"Line Type: {json_response.get('line_type').capitalize() if json_response.get('line_type') else 'Not Found'}")
    print(" ")
    print("-" * 40)
    print(" ")

def main():
    try:
        with open('input.csv', mode='r') as input_file:
            csv_reader = csv.reader(input_file)
            numbers = [row[0] for row in csv_reader if row and row[0].strip()]

        with open('output.csv', mode='w', newline='') as output_file:
            csv_writer = csv.writer(output_file)
            csv_writer.writerow([
                "Number", "Valid", "Local Format", "International Format", 
                "Country Prefix", "Country Code", "Country Name", 
                "Location", "Carrier", "Line Type"
            ])

            for number in numbers:
                json_response = validate_number(number)
                if json_response:
                    display_formatted_response(json_response)
                    csv_writer.writerow([
                        json_response.get("number"),
                        json_response.get("valid"),
                        json_response.get("local_format"),
                        json_response.get("international_format"),
                        json_response.get("country_prefix"),
                        json_response.get("country_code"),
                        json_response.get("country_name"),
                        json_response.get("location"),
                        json_response.get("carrier"),
                        json_response.get("line_type")
                    ])
                time.sleep(1)

        print("Processing completed. Check output.csv for results.")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
