# StatusPing

A serverless uptime monitor built on AWS and Cloudflare. StatusPing checks a list of websites every 5 minutes, stores the results in a database, and displays live status on a public dashboard — with zero servers to manage.

**Live dashboard:** https://statusping.mdmuzam7.workers.dev

## What it does

- Checks a list of websites on a schedule (every 5 minutes)
- Records whether each site is up, its HTTP status code, and its response time
- Stores every check in a database, building a history over time
- Exposes the latest results through a public REST API
- Displays live status on a simple web dashboard, deployed with automatic SSL

## Architecture

```
EventBridge (5-min timer)
        |
        v
Lambda: checker  -->  DynamoDB (stores results)
                            |
                            v
                      Lambda: reader
                            |
                            v
                      API Gateway (/status)
                            |
                            v
                  Cloudflare dashboard (HTML/JS)
```

- **AWS Lambda** — two functions: one checks websites and writes results, one reads the latest results back out
- **Amazon EventBridge** — triggers the checker function automatically every 5 minutes, so it runs unattended
- **Amazon DynamoDB** — stores every check, keyed by URL and timestamp, so history builds up over time
- **Amazon API Gateway** — exposes the reader function as a public REST endpoint (`GET /status`)
- **Cloudflare** — hosts the dashboard as a static site with automatic SSL, redeploying on every push to GitHub

## Tech stack

Python (boto3), AWS Lambda, DynamoDB, EventBridge, API Gateway, IAM, HTML/CSS/JavaScript, Cloudflare, Git

## What I learned

This was my first hands-on project with AWS and cloud infrastructure. Along the way I learned:
- How to set up least-privilege IAM users and roles instead of using root/admin access everywhere
- The serverless model — writing code that only runs (and is only billed) when triggered, with no server to maintain
- How NoSQL databases like DynamoDB use partition keys and sort keys to organize data
- How to expose a backend function as a public API using API Gateway, including CORS
- How static site hosting and SSL work in practice, deploying through Cloudflare

## Running it yourself

The Python files (`checker.py`, `reader.py`) are written to run as AWS Lambda functions and expect `boto3` (provided automatically in the Lambda runtime) plus a DynamoDB table named `statusping-results` with `url` as the partition key and `timestamp` as the sort key. `index.html` is a static file that can be served from any static host — just update the `API_URL` constant to point at your own API Gateway endpoint.