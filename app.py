# app.py (V2: LTの障害デモ用コード)
import json
import os
import uuid
import boto3

dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('TABLE_NAME', 'BookshelfTable')
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    try:
        body = json.loads(event.get('body', '{}'))
        
        # 【仕様変更】データの取得方法を厳格化し、rating(評価)を必須項目にする
        title = body['title'] 
        author = body['author']
        
        # V1の古い形式のデータが送られてくると、ここに'rating'キーが存在しないため KeyError でクラッシュします
        rating = int(body['rating']) 
        
        item = {
            'book_id': str(uuid.uuid4()),
            'title': title,
            'author': author,
            'rating': rating
        }
        
        table.put_item(Item=item)
        
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Book added successfully", "item": item})
        }
        
    except Exception as e:
        print(f"[ERROR] Failed to process request: {e}")
        # CloudWatchのErrorsメトリクスを上昇させるためにエラーを再送出
        raise e