# app.py (V1)
import json
import os
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
# 環境変数からテーブル名を取得
table_name = os.environ.get('TABLE_NAME', 'BookshelfTable')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        # API Gateway等からの呼び出しを想定
        body = json.loads(event.get('body', '{}'))
        
        # V1仕様: titleのみ必須、他は任意
        title = body.get('title')
        if not title:
            raise ValueError("title is required")

        item = {
            'book_id': str(uuid.uuid4()),
            'title': title,
            'author': body.get('author', 'Unknown') # authorがなくてもUnknownとして登録
        }
        
        table.put_item(Item=item)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Book added successfully", "item": item})
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to process request: {e}")
        # LambdaのErrorメトリクスを発生させるために例外を再送出する
        raise e