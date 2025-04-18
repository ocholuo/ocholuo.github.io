<!-- ---
title: AWS - Security
date: 2020-07-18 11:11:11 -0400
categories: [01AWS, CloudSecurity]
tags: [AWS, AWSSecurity]
toc: true
image:
--- -->

- [AWS - Security](#aws---security)
  - [audit](#audit)



---


# AWS - Security

click for detailed note


[AWS Organizations]()
- restrict what services and actions are allowed in accounts.
- consolidate multiple AWS accounts into an organization to create and centrally manage.
- Each paying account is an independent entity and is not able to access resources of other accounts in the Organization.
- <font color=OrangeRed> The billing is performed centrally on the root account </font> in the AWS Organization.



[AWS Systems Manager]()
- gives visibility and control of the <font color=OrangeRed> infrastructure on AWS </font>
- provides a unified user interface, view operational data from multiple AWS services
- to <font color=OrangeRed> automate operational tasks across your AWS resources </font>
￼


[AWS Secrets Manager ]()
- <font color=OrangeRed> protects the secrets you use for access </font> to applications, services and IT resources.
- easily rotate, manage, and retrieve database credentials, API keys, and other secrets throughout their lifecycle.


[TAM: Technical account manager: ]()
- Only for the <font color=OrangeRed> enterprise support plan </font>
- A dedicated voice in AWS to serve as your advocate.
- <font color=OrangeRed> Proactive guidance and insight </font> into ways to <font color=OrangeRed> optimize AWS through business and performance reviews </font>
  - Orchestration and access to the full breadth and depth of technical expertise across the full range of AWS.
  - And access to <font color=OrangeRed> resources and best practice recommendations </font>


[Infrastructure Event Management]()
- A common understanding of <font color=OrangeRed> event objectives and use cases </font> through pre-event planning and preparation.
- Resource recommendations and deployment guidance based on anticipated capacity needs.
- Dedicated attention of your AWS Support team during your event.
- And the ability to <font color=OrangeRed> immediately scale down resources to normal operating levels post-event </font>


[Service Health Dashboard]()
- general status of AWS services,  
- shows the current status of services across regions.
- but not provide proactive notifications of scheduled activities or guidance of any kind.


[AWS Personal Health Dashboard ]()
- provides <font color=OrangeRed> alerts and remediation guidance </font> when AWS is experiencing events that may impact you.
- <font color=OrangeRed> personalized view </font> into the performance and availability of the AWS services underlying your AWS resources.
  - displays relevant and timely information to help manage events in progress
  - provides <font color=OrangeRed> proactive notifications to help plan for scheduled activities </font>
    - forward-looking notifications.
    - can set alerts across multiple channels, including email and mobile notifications.
    - alerts are triggered by changes in the health of AWS resources,
    - giving you event visibility, and guidance to help quickly diagnose and resolve issues.
- Having an AWS account grants you access to the Personal Health Dashboard to receive alerts and remediation guidance regarding events affecting the services underlying your resources.
- Business or Enterprise support plan, also get AWS Health API for integrating health data and notifications with your existing in-house and third-party IT management tools.



[AWS Security Hub]()
- <font color=OrangeRed> consolidates view of your security and compliance status </font> in the cloud.
- Unified security and compliance center



[AWS support concierge 门房:]()
- A primary contact to help manage AWS resources.
- account assistance
- Only for the <font color=OrangeRed> enterprise support plan </font>
- <font color=OrangeRed> non-tech billing and account level inquiries </font>
  - Personalized handling of billing inquiries, tax questions, service limits, and bulk reserve instance purchases.
  - answering billing and account questions
  - direct access to an agent to help optimize costs to identify underused resources




[Guard Duty]()
- a <font color=OrangeRed> threat detection service </font>
- Designed to <font color=OrangeRed> actively protect </font> the environment from threats.
- <font color=OrangeRed> monitors environment, and identify malicious/unauthorized activity </font> in AWS account and workloads
  - such as <font color=LightSlateBlue> unusual API calls or potentially unauthorized deployments </font> that indicate a possible account compromise.
  - detects <font color=LightSlateBlue> potentially compromised instances or reconnaissance </font> by attackers.
  - continuously monitor and <font color=OrangeRed> protect AWS accounts and workloads </font>
  - can <font color=OrangeRed> identify malicious or unauthorized activities </font> in AWS accounts
- Use <font color=OrangeRed> threat intelligence </font> feeds to detect threats to the environment.


[AWS Config]()
- fully-managed service
- a service assess,
- enables and simplify:

- <font color=OrangeRed> security analysis </font>
  - continuously monitors and records AWS resource configurationsd
  - discover existing and deleted AWS resources
  - dive into configuration details of a resource at any point in time.

- <font color=OrangeRed> change management </font>
  - <font color=LightSlateBlue> audit, evaluate, and monitor changes and Aconfigurations </font> of AWS resources.
  - track resource inventory and changes.
  - review changes in configurations and relationships between AWS resources
  - dive into detailed resource configuration histories,
  - provides an <font color=LightSlateBlue> AWS resource inventory, configuration history, and configuration change notifications </font> to <font color=OrangeRed> enable security and regulatory compliance </font>
  - allows to <font color=LightSlateBlue> automate the evaluation of recorded configurations </font> against desired configurations.

- <font color=OrangeRed> compliance auditing </font>
  - determine your overall compliance against rules/configurations specified in your internal guidelines.
- and <font color=OrangeRed> operational troubleshooting </font>


## audit

[CloudTrail]() <font color=blacko> got all the log, auditing </font>
- simplifies security analysis, resource change tracking, and troubleshooting.
- <font color=OrangeRed> enables governance, compliance, operational auditing, and risk auditing </font> of AWS account.
  - <font color=LightSlateBlue> enabled automatically </font> when create AWS account
  - delivers log files within 15min of account activity.
  - enable CloudTrail for all regions in your environment
    - can create a trail applies to one Region or to all Regions
    - By default, the trail applies to all AWS Regions.
    - provides a complete audit trail of all AWS services within an account
  - CloudTrail can deliver all log files from all regions to one S3 bucket.
    - By default, <font color=OrangeRed> CloudTrail event log files are encrypted using S3 server-side encryption </font>
- <font color=OrangeRed> continuously monitor, tracks user activity and API usage </font> for all regions in AWS
  - provides event history of your AWS account activity
  - including actions taken OR API calls made via:
    - AWS Management Console.
    - AWS SDKs.
    - Command line tools.
    - Higher-level AWS services (such as CloudFormation).


[CloudWatch Logs]() <font color=blacko> collect log, create alarm, does not debug or log errors </font>
- monitor, collect, store, and access logs from resources, applications, and services in <font color=OrangeRed> near real-time </font>
  - <font color=LightSlateBlue> Basic monitoring collects metrics every 5min </font>
  - <font color=LightSlateBlue> detailed monitoring collects metrics every 1min </font>
- <font color=OrangeRed> collect and track metrics, collect and monitor log files, and set alarms.  </font>
  - <font color=LightSlateBlue> Compute </font> (EC2 insatnces, autoscaling groups, elastic load balancers, route53 health checks)
    - <font color=LightSlateBlue> CPU, Disk, Network utilization, and others. </font>
    - <font color=LightSlateBlue> aggregate 聚集 logs from your EC2 instance.  </font>
    - <font color=LightSlateBlue> centrally upload logs from all the servers. </font>
    - <font color=LightSlateBlue> Content Delivery </font> (EBS Volumes, Storage Gateways, CloudFront)
  - <font color=LightSlateBlue> Storage, CloudTrail, Lambda functions, and Amazon SQS queues </font>
  - <font color=LightSlateBlue> allow real-time monitoring as well as adjustable retention. </font>
- providing a unified view of AWS resources, applications and services that run on AWS, and on-premises servers.
- actionable insights to monitor applications, respond to system-wide performance changes, and optimize resource utilization to get a view of your overall operational health.



[AWS Trusted Advisor]() <font color=blacko> what should use </font>
- <font color=OrangeRed> optimize performance and security </font>
- <font color=OrangeRed> real-time guidance </font> to provision 提供 resources guid following AWS <font color=OrangeRed> best practices </font> and staying within limits.
- auto service, during implement ells right and problems.
- provides valuable guidance for architecting your AWS environment and workloads, but doesn't include AWS service health information.
- offers recommendations for <font color=OrangeRed> cost optimization, performance, security, fault tolerance and service limits </font>
- Offers a Service Limits check (in the Performance category)
  - the check displays your usage and limits for some aspects of some services.
  - Business and enterprise can use all checks.










.
