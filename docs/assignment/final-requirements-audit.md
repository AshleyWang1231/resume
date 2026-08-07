# Final Requirements Audit — Homework Assignment

Audit target: `Homework_Assignment.pdf`  
Project audited: `/Users/wang.lu/Documents/Assignment/resume`  
Public URL audited: http://resume-visitor-board-011578632495-ap-southeast-1.s3-website-ap-southeast-1.amazonaws.com

## Executive Summary

The deployed submission satisfies the assignment’s core requirements: it is a publicly accessible working serverless app using **S3**, **Lambda Function URL**, and **DynamoDB**. The app allows users to create and read visitor-board messages, and it also implements the optional update/delete bonus through a three-minute owner-token mechanism. The AI Collaboration Snapshot is present, under 500 words, includes actual prompts from this session, and describes one real AI mistake plus how it was fixed.

No critical requirement gaps were found in the final audit.

## Evidence Commands Run

The final audit executed live checks against AWS plus local code checks. Raw output was captured at:

```text
/tmp/final_assignment_audit_raw.txt
```

Key verification commands included:

```bash
node --check script.js
python3 -m py_compile aws/lambda/visitor_board.py aws/lambda/index.py
python3 -m pytest aws/lambda/test_visitor_board.py -q
curl -I http://resume-visitor-board-011578632495-ap-southeast-1.s3-website-ap-southeast-1.amazonaws.com
curl /messages against the deployed Lambda Function URL
aws dynamodb describe-table --table-name ResumeVisitorMessages
aws lambda get-function-url-config --function-name resumeVisitorApi
aws lambda get-policy --function-name resumeVisitorApi
aws iam get-role-policy --role-name resumeVisitorApiRole --policy-name ResumeVisitorMessagesDynamoDBAccess
```

Local automated tests passed:

```text
12 passed in 0.03s
```

---

## Requirement-by-Requirement Audit

### 1. Core deliverable: publicly accessible working URL

**Requirement from assignment:** Submit a publicly accessible working URL where the evaluator can actually use the app.

**Status:** PASS

**Evidence:**

The public S3 website returned `HTTP/1.1 200 OK`:

```text
http://resume-visitor-board-011578632495-ap-southeast-1.s3-website-ap-southeast-1.amazonaws.com
```

Audit output confirmed:

```text
PASS: public URL loads HTML
PASS: S3 page includes Visitor Board
PASS: S3 page includes name input
PASS: S3 page includes message textarea
```

---

### 2. Real-world scenario requiring write and read

**Requirement from assignment:** Pick a small real-world scenario requiring both writing data and reading it back.

**Status:** PASS

**Scenario implemented:** Interactive Resume Visitor Board.

Visitors can submit a public name/message on the resume site and see messages loaded from DynamoDB.

**Evidence:**

Live API check confirmed create/read behavior:

```text
POST_STATUS 201
GET_STATUS 200
GET_COUNT 2
PASS: live API supports create/read/update/delete with owner-token controls and public redaction
```

---

### 3. S3 requirement

**Requirement from assignment:** Use S3 to host the frontend as a static website.

**Status:** PASS

**Evidence:**

S3 website URL returned public HTML:

```text
HTTP/1.1 200 OK
Server: AmazonS3
Content-Type: text/html
```

The public page includes the static frontend and Visitor Board. Audit confirmed:

```text
PASS: deployed script has Lambda URL
PASS: deployed CSS has visitor board styles
```

---

### 4. Lambda requirement

**Requirement from assignment:** Use Lambda to run backend logic, exposed via Function URL or API Gateway.

**Status:** PASS

**Implementation:** AWS Lambda Function URL.

**Evidence:**

Function URL configuration:

```json
{
  "FunctionUrl": "https://mq3a4e5i6lmbukdxisaiq6ivcq0pcvxh.lambda-url.ap-southeast-1.on.aws/",
  "AuthType": "NONE",
  "InvokeMode": "BUFFERED"
}
```

Live API routes verified:

```text
OPTIONS_STATUS 204
POST_STATUS 201
PATCH_STATUS 200
DELETE_STATUS 200
GET_STATUS 200
```

---

### 5. DynamoDB requirement

**Requirement from assignment:** Use DynamoDB to store and retrieve all data.

**Status:** PASS

**Evidence:**

DynamoDB table:

```json
{
  "TableName": "ResumeVisitorMessages",
  "KeySchema": [
    {
      "AttributeName": "id",
      "KeyType": "HASH"
    }
  ],
  "BillingMode": "PAY_PER_REQUEST",
  "Status": "ACTIVE"
}
```

Current table count during audit:

```json
{
  "Count": 2,
  "ScannedCount": 2
}
```

Live API read from DynamoDB returned two polished sample messages.

---

### 6. Minimum create/read functionality

**Requirement from assignment:** At minimum, users must be able to create one item and view all items.

**Status:** PASS

**Evidence:**

Live test created a temporary message:

```text
POST_STATUS 201
```

Live `GET /messages` succeeded afterward:

```text
GET_STATUS 200
```

The temporary audit message was deleted after verification so the public board returned to the two polished sample messages.

---

### 7. Optional update/delete bonus

**Requirement from assignment:** Bonus points are optional for update/delete functionality beyond create/read.

**Status:** PASS — implemented safely with owner-token mechanism.

**Implementation:**

- `PATCH /messages/{id}` updates a message.
- `DELETE /messages/{id}` deletes a message.
- Both require a temporary `editToken` returned only after creation.
- Token is valid for three minutes.
- DynamoDB stores only `editTokenHash`, not the raw token.
- Public `GET /messages` does not expose token fields.

**Evidence:**

Live audit output:

```text
BAD_PATCH_STATUS 403 {'error': 'Invalid edit token.'}
PATCH_STATUS 200
DELETE_STATUS 200 {'ok': True}
PASS: live API supports create/read/update/delete with owner-token controls and public redaction
```

---

### 8. CORS handling

**Requirement from evaluation rubric:** Production thinking includes CORS handling.

**Status:** PASS

**Evidence:**

Live preflight response:

```text
OPTIONS_STATUS 204
OPTIONS_ALLOW_METHODS GET,POST,PATCH,DELETE,OPTIONS
```

Lambda is the single source of truth for CORS headers.

---

### 9. Basic input validation

**Requirement from evaluation rubric:** Production thinking includes basic input validation.

**Status:** PASS

**Evidence:**

Live API rejected non-string input:

```text
NON_STRING_STATUS 400 {'error': 'Name and message must be text.'}
```

Local tests also cover:

- empty name rejection
- non-object JSON body rejection
- invalid edit token rejection
- expired edit token rejection

---

### 10. Least-privilege IAM

**Requirement from evaluation rubric:** Consider least-privilege IAM roles.

**Status:** PASS, with one note.

**Evidence:**

Lambda role has AWS basic logging policy:

```json
{
  "PolicyName": "AWSLambdaBasicExecutionRole"
}
```

Inline DynamoDB policy is scoped to one table:

```json
{
  "Action": [
    "dynamodb:PutItem",
    "dynamodb:Scan",
    "dynamodb:GetItem",
    "dynamodb:UpdateItem",
    "dynamodb:DeleteItem"
  ],
  "Resource": "arn:aws:dynamodb:ap-southeast-1:011578632495:table/ResumeVisitorMessages",
  "Effect": "Allow"
}
```

Lambda public invoke permission is scoped to Function URL invocation:

```text
PASS: public InvokeFunction permission is scoped to Function URL
```

**Note:** `dynamodb:Scan` is intentionally used for this small demo. For a production-scale board, a createdAt-indexed query would be better.

---

### 11. Service integration soundness

**Requirement from evaluation rubric:** S3 → Lambda → DynamoDB integration must be sound.

**Status:** PASS

**Evidence:**

The deployed S3 page contains the Lambda URL in `script.js`, and live API calls created, read, updated, and deleted DynamoDB-backed records.

Audit output:

```text
PASS: deployed script has Lambda URL
PASS: live API supports create/read/update/delete with owner-token controls and public redaction
```

---

### 12. AI Collaboration Snapshot

**Requirement from assignment:** Submit a one-page AI Collaboration Snapshot, approximately 500 words, including scenario, architecture summary, at least two actual prompts, what they helped achieve, one AI mistake, and how it was fixed/refined.

**Status:** PASS

**Snapshot file:**

```text
/Users/wang.lu/Documents/Assignment/ai-collaboration-snapshot.md
```

Audit output:

```text
word_count 424
PASS: under 500 words
PASS: public URL included
PASS: scenario included
PASS: architecture included
PASS: two prompts included
PASS: AI wrong/fix included
PASS: bonus reflected
```

---

### 13. Optional full AI transcript link

**Requirement from assignment:** Optional.

**Status:** Not included.

**Assessment:** This is acceptable because the assignment marks full transcript link as optional. The required AI Collaboration Snapshot is present and satisfies the required contents.

---

## Final Submission Checklist

| Submission item | Status | Evidence |
|---|---|---|
| Public working URL | PASS | S3 URL returns 200 and page includes Visitor Board |
| One-page AI Collaboration Snapshot | PASS | 424 words, required fields present |
| Full transcript link | Optional / not included | Not required |
| Update/delete functionality | PASS | PATCH/DELETE verified live with owner token |

## Final URLs

Public app URL:

```text
http://resume-visitor-board-011578632495-ap-southeast-1.s3-website-ap-southeast-1.amazonaws.com
```

Lambda Function URL:

```text
https://mq3a4e5i6lmbukdxisaiq6ivcq0pcvxh.lambda-url.ap-southeast-1.on.aws/
```

## Final Audit Conclusion

Based on the evidence gathered in this audit, the submission is ready. It satisfies the assignment’s core requirements, includes the optional update/delete bonus, demonstrates production-thinking items requested in the rubric, and includes a concise AI Collaboration Snapshot based on actual prompts and actual issues from the build process.
