# AWS Visitor Board Deployment Notes

This folder contains the Lambda source for the homework assignment feature.

## Required AWS resources

- S3 static website bucket for public files only:
  - `index.html`
  - `styles.css`
  - `script.js`
  - `assets/`
- Lambda function: `resumeVisitorApi`
- Lambda Function URL: public backend endpoint
- DynamoDB table: `ResumeVisitorMessages`
  - partition key: `id` string
  - billing mode: on-demand

## Lambda environment variables

| Name | Value |
|---|---|
| `TABLE_NAME` | `ResumeVisitorMessages` |
| `ALLOWED_ORIGIN` | final S3 website origin |
| `MAX_MESSAGES` | `25` |
| `EDIT_WINDOW_SECONDS` | `180` |

## IAM

Attach AWS managed policy `AWSLambdaBasicExecutionRole` for CloudWatch Logs.

Add one inline DynamoDB policy scoped to the `ResumeVisitorMessages` table ARN with only:

```text
dynamodb:PutItem
dynamodb:Scan
dynamodb:GetItem
dynamodb:UpdateItem
dynamodb:DeleteItem
```

Do not use `dynamodb:*` or `Resource: *`.

## Owner-token edit/delete bonus

`POST /messages` returns a short-lived `editToken` and `editExpiresAt`. The raw token is shown only to the original browser session; DynamoDB stores only `editTokenHash`. `PATCH /messages/{id}` and `DELETE /messages/{id}` require the token and are rejected after `EDIT_WINDOW_SECONDS`.

Do not log request bodies or put edit tokens in URLs.

## Optional CloudFormation starter

`cloudformation.yaml` creates the S3 bucket, DynamoDB table, Lambda role, Lambda function, and Function URL. Package and deploy both `lambda/index.py` and `lambda/visitor_board.py`; the configured handler is `index.lambda_handler`, and `index.py` delegates to the visitor-board handler.

## CORS

`lambda/visitor_board.py` is the single source of truth for CORS response headers, including `GET`, `POST`, `PATCH`, `DELETE`, and `OPTIONS`. Keep Lambda Function URL CORS disabled in infrastructure so headers are not configured in two places.

## Frontend configuration

Set `VISITOR_BOARD_API` in `script.js` to the Lambda Function URL before uploading public static files to S3.
