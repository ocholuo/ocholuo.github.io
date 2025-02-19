---
title: AWS - Security - GuardDuty (AWS account and workloads)
date: 2020-07-18 11:11:11 -0400
categories: [01AWS, CloudSecurity]
tags: [AWS, AWSSecurity]
toc: true
image:
---

- [GuardDuty](#guardduty)
  - [how Amazon GuardDuty works](#how-amazon-guardduty-works)
  - [enable Amazon GuardDuty](#enable-amazon-guardduty)


---


# GuardDuty

> identify malicious/unauthorized activity in `AWS account and workloads`

![Pasted Graphic](https://i.imgur.com/XJAk8xl.jpg)

- Designed to <font color=OrangeRed> actively protect </font> the environment from threats.

- intelligent <font color=OrangeRed> threat detection service </font>

- continuously <font color=OrangeRed> analyzes and monitor events </font> across the accounts, protect the accounts and workloads.
  - such as
    - information about AWS user and API activity in accounts from CloudTrail,
    - network traffic data from Amazon VPC Flow Logs,
    - name query patterns from DNS logs.

- <font color=OrangeRed> monitors environment for malicious / unauthorized activiaty </font>
  - activities that can associated with account / instance compromise, and malicious reconnaissance.
  - such as
    - unusual API calls or potentially unauthorized deployments that indicate a possible account compromise.
    - suspicious outbound communications to known malicious IP addresses
    - possible data theft that use DNS queries as the transport mechanism
    - detects potentially compromised instances or reconnaissance by attackers.
    - identify malicious or unauthorized activities in AWS accounts

- delivers more accurate findings by machine learning
  - Use threat intelligence feeds to detect threats to the environment. such as lists of malicious IPs and domains.
  - can customize GuardDuty by adding your own threat lists and trusted IP lists.

- can enable GuardDuty through AWS Management Console
  - and have access to a more intelligent and cost-effective option for threat detection in the AWS Cloud

- GuardDuty analyzes and processes data from:
  - The origin or location of a set of data
  - CloudTrail event logs
  - VPC Flow Logs
  - And DNS logs


Term
- Account:
  - standard AWS account that contains your AWS resources.
  - can sign in to AWS with your account, and enable GuardDuty.
  - can invite other accounts to enable GuardDuty, and these accounts can be associated with your AWS account in GuardDuty.
    - If your invitations are accepted,
    - your account is <font color=LightSlateBlue> master GuardDuty account </font>
    - the added accounts is your member accounts.
    - view and manage GuardDuty findings for member accounts
- data source:
  - the origin or location of a set of data.
  - To detect unauthorized and unexpected activity in AWS environment, GuardDuty analyzes and processes data from:
    - The origin or location of a set of data
    - CloudTrail event logs
    - VPC Flow Logs
    - And DNS logs
- finding
  - a potential security issue that is discovered by GuardDuty.
  - Findings are displayed in the GuardDuty console
  - contain a detailed description of the security issue.
- trusted IP list
  - a list of whitelisted IP addresses for highly secure communication with AWS environment.
  - GuardDuty does not generate findings based on trusted IP lists.
- <font color=LightSlateBlue> threat list </font>
  - list of known malicious IP addresses.
  - GuardDuty generates findings based on threat lists.

---
￼
## how Amazon GuardDuty works
1. connect all accounts, and enable GuardDuty within the AWS console.
   - use the console to monitor the AWS accounts
   - without additional security software or infrastructure to deploy or manage.
2. GuardDuty looks at <font color=LightSlateBlue> CloudTrail Events, VPC Flow Logs, and DNS Query Logs </font>
   - continuously analyzes those logs.
   - automatically analyzes network and account activity at scale,
   - provides broad, continuous monitoring of your AWS accounts and workloads.
3. intelligently detects threats and malicious or authorized behavior
   - by using
   - <font color=LightSlateBlue> managed rule sets </font>
   - <font color=LightSlateBlue> integrated threat intelligence </font>
   - <font color=LightSlateBlue> anomaly detection </font>
   - and <font color=LightSlateBlue> machine learning </font>
4. After GuardDuty detects a threat,
   - it can use actionable alerts to review detailed findings in the console,
   - integrate into event management or workflow systems,
   - or trigger AWS Lambda for automated remediation or prevention.

---


## enable Amazon GuardDuty

![Screen Shot 2020-07-13 at 23.11.35](https://i.imgur.com/Pg30tK2.png)

- AWS console > GuardDuty > enable GuardDuty.
- When enable GuardDuty
  - you give it permission to set up the appropriate service-linked roles and to analyze your logs.
- A <font color=OrangeRed> service-linked role </font> is a unique type of IAM role
  - Is linked directly to an AWS service
  - Service-linked roles are predefined by the service
  - defines how you create, modify, and delete a service-linked role.
  - include all the permissions that the service requires to call other AWS services on your behalf.

- When you enable GuardDuty, it immediately starts analyzing your VPC Flow Logs data.
  - It consumes VPC Flow Log events directly from the VPC Flow Logs feature through an independent and duplicative stream of flow logs.
  - This process <font color=LightSlateBlue> does not affect any existing flow log configurations </font> that might have.
  - GuardDuty does not manage flow logs or make them accessible in your account.
    - To manage the access and retention of your flow logs, you must configure the VPC Flow Logs feature.

- no additional charge for Amazon GuardDuty access to flow logs.
  - However, enabling flow logs for retention or use in your account is subject to existing pricing

- After you enable GuardDuty, findings are displayed in the console.
  - The slide shows an example of the kinds of findings that are available in the console.
  - To access the findings: General Settings > Generate Sample Findings.

![Screen Shot 2020-07-13 at 23.20.14](https://i.imgur.com/HALa7pM.png)



















.
