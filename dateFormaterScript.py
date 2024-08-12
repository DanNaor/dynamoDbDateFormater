import sys
import boto3
from datetime import datetime

def format_date(item):
    RED = '\033[91m'
    RESET = '\033[0m'
    
    # Define the date format conversion function
    if 'created_at' in item:
        try:
            # Attempt to parse the first date format
            current_date = datetime.strptime(item['created_at'], '%Y-%m-%d %H:%M:%S.%f')
            print(f"Updated item: {item['id']}")

        except ValueError:
            try:
                # Attempt to parse the second date format
                current_date = datetime.strptime(item['created_at'], '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                print(f"{RED}Error formatting date: {e}{RESET}")
                return item
        # Format the date to the required format
        formatted_date = current_date.strftime('%d/%m/%Y %H:%M:%S')
        item['created_at'] = formatted_date
    return item

def update_table_items(table_name):
    # Initialize DynamoDB client
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')

    # Get the DynamoDB table
    table = dynamodb.Table(table_name)

    # Scan the table and format 'created_at' for each item
    response = table.scan()
    items = response['Items']

    for item in items:
        updated_item = format_date(item)
        if 'created_at' in updated_item:
            # Update the item in DynamoDB if 'created_at' exists in updated_item
            table.update_item(
                Key={'id': item['id']},
                UpdateExpression="SET created_at = :val1",
                ExpressionAttributeValues={':val1': updated_item['created_at']}
            )
        else:
            print(f"Skipped item {item['id']} because 'created_at' field is missing")

    print("Table update completed.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python update_table.py <table_name>")
        sys.exit(1)
    
    table_name = sys.argv[1]
    update_table_items(table_name)
