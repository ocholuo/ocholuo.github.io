---
title: "Meow's AWS - Developer Exam Flash Cards"
date: 2026-05-24 11:11:11 -0400
categories: [01Cloud, 01AWS]
tags: [AWS, Developer, exam, STS, IAM, CodeCommit, CloudFormation, ElasticBeanstalk]
math: false
toc: true
image: ""
---

# AWS Developer Exam — Flash Cards

---

## Overview

Concise Q&A flash cards covering AWS developer exam topics: STS, IAM, CodeCommit, CloudFormation, Elastic Beanstalk, and CodeDeploy.

---

## STS — Security Token Service

**Q: When requested through an STS API call, credentials are returned with what three components?**

<font color=OrangeRed>Security Token, Access Key ID, Secret Access Key</font>

<font color="blue">STS credentials are used to authenticate further API calls to AWS. The required components are: Security Token, Access Key ID, and Secret Access Key.</font>

---

**Q: Using STS to allow end users to authenticate from third-party providers such as Facebook, Google, and Amazon — what is this type of authentication called?**

<font color=OrangeRed>Web Identity Federation</font>

---

**Q: When using Web Identity Federation to allow a user to access an AWS service (such as an S3 bucket), which is the correct order of steps?**

<font color=OrangeRed>A user authenticates with Facebook first. They are then given an ID token by Facebook, which they can then trade for temporary security credentials.</font>

<font color="blue">The full flow:
1. Authenticate with Facebook → receive a web identity token.
2. Call AWS STS and pass the web identity token as input.
3. AWS STS authorizes the call and provides temporary AWS access credentials.
4. The user assumes an IAM role and accesses AWS resources in accordance with the role's security policy.</font>

---

## IAM — Identity and Access Management

**Q: Which of these are necessary fields in an IAM Policy?**

<font color=OrangeRed>Actions</font>

<font color=OrangeRed>Resources</font>

<font color=OrangeRed>Effects</font>

---

**Q: Which service can be used to securely store confidential information like credentials and license codes so that they can be accessed by EC2 instances?**

<font color=OrangeRed>Systems Manager Parameter Store</font>

<font color="blue">AWS Systems Manager Parameter Store provides secure, hierarchical storage for configuration data management and secrets management. Data such as passwords, database strings, and license codes can be stored as parameter values.</font>

---

## CodeDeploy — AppSpec File

**Q: When deploying application code to an EC2/On-Premises compute platform, the AppSpec file can be written in which language?**

<font color=OrangeRed>AppSpec files on an EC2/on-premises compute platform must be a YAML-formatted file named `appspec.yml` and it must be placed in the root of the directory structure of an application's source code. Otherwise, deployments fail.</font>

<font color=OrangeRed>AppSpec files on an AWS Lambda compute platform can be YAML-formatted or JSON-formatted.</font>

---

## CodeCommit — Notifications

**Q: To receive an email whenever a user pushes code to a CodeCommit repository, how can this be configured?**

<font color=OrangeRed>Configure Notifications in the console — this will create a CloudWatch Events rule to send a notification to an SNS topic which will trigger an email to be sent to the user.</font>

<font color=OrangeRed>CodeCommit can use a trigger to send events to Amazon SNS, but Amazon SNS cannot poll for CodeCommit events.</font>

---

## CloudFormation

**Q: Which two things can be defined using the Transforms section of the CloudFormation template?**

<font color=OrangeRed>To re-use code located in S3</font>

<font color=OrangeRed>To specify the use of the Serverless Application Model for Lambda deployments</font>

---

**Q: To use the output of a CloudFormation stack as input to another CloudFormation stack, which section of the CloudFormation template should be used?**

<font color=OrangeRed>Outputs</font>

<font color="blue">The `Outputs` section enables cross-stack references — one stack exports a value, and another stack imports it as input.</font>

---

**Q: How can you prevent CloudFormation from deleting an entire stack on failure?**

<font color=OrangeRed>Use the `--disable-rollback` flag with the AWS CLI</font>

<font color=OrangeRed>Set the 'Rollback on failure' radio button to No in the CloudFormation console</font>

---

## Elastic Beanstalk — Docker Deployment

**Q: An application is running using Docker provisioned with Elastic Beanstalk. How should the application be upgraded to a new version?**

<font color=OrangeRed>Bundle the code into a zip file, upload and deploy it using the Elastic Beanstalk console.</font>

---

## Key Takeaways

- <font color=OrangeRed>STS credentials</font> = Security Token + Access Key ID + Secret Access Key
- <font color=OrangeRed>Web Identity Federation</font> = authenticate with third-party (Facebook/Google/Amazon) → get token → trade for STS temp credentials
- <font color=OrangeRed>IAM Policy required fields</font>: Actions, Resources, Effects
- <font color=OrangeRed>Parameter Store</font>: secure hierarchical storage for secrets/config (passwords, DB strings, license codes)
- <font color=OrangeRed>AppSpec file</font>: YAML-only for EC2/on-premises (`appspec.yml` at root); YAML or JSON for Lambda
- <font color=OrangeRed>CodeCommit notifications</font>: CloudWatch Events → SNS topic → email
- <font color=OrangeRed>CloudFormation Transforms</font>: re-use S3 code + SAM for Lambda
- <font color=OrangeRed>CloudFormation Outputs</font>: cross-stack value passing
- <font color=OrangeRed>Beanstalk Docker upgrade</font>: zip file → upload via console
- <font color=OrangeRed>CloudFormation rollback prevention</font>: `--disable-rollback` or set Rollback on failure = No

## References

- Linux Academy AWS Developer course notes
- AWS Developer Associate exam study material
