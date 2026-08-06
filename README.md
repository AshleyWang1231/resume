# Lu Wang — AI Engineer Portfolio + AWS Visitor Board

Static bilingual resume/portfolio site extended with an AWS serverless homework feature: the **Interactive Resume Visitor Board**.

## Current public assignment architecture

```text
S3 static frontend → Lambda Function URL → DynamoDB
```

The public page should be evaluated through the Visitor Board:

- visitor enters required `name` and `message`
- frontend calls the Lambda Function URL
- Lambda validates input and stores messages in DynamoDB
- frontend loads submitted messages back from DynamoDB

The old floating resume-agent terminal is not part of the public page. Legacy non-AWS backend code may remain in `backend/`, but it is not the homework feature.

## Frontend

Upload only these public static files to S3:

```text
index.html
styles.css
script.js
assets/
```

Before uploading, set `VISITOR_BOARD_API` in `script.js` to the deployed Lambda Function URL.

## AWS backend

AWS resources and Lambda code live in:

```text
aws/
```

Key files:

```text
aws/lambda/visitor_board.py       # Lambda handler
aws/lambda/test_visitor_board.py  # local tests
aws/cloudformation.yaml           # starter AWS resources
aws/README.md                     # deployment notes
```

## Local preview

```bash
python3 -m http.server 8000
# open http://localhost:8000
```

Without a deployed Lambda URL, the Visitor Board shows that the API is not configured yet.

## Verification

```bash
node --check script.js
python3 -m py_compile aws/lambda/visitor_board.py
python3 -m pytest aws/lambda/test_visitor_board.py -q
```
