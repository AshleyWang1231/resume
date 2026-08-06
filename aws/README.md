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

## IAM

Attach AWS managed policy `AWSLambdaBasicExecutionRole` for CloudWatch Logs.

Add one inline DynamoDB policy scoped to the `ResumeVisitorMessages` table ARN with only:

```text
dynamodb:PutItem
dynamodb:Scan
```

Do not use `dynamodb:*` or `Resource: *`.

## Optional CloudFormation starter

`cloudformation.yaml` creates the S3 bucket, DynamoDB table, Lambda role, Lambda function, and Function URL. The template uses placeholder inline Lambda code because CloudFormation cannot inline the full handler cleanly. After creating the stack, update the Lambda function code with `lambda/visitor_board.py`.

## Frontend configuration

Set `VISITOR_BOARD_API` in `script.js` to the Lambda Function URL before uploading public static files to S3.
