FROM public.ecr.aws/lambda/python:3.12

# 依存関係のコピーとインストール
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Lambdaコードのコピー
COPY app.py ${LAMBDA_TASK_ROOT}

# ハンドラーの設定
CMD [ "app.lambda_handler" ]