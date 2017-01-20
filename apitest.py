import boto3
from flask import Flask
from flask.json import jsonify
from flask import request

app = Flask(__name__)

dynamo = boto3.client('dynamodb', region_name='us-east-1')

#### FLASK API to LIST DYNAMO TABLES in the Account

@app.route("/listtables")
def list_tables():
    response = dynamo.list_tables(
    )
    tablenames = response['TableNames']
    return jsonify({'TableNames': tablenames})

### GET API to retrieve all items in the table
### POST API to put item in the same table

@app.route("/accounts", methods=['GET', 'POST'])
def add_accounts():

    if request.method == 'POST':
        response_put_item = dynamo.put_item(
            TableName='AWSAccounts',
            Item={
                'AccountID': {
                    "S": request.args['account_number']
                }
            },
            ConditionExpression='attribute_not_exists(AccountID)'
        )
        return jsonify(response_put_item)

    if request.method == 'GET':
        response_scan_table = dynamo.scan(
            TableName='AWSAccounts',
            Limit=5,
            Select='ALL_ATTRIBUTES',
            ReturnConsumedCapacity='TOTAL',
            ConsistentRead=True
        )
        return jsonify(response_scan_table)


if __name__ == "__main__":
    app.run()
