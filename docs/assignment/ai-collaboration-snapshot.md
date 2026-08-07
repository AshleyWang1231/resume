# AI Collaboration Snapshot

Public URL: http://resume-visitor-board-011578632495-ap-southeast-1.s3-website-ap-southeast-1.amazonaws.com

## Scenario and architecture

I chose to reuse my existing resume website and add an **Interactive Resume Visitor Board**. Visitors can **submit** a public name/message, **see** stored messages, and **edit** or **delete** their own message for three minutes using a temporary owner token.

**Architecture summary**: the existing static HTML/CSS/JavaScript resume frontend is hosted on **S3**, calls an **AWS Lambda Function URL**, and Lambda stores visitor-board data in **DynamoDB**.

## Actual prompts and what they helped with

Prompt 1:

> “not my types, i'm thikning using my resume to complete this assignment, analyze feasibility:https://github.com/AshleyWang1231/resume
>
>  show me a recommended implementation strategy that keeps the project small but high-scoring.”

This helped me stop thinking about generic ideas like a todo app or poll. The useful direction was to keep my existing resume site and add one small create/read feature that clearly used S3, Lambda, and DynamoDB.

Prompt 2:

> “The visitor board is the assignment feature and must use:
> 1. S3 for frontend
> 2. Lambda Function URL for the backend
> 3. DynamoDB for storing data”

This helped tighten the scope. It made the Visitor Board the actual assignment feature, while treating the existing AI resume agent, Aliyun, DeepSeek, and Cloudflare backend as separate portfolio context rather than the homework solution.

Prompt 3:

> “what if we add a timer? Can the current token be updated and deleted within 3 minutes? is this reasonable?”

This helped turn the optional update/delete bonus into a safer design. Instead of allowing public delete, I added a short-lived owner-token approach: the creator receives an edit token, Lambda stores only a token hash, and PATCH/DELETE are allowed only within three minutes.

## What AI got wrong or incomplete

The first suggested delete-bonus idea was not safe enough: it would have allowed public delete without authentication. I pushed back that no one should be able to delete information without auth, and refined the design into a temporary owner-token model.

Deployment also exposed incomplete AI guidance. The Lambda Function URL returned `403`, then `502`. I used AWS CLI output and CloudWatch logs to find the real problems: missing/incorrect invoke permission and handler/package mismatch. I fixed this by updating CloudFormation, using an `index.py` wrapper, scoping public invocation to the Function URL, redeploying Lambda/S3, and verifying live GET/POST/PATCH/DELETE behavior.

## Production choices

I added CORS headers in Lambda, input validation, safe frontend rendering with `textContent`, token hashing, server-enforced token expiration, no token fields in public GET responses, and DynamoDB IAM scoped to the `ResumeVisitorMessages` table.
