---
title: "Meow's AWS - Cloud Practitioner Exam Practice Q&A"
date: 2026-05-24 11:11:11 -0400
categories: [01Cloud, 01AWS]
tags: [AWS, CloudPractitioner, exam, practice]
math: false
toc: true
image:
---

# AWS Cloud Practitioner - Exam Practice Q&A

---

## Overview

This note collects practice Q&A for the AWS Certified Cloud Practitioner exam. Questions are grouped by topic. Correct answers are highlighted in <font color=OrangeRed>red</font>. Key terms and explanations appear in <font color="blue">blue</font>. Yellow-highlighted questions are marked as exam-critical.

---

## Cloud Concepts and Architecture

**Q: What are the 6 advantages of cloud computing?**

<font color=OrangeRed>
1. Trade Capital Expenses For Variable Expenses
2. Benefit from massive economies of scale
3. Stop guessing about capacity
4. Increase speed and agility
5. Stop spending money running and maintaining data centers
6. Go global in minutes
</font>

---

**Q: What are the three types of cloud computing service models?**

<font color=OrangeRed>
1. Infrastructure As A Service (IaaS) - e.g., EC2
2. Platform As A Service (PaaS) - e.g., Elastic Beanstalk
3. Software As A Service (SaaS) - e.g., Gmail
</font>

---

**Q: What are the three types of cloud computing deployment models?**

<font color=OrangeRed>
1. Public Cloud - AWS, Azure, GCP
2. Hybrid - mix of private and public
3. Private/On-Premises Cloud - managed in own datacenter (OpenStack or VMware)
</font>

---

**Q: Which descriptions are correct regarding cloud deployment models? (choose 2)**

<font color=OrangeRed>With public cloud</font>, the consumer organization typically <font color=OrangeRed>incurs OPEX costs</font> as they do not own the infrastructure and just pay usage costs.

<font color=OrangeRed>With the private cloud</font>, the consumer organization typically <font color=OrangeRed>owns and manages the infrastructure</font>.

---

**Q: What type of cloud is used by traditional on-premises methods?**

<font color=OrangeRed>Private Cloud</font>

---

**Q: VMware Cloud on AWS allows companies to migrate and extend their on-premises VMware vSphere-based environments to AWS Cloud using Amazon EC2. Which of the following choices accurately classifies this deployment model?**

<font color=OrangeRed>Hybrid</font>

---

**Q: Which cloud computing model gives the IT department the highest level of flexibility and management control?**

<font color=OrangeRed>IaaS</font>

<font color="blue">On-premises cloud is a cloud deployment model, not a cloud computing model. Other cloud deployment models are Private, Public and Hybrid.</font>

---

**Q: Which of the following is an example of a SaaS?**

<font color=OrangeRed>All of the infrastructure, operating system and software are provided by a third party.</font>

---

**Q: What type of cloud computing service type do AWS Elastic Beanstalk and Amazon RDS correspond to?**

<font color=OrangeRed>PaaS</font>

---

**Q: What is fault-tolerance?**

<font color=OrangeRed>The ability to maintain operations during and/or after failure.</font>

---

**Q: How does Elasticity differ from Scalability?**

<font color=OrangeRed>Elasticity differs in its ability to not only scale-out but to shrink back down resources based on demand as well.</font>

---

**Q: The ability to horizontally scale Amazon EC2 instances based on demand is an example of which concept?**

<font color=OrangeRed>Elasticity</font>

---

**Q: Which of the following was NOT a business challenge before the cloud?**

- Cost Control of an on-premises datacenter.
- Slow Provisioning of on-premises data centers.
- Differing security protocols for a distributed workforce.
- <font color=OrangeRed>Fully-customizable infrastructure with on-premises data centers</font> (This is NOT a challenge - it is a benefit of on-premises)

---

**Q: How can an application achieve high availability and fault-tolerance?**

<font color=OrangeRed>Utilizing multiple Availability Zones</font>

---

**Q: Which of these is an example of the hierarchy in the AWS global infrastructure from largest to smallest?**

<font color=OrangeRed>AWS Global Infrastructure, AWS Regions, Availability Zones, and Data Centers</font>

---

**Q: Which of these is descriptive of an Availability Zone?**

<font color=OrangeRed>An Availability Zone is an area containing datacenters in which AWS resources are available.</font>

<font color="blue">An Availability Zone is one or more discrete data centers housed in separate facilities, each with redundant power, networking, and connectivity.</font>

---

**Q: What is a region?**

<font color=OrangeRed>A physical location in the world that has two or more availability zones.</font>

---

**Q: What things go into choosing the right AWS Region?**

1. Data Sovereignty Laws - do you have to have your data in a certain area by law
2. Latency to end users - where are your users; put resources where they can quickly access them
3. AWS Services - some regions get certain services before others

---

**Q: Which of the following are components of the AWS Global Infrastructure? One or more discrete data centers interconnected through low latency links?**

<font color=OrangeRed>Availability Zone</font>

---

**Q: Which statements about the AWS global infrastructure are true regarding data stored within an AWS Region?**

### <font color=OrangeRed>Data stored within an AWS region is not replicated outside of that region automatically.</font>

It is up to customers of AWS to determine whether they want to replicate their data to other regions. Compliance and network latency must always be considered.

---

**Q: What should users do if they want to install an application in geographically isolated locations?**

<font color=OrangeRed>Deploy the app to multiple AWS Regions</font>

---

**Q: A solution that is able to support growth in users, traffic, or data size with no drop in performance aligns with which cloud architecture principle?**

<font color=OrangeRed>Elasticity</font>

---

**Q: Which of the following is an AWS Cloud architecture design principle?**

<font color=OrangeRed>Implement loose coupling</font>

---

**Q: A company's web application currently has tight dependencies on underlying components, so when one component fails the entire web application fails. Applying which AWS Cloud design principle will address this?**

<font color=OrangeRed>Focus on decoupling components by isolating them and ensuring individual components can function when other components fail.</font>

---

**Q: What is a benefit of loose coupling as a principle of cloud architecture design?**

<font color=OrangeRed>Prevents cascading failures between different components</font>

---

**Q: When architecting cloud applications, which is a key design principle?**

<font color=OrangeRed>Implement elasticity</font>

---

**Q: Which architectural best practice aims to reduce the interdependencies between services?**

<font color=OrangeRed>Break into smaller, loosely coupled components</font> — reduce interdependencies in a system by enabling interaction only through specific, technology-agnostic interfaces (e.g., RESTful APIs).

---

**Q: What are two best practices for designing your cloud environment?**

<font color=OrangeRed>Assume and practice failures.</font>

<font color=OrangeRed>Build loosely coupled components</font> (so if one fails, it does not all fail.)

---

**Q: Which is a recommended pattern for designing a highly available architecture on AWS?**

<font color=OrangeRed>Ensure that the application is designed to accommodate failure of any single component.</font>

---

**Q: A new service using AWS must be highly available. Yet, due to regulatory requirements, all of its Amazon EC2 instances must be located in a single geographic area. According to best practices, to meet these requirements, the EC2 instances must be placed in at least two:**

<font color=OrangeRed>Availability Zones</font>
<font color=OrangeRed>Subnets</font>

<font color="blue">Each Availability Zone is associated with a subnet. So 2 Availability Zones = 2 Subnets.</font>

---

**Q: Which of the following features can be configured through the Amazon Virtual Private Cloud (Amazon VPC) Dashboard?**

<font color=OrangeRed>Subnet</font>

---

**Q: What is an example of agility in the AWS Cloud?**

<font color=OrangeRed>Decreased acquisition time for new compute resources.</font>

---

**Q: How does AWS shorten the time to provision IT resources?**

<font color=OrangeRed>Provide the ability to programmatically provision existing resources</font>

---

**Q: How can the AWS Cloud increase user workforce productivity after migration from an on-premises data center?**

<font color=OrangeRed>Users do not have to wait for infrastructure provisioning</font>

---

**Q: What approach to transcoding a large number of individual video files adheres to AWS architecture principles?**

<font color=OrangeRed>Use many instances in parallel</font>

---

**Q: Which of the following deployment models enables customers to fully trade their capital IT expenses for operational expenses?**

<font color=OrangeRed>Cloud</font>

---

**Q: How can a company reduce its Total Cost of Ownership (TCO) using AWS?**

<font color=OrangeRed>By minimizing large capital expenditures</font>

---

**Q: Traditional vs. Cloud Computing - key differences?**

1. IT Assets as Provisioned Resources
2. Global, Available, and Scalable Capacity
3. Higher Level Managed Services
4. Built-In Security
5. Architecting For Cost
6. Operating on AWS

---

## IAM (Identity and Access Management)

**Q: What does IAM stand for? When you create a user or group, is it created regionally or globally?**

<font color=OrangeRed>Identity Access Management; Globally</font>

---

**Q: Which of the following can IAM be used to manage?**

<font color=OrangeRed>Users, MFA, Roles, Groups</font>

---

### <font color=OrangeRed>IAM Key Concepts</font>

**Q: What access privileges does a new IAM user have by default?**

<font color=OrangeRed>AWS Console login access</font>

**Q: Any new IAM Users created are granted \_.**

<font color=OrangeRed>No access to AWS services.</font>

---

**Q: Which AWS managed policy could be attached to an IAM User to grant all access permissions?**

<font color=OrangeRed>AdministratorAccess</font>

---

**Q: Which of the following will grant permissions when directly attached to an IAM User?**

<font color=OrangeRed>IAM Policy</font>

---

**Q: Three developers need access to S3. What is the most appropriate and efficient way to give all developers (IAM users) access to S3?**

<font color=OrangeRed>Add the developers to an IAM Group and attach an IAM policy to that group.</font>

---

**Q: In this scenario, we have an IAM User with an AWS DenyAll policy, but this user is also in an IAM Group with access to various AWS services including S3, EC2, VPC, and IAM. Which resources can this user access?**

<font color=OrangeRed>The IAM user cannot access any of the AWS services.</font>

<font color="blue">An explicit deny always overrides an explicit allow.</font>

---

**Q: Which IAM entity can be used for assigning permissions to AWS services?**

<font color=OrangeRed>IAM role</font>

---

**Q: Which of the following IAM options allows an application to write data to S3 for backups?**

> Role

---

**Q: What is an AWS Identity and Access Management (IAM) role?**

<font color=OrangeRed>An entity that defines a set of permissions for use with an AWS resource</font>

---

**Q: Are roles regional or universal?**

<font color=OrangeRed>Universal</font> - they can be used in any place around the world.

---

**Q: Roles are a better alternative to...**

<font color=OrangeRed>Using Access Key IDs and secret access keys</font>

---

**Q: What is a root account? What access does it have? How do you secure the root account?**

<font color=OrangeRed>The email address you used to set up your AWS account; it has full administrator access; you should secure it with multi-factor authentication.</font>

---

**Q: What does MFA stand for?**

<font color=OrangeRed>Multi-Factor Authentication</font>

---

**Q: Which of the following is NOT a method of getting or using MFA codes?**

- Virtual MFA Device
- Hardware key fob
- <font color="blue">API keys</font> (not an MFA method)
- <font color=OrangeRed>Single sign-on</font> (not an MFA method)

---

**Q: What are the ways you can interact with AWS?**

1. Console
2. Command Line Interface (CLI)
3. Software Development Kits (SDKs)

---

**Q: Which AWS IAM feature allows developers to access AWS services through the AWS CLI?**

<font color=OrangeRed>Access keys</font>

---

**Q: To use the AWS CLI, users are required to generate:**

<font color=OrangeRed>An access/secret key</font>

---

**Q: Access keys in AWS Identity and Access Management (IAM) are used to:**

<font color=OrangeRed>Make programmatic calls to AWS from AWS APIs</font>

---

**Q: Which of the following can limit Amazon S3 bucket access to specific users?**

<font color=OrangeRed>IAM policy</font>

---

**Q: Which actions represent best practices for using AWS IAM? (Choose two.)**

<font color=OrangeRed>Configure a strong password policy</font>
<font color=OrangeRed>Rotate access keys on a regular basis</font>

---

**Q: You are using your corporate directory to grant your users access to AWS services. What is this called?**

<font color=OrangeRed>Federated Access</font>

<font color="blue">When you use an external directory, such as a corporate one, to grant users in that directory access to AWS resources.</font>

---

**Q: Which of the following can a customer use to enable single sign-on (SSO) to the AWS Console?**

<font color=OrangeRed>AWS Directory Service</font>

---

**Q: What do group policies consist of?**

<font color="blue">Policies consist of JavaScript Object Notation (JSON). You also have a key value pair, e.g., "name": "AcloudGuru"</font>

---

**Q: How do you set permissions in a group?**

<font color=OrangeRed>Apply policies to the group</font>

---

**Q: Which of the following are AWS Security, Identity, and Compliance services?**

<font color=OrangeRed>KMS</font> - makes it easy to create and manage cryptographic keys.
<font color=OrangeRed>Secrets Manager</font> - protects the secrets you use for access to applications and services.
<font color=OrangeRed>Security Hub</font> - consolidates your view of security and compliance status in the cloud.

---

## EC2 (Elastic Compute Cloud)

**Q: What is Amazon EC2?**

<font color=OrangeRed>Amazon Elastic Compute Cloud; a web service that provides resizable compute capacity in the cloud. It reduces the time required to obtain and boot new server instances to minutes, allowing you to quickly scale capacity, both up and down, as your computing requirements change.</font>

---

**Q: What benefits does Amazon EC2 provide over using non-cloud servers? (choose 2)**

1. **Elastic Web-Scale computing** - increase or decrease capacity within minutes not hours and commission one to thousands of instances simultaneously.
2. **Inexpensive** - Amazon passes on the financial benefits of scale by charging very low rates and on a capacity consumed basis.

AWS provides an SLA for EC2 of at least 99.99%.

---

**Q: Which AWS service provides elastic web-scale cloud computing allowing you to deploy operating system instances?**

<font color=OrangeRed>EC2</font>

---

**Q: Which of the following are the four types of EC2 instances?**

1. On Demand
2. Reserved
3. Spot
4. Dedicated Hosts

---

**Q: What is an On Demand EC2?**

<font color=OrangeRed>Allows you to pay a fixed rate by the hour (or by the second) with no commitment.</font>

---

**Q: What is a Reserved EC2?**

<font color=OrangeRed>Provides you with a capacity reservation and offers a significant discount on the hourly charge for an instance. Contract Terms are 1 year or 3 years.</font>

---

**Q: What is a Spot EC2?**

<font color=OrangeRed>Enables you to bid whatever price you want for instance capacity, providing for even greater savings if your applications have flexible start and end times.</font>

---

**Q: What is a Dedicated Host EC2?**

<font color=OrangeRed>Physical EC2 server dedicated for your use. Dedicated Hosts can help you reduce costs by allowing you to use your existing server-bound software licenses.</font>

---

### <font color=OrangeRed>EC2 Pricing Models</font>

**Q: Which Amazon EC2 billing option gives you low cost, maximum flexibility, no upfront costs or commitment, and you only pay for what you use?**

<font color=OrangeRed>On-Demand instances</font>

With On-Demand instances you pay for hours used with no commitment. There are no upfront costs so you have maximum flexibility.

INCORRECT: "Spot Instances" is incorrect. Spot instances are used for getting a very low price which you bid on. You lose some flexibility as you are constrained by market prices and your workloads can be terminated if the market price exceeds your bid price.

---

**Q: What is the main benefit of why someone might choose an On-Demand EC2 instance?**

<font color=OrangeRed>Create, start, stop at any time. Charged on second or hour rate, no termination fee.</font>

---

**Q: Which Amazon EC2 instance pricing model can provide discounts of up to 90%?**

<font color=OrangeRed>Spot instances</font>

---

**Q: Which Amazon EC2 pricing model adjusts based on supply and demand of EC2 instances?**

<font color=OrangeRed>Spot instances</font>

---

**Q: Which Amazon EC2 pricing model is the MOST cost-efficient for an uninterruptible workload that runs once a year for 24 hours?**

<font color=OrangeRed>On-demand instances</font>

---

**Q: You need to run a production process that will use several EC2 instances and run constantly on an ongoing basis. The process cannot be interrupted or restarted without issue. What EC2 pricing model would be best for this workload?**

<font color=OrangeRed>Reserved Instances (RIs)</font>

---

**Q: What are the benefits of using reserved instances? (choose 2)**

With reserved instances you commit to a 1- or 3-year term and get a significant discount from the on-demand rate. You can also reserve capacity in an availability zone with reserved instances.

CORRECT: <font color=OrangeRed>"Reduced cost"</font> is a correct answer.
CORRECT: <font color=OrangeRed>"Reserve capacity"</font> is also a correct answer.

---

**Q: Which Amazon EC2 Reserved Instance type enables you to match your capacity reservation to predictable recurring dates and times?**

<font color=OrangeRed>Scheduled RI</font>

---

**Q: You have a new requirement for your application that needs a set of servers for a short period of time of up to four months. While the instances are needed for a short period, the instances must be always available for the full duration. What instance type would be the best choice?**

A. Reserved instances (at least a year) - INCORRECT
B. Partial up front reserved instances - INCORRECT
C. <font color=OrangeRed>On-demand instances</font> - CORRECT
D. Spot instances - INCORRECT

---

**Q: Which of the Reserved Instance (RI) pricing models provides the highest average savings compared to On-Demand pricing?**

<font color=OrangeRed>3 year, all upfront, standard RI pricing</font>

---

**Q: Which of the Reserved Instance (RI) pricing models can change the attributes of the RI as long as the exchange results in the creation of RIs of equal or greater value?**

<font color=OrangeRed>Convertible RIs</font>

---

**Q: Medium Corp is planning to purchase Reserved Instances. Which option is the MOST expensive?**

<font color=OrangeRed>Reservation for 1 year with no upfront</font>

---

**Q: Andrew is a software developer and wants to run few instances for a batch processing job for duration of three days. The job metadata is stored in S3 and if the job gets interrupted, it can be started again without any impact. Considering cost is a major factor, which instance pricing model should he choose?**

<font color=OrangeRed>Spot instance</font>

---

**Q: Which Amazon EC2 pricing model automatically adjusts charges as your usage changes?**

<font color=OrangeRed>Savings Plans</font> is the only Amazon EC2 pricing model that provides the flexibility of adjusting charges depending on the amount of usage, thereby saving money in the process.

---

**Q: You have EC2 instances running at 90% utilization and you expect this to continue for at least a year. What type of EC2 instance would you choose to ensure your costs stay at a minimum and avoid interruption?**

> Reserved instances

---

**Q: In this scenario, we have an increase in traffic on a holiday sale. What EC2 purchasing option should we use to acquire the resources to handle the traffic?**

<font color=OrangeRed>On-Demand</font>

---

**Q: You have a dedicated web server and database that remains largely idle but sometimes has huge spikes in activity. What can you architect to improve your cost-efficiency?**

> Configure serverless architecture leveraging Lambda.

---

**Q: Which of the following is not an available EC2 Instance Type?**

- General Purpose
- Memory Optimized
- Compute Optimized
- Accelerated Computing
- Storage Optimized
- <font color=OrangeRed>Database Optimized</font> (this is NOT a valid EC2 instance type)

---

**Q: Which of the following types of EC2 instances is ideal for workloads that process large data sets in memory?**

<font color=OrangeRed>Memory Optimized</font>

---

**Q: Which service allows an organization to bring their own licensing on host hardware that is physically isolated from other AWS accounts?**

CORRECT: <font color=OrangeRed>"EC2 Dedicated Hosts"</font> is the correct answer.

INCORRECT: "EC2 Dedicated **Instances**" is incorrect.

---

**Q: Where can resources be launched when configuring EC2 Auto Scaling?**

Amazon EC2 Auto Scaling is configured within the EC2 console and can launch instances within a VPC across multiple AZs. It cannot launch resources into another AWS Region.

CORRECT: <font color=OrangeRed>"Multiple AZs within a region"</font> is the correct answer.

---

**Q: An Auto Scaling Group is a \_.**

<font color=OrangeRed>Logical grouping of EC2 instances for the purpose of scaling</font>

---

**Q: In this scenario, we have an ELB balancing traffic between two instances, but the instances are reaching capacity. What could we do to automate a solution for handling the traffic?**

> Create an Auto Scaling Group

---

**Q: Which of these important Cloud concepts will an ELB improve?**

<font color=OrangeRed>Fault Tolerance</font>
<font color=OrangeRed>High Availability</font>

---

**Q: Which AWS service can be used to manually launch instances based on resource requirements?**

<font color=OrangeRed>EC2</font>

---

**Q: Which AWS service can be used to automatically scale an application up and down without making capacity planning decisions?**

<font color=OrangeRed>Auto Scaling</font>

---

**Q: John is running a web application and seeing very changing traffic workloads - few hours a day traffic is very high however for rest of the day traffic is less. Which AWS feature can john utilize to add and remove server capacity based on traffic workload?**

<font color=OrangeRed>Auto-scaling</font>

---

**Q: Which of the following services will automatically scale with an expected increase in web traffic?**

<font color=OrangeRed>ELB (Elastic Load Balancing)</font>

---

**Q: By default, a root EBS volume is set to be \_ when an instance is \_.**

<font color=OrangeRed>deleted, terminated</font>

---

**Q: By default, Security Groups \_\_.**

<font color=OrangeRed>allow all outbound traffic and deny all inbound traffic</font>

---

**Q: Which of these types of operating systems will we see in AWS?**

<font color=OrangeRed>Windows</font>
<font color=OrangeRed>Linux</font>

---

**Q: What should the permissions of a key pair (.pem file) be before connecting to an EC2 instance?**

<font color=OrangeRed>400</font>

---

**Q: What does AMI stand for?**

<font color=OrangeRed>Amazon Machine Image</font>

---

**Q: Community AMIs are \_.**

<font color=OrangeRed>free to use</font>

---

**Q: A Security Group is used to \_ traffic on the \_.**

<font color=OrangeRed>explicitly allow, instance level</font>

---

**Q: Which of these components does a security group represent for an EC2 instance?**

<font color=OrangeRed>Firewall</font>

---

**Q: A security group is a \_ on the \_ level.**

<font color=OrangeRed>Firewall, instance</font>

---

**Q: What acts as a virtual firewall that controls traffic to your EC2 instances?**

<font color=OrangeRed>Security group</font>

**Bold:** "AWS WAF" is incorrect - WAF protects your web applications. AWS security groups (SGs) are associated with EC2 instances and provide security at the protocol and port access level.

---

**Q: Which tools can best assist with identifying common security vulnerabilities within your EC2 Instances?**

- AWS Config (configuration)
- AWS Trusted Advisor
- <font color=OrangeRed>AWS Inspector</font>
- ~~AWS Guard Duty~~ (Guard Duty is a threat detection service)

<font color=OrangeRed>AWS Inspector</font> can check your EC2 instances for common security vulnerabilities.

---

**Q: What type of placement group should you use to spread Amazon EC2 instances across logical partitions so that they don't share the same underlying hardware?**

<font color=OrangeRed>Partition</font>

<font color="blue">With a partition placement group, EC2 instances are placed into logical segments called partitions, each of which has its own set of racks to supply its network and power source. This level of isolation is designed to prevent the impact of hardware failure within your application.</font>

---

**Q: Which of the following are advantages of using Amazon Machine Images (AMIs) backed by Amazon Elastic Block Storage (EBS), rather than by EC2 instance storage?**

<font color=OrangeRed>Unlike EC2 instance store, EBS uses persistent storage</font>
<font color=OrangeRed>EBS launches faster than EC2 instance storage</font>

---

**Q: Which type of AWS storage is ephemeral and is deleted when an instance is stopped or terminated?**

<font color=OrangeRed>EC2 instance store</font>

---

**Q: Your company needs to host a database in their AWS environment but needs to have control over patching. Which is the best choice?**

> EC2 instance

---

**Q: What is AWS Lightsail?**

<font color=OrangeRed>One of AWS's VPS Services</font>

---

**Q: Which service can you use to provision a preconfigured server with little to no AWS experience?**

<font color=OrangeRed>Amazon LightSail</font>

---

## VPC, Networking, and Load Balancers

**Q: What does VPC stand for?**

<font color=OrangeRed>Virtual Private Cloud</font>

---

**Q: What is a VPC?**

<font color=OrangeRed>A logically isolated section of the AWS Cloud</font>

Amazon Virtual Private Cloud (Amazon VPC) lets you provision a logically isolated section of the AWS cloud where you can launch AWS resources in a virtual network you define. You have complete control over your virtual networking environment, including selection of your own IP address range, creation of subnets, and configuration of route tables and network gateways.

---

**Q: What is the scope of a VPC within a region?**

<font color=OrangeRed>An Amazon Virtual Private Cloud (VPC) spans all availability zones within a region.</font>

---

**Q: How many VPCs are created by default in a region?**

<font color=OrangeRed>1</font>

---

**Q: How many VPCs can an EC2 instance be attached to at a time?**

<font color=OrangeRed>1</font>

---

**Q: How many Internet Gateways can an EC2 instance be attached to at a time?**

> 1

---

**Q: VPCs span all of these except for \_.**

<font color=OrangeRed>AWS Regions</font>

---

**Q: Which choice below allows you to carve out a portion of the AWS Cloud?**

<font color=OrangeRed>VPC</font>

> Subnet (creates subsections of the VPC)

---

**Q: What is a NACL?**

<font color=OrangeRed>A firewall on the subnet level</font>

<font color="#ad8456">A stateless firewall for inbound/outbound traffic (NACL)</font>

---

**Q: Which of the following is true about public subnets and private subnets?**

<font color=OrangeRed>A public subnet has a route table pointing to an Internet Gateway</font>
<font color=OrangeRed>A private subnet does not have a route table pointed to an Internet Gateway</font>

---

**Q: A subnet is a \_.**

<font color=OrangeRed>Subsection of a network</font>

---

**Q: Which of these statements is true of subnets?**

<font color=OrangeRed>The default VPC already has subnets created for each AZ by default.</font>
**Subnets cannot span AZs.**
<font color=OrangeRed>We can add one or more subnets in each AZ.</font>

---

**Q: How many subnets are created by default in each region when an AWS account is created?**

<font color=OrangeRed>1 subnet per Availability Zone</font>

---

**Q: Which of the following will create subsections of a VPC?**

<font color=OrangeRed>Subnet</font>

---

**Q: What does a route table do?**

<font color=OrangeRed>Directs traffic within a network</font>

---

**Q: Which of the following is descriptive of an Internet Gateway?**

<font color=OrangeRed>A route to and from the internet</font>

---

**Q: In this scenario, we have a NACL with the following rules:**

| Rules | Traffic |
|-------|---------|
| Rule#1 | Allow SSH |
| Rule#2 | Allow HTTP |
| Rule#3 | Deny All |
| Rule#4 | Allow All |

**Which is true based on the rules within this NACL?**

<font color=OrangeRed>All traffic except SSH and HTTP will be denied</font>

---

**Q: Which feature allows you to associate security features with a subnet inside your VPC to protect your environment from incoming traffic requests?**

<font color=OrangeRed>NACLs</font>

---

**Q: Which items can be configured from within the VPC management console? (choose 2)**

<font color=OrangeRed>Subnets</font> and <font color=OrangeRed>Security groups</font> can be configured from within the VPC console.

**"Regions" is incorrect.**

---

**Q: Which AWS network element allows you to assign a static IPv4 address to an EC2 instance?**

<font color=OrangeRed>Elastic IP</font>

---

**Q: What are two ways of connecting to an Amazon VPC from an on-premises data center? (choose 2)**

You can connect from your on-premises data center to a VPC via <font color=OrangeRed>Direct Connect</font> or <font color=OrangeRed>VPN CloudHub.</font>

- AWS Direct Connect is a network service that provides an alternative to using the Internet to connect a customer's on-premises sites to AWS.
- If you have multiple VPN connections, you can provide secure communication between sites using the AWS VPN CloudHub.

---

**Q: What can you use to quickly connect your office securely to your Amazon VPC?**

<font color=OrangeRed>AWS managed VPN</font>

---

**Q: Which AWS services can be used to connect the AWS Cloud and on-premises resources? (Select TWO.)**

<font color=OrangeRed>AWS Managed VPN</font> - a virtual private network connection over the public Internet. This creates an encrypted link between the on-premises network and your AWS VPC.

<font color=OrangeRed>AWS Direct Connection</font> - connects on-premises networks to AWS using private network links.

---

**Q: Which AWS service allows companies to connect an Amazon VPC to an on-premises data center?**

<font color=OrangeRed>Amazon Direct Connect</font>

---

**Q: Which services below provide a connection from your on-premises environment infrastructure and resources to your resources hosted in AWS?**

- AWS VPC
- VPC peering (peers two VPCs together, not on-premises)
- <font color=OrangeRed>AWS Direct Connect</font>
- > AWS Virtual Private Network

---

**Q: Which service would provide network connectivity in a hybrid architecture that includes the AWS Cloud?**

<font color=OrangeRed>AWS Direct Connect</font>

---

**Q: What are the types of load balancers?**

<font color=OrangeRed>Application Load Balancers, Network Load Balancers, Classic Load Balancers</font>

---

**Q: What is an Application Load Balancer?**

<font color=OrangeRed>Load balancer that is application aware - can see layer 7 (i.e., code) and make intelligent decisions.</font>

---

**Q: What is a Network Load Balancer?**

<font color=OrangeRed>Load balancer that is used when you need extreme performance and have a static IP address.</font>

---

**Q: What is a Classic Load Balancer?**

<font color=OrangeRed>Load balancer that should be used for test and development. Keeps cost low (being phased out).</font>

---

**Q: Have an application composed of individual services and you need to route a request to a service based on the content of the request. What type of load balancer should you use?**

<font color=OrangeRed>Application load balancer</font>

---

**Q: Which service is used to introduce fault tolerance into an application architecture?**

<font color=OrangeRed>ELB (fault tolerance)</font>

Amazon CloudFront (cache)

---

**Q: Which AWS services should be used for read/write of constantly changing data?**

<font color=OrangeRed>RDS</font> or <font color=OrangeRed>AWS EFS</font>

---

**Q: Which AWS service allows you to connect to storage from on-premises servers using standard file protocols?**

<font color=OrangeRed>Amazon EFS</font>

<font color="blue">EFS is a fully-managed service that makes it easy to set up and scale file storage in the Amazon Cloud. EFS filesystems are mounted using the NFS protocol. Access to EFS file systems from on-premises servers can be enabled via Direct Connect or AWS VPN.</font>

---

**Q: A company is planning to launch an ecommerce site in a single AWS Region to a worldwide user base. Which AWS services will allow the company to reach users and provide low latency and high transfer speeds? (Choose two.)**

<font color=OrangeRed>AWS Global Accelerator</font>
<font color=OrangeRed>Amazon CloudFront</font>

---

**Q: A cloud practitioner needs to decrease application latency and increase performance for globally distributed users. Which services can assist? (Select TWO.)**

<font color=OrangeRed>Amazon S3 and CloudFront</font>

<font color="blue">ElastiCache caches data from a database in-memory. AppStream 2.0 is an application streaming service for streaming applications to computers.</font>

---

**Q: Company wants to use an AWS service to monitor the health of application endpoints, with the ability to route traffic to healthy regional endpoints to improve application availability. Which service will support these requirements?**

<font color=OrangeRed>AWS Global Accelerator</font>

---

**Q: Which services can be used across hybrid AWS Cloud architectures?**

<font color=OrangeRed>Route 53</font>

"Virtual Private Gateway" can also be used for such architectures.

---

**Q: Which service provides a hybrid storage service that enables on-premises applications to seamlessly use cloud storage?**

<font color=OrangeRed>AWS Storage Gateway</font>

---

**Q: Which AWS hybrid storage service enables on-premises applications to seamlessly use AWS Cloud storage through standard file-storage protocols?**

<font color=OrangeRed>AWS Storage Gateway</font>

---

**Q: What is the purpose of the AWS Storage Gateway?**

<font color=OrangeRed>Connect on-premises data storage to the AWS Cloud</font>

---

**Q: A company is considering using AWS for a self-hosted database that requires a nightly shutdown for maintenance and cost-saving purposes. Which service should the company use?**

<font color=OrangeRed>EC2 with EBS</font>

---

## S3 and Storage

**Q: What is S3?**

<font color=OrangeRed>Storage Service</font>

S3 is:
1. Object-Based (allows you to upload files)
2. Storage is unlimited
3. Files are stored in <font color=OrangeRed>buckets</font>
4. S3 is a universal namespace so names must be unique globally

---

**Q: What S3 term is used in place of "file"?**

<font color=OrangeRed>Object</font>

---

**Q: What is the root level folder you create in S3 called?**

<font color=OrangeRed>Bucket</font>

---

**Q: Amazon S3 bucket names must be unique across \_.**

<font color=OrangeRed>AWS</font>

Amazon S3 bucket names must be unique across AWS.

---

**Q: S3 is an example of \_.**

- Elastic Block Store (INCORRECT)
- Storage array (INCORRECT)
- Block storage (INCORRECT)
- <font color=OrangeRed>Bulk storage</font>

---

**Q: Which of the following are examples of cloud bulk storage?**

<font color=OrangeRed>Google Drive, Amazon S3, Dropbox</font>

---

**Q: Which of the following is an example of block storage?**

<font color=OrangeRed>Amazon EBS</font>

~~AWS Storage Gateway~~ (incorrect - Storage Gateway is hybrid storage)

---

**Q: What type of websites can be hosted on S3? What type of websites CANNOT be hosted on S3?**

<font color=OrangeRed>S3 can host static websites (HTML); S3 CANNOT host websites that require database connections (e.g., WordPress).</font>

---

**Q: Which storage service can be used as a low-cost option for hosting static websites?**

<font color=OrangeRed>S3</font>

---

**Q: What is the lowest-cost, durable storage option for retaining database backups for immediate retrieval?**

<font color=OrangeRed>S3</font>

---

**Q: Which statements are correct regarding Amazon S3 buckets? (choose 2)**

<font color=OrangeRed>Bucket names must be unique globally</font>

<font color=OrangeRed>Buckets are region-specific</font> and the data never leaves that region unless explicitly configured to do so through <font color="blue">cross-region replication (CRR).</font>

---

**Q: Do you view buckets globally or regionally? Can you have buckets in individual regions?**

<font color=OrangeRed>Globally</font>; yes, you can have buckets in individual regions.

---

**Q: What does cross region replication do?**

<font color=OrangeRed>Allows you to replicate the contents of one bucket to another bucket automatically</font>

---

**Q: What is a characteristic of Amazon S3 cross-region replication?**

<font color=OrangeRed>S3 buckets configured can be owned by a single AWS account or different accounts</font>

---

**Q: What is the availability and durability of S3 Standard Storage Class?**

<font color=OrangeRed>11 nines (9x11) durability and 99.99% availability.</font>

---

**Q: What is S3 Standard?**

<font color=OrangeRed>Almost 100% availability and durability, stored redundantly across multiple devices.</font>

---

**Q: What are the 6 types of S3?**

1. S3 Standard
2. S3 - IA (Infrequently Accessed)
3. S3 One Zone-IA
4. S3 - Intelligent Tiering
5. S3 Glacier
6. S3 Glacier Deep Archive

---

**Q: What S3 storage class is the most expensive?**

<font color=OrangeRed>Standard</font>

---

**Q: What is S3-IA?**

<font color=OrangeRed>(Infrequently Accessed) - for data that is accessed less frequently, but requires rapid access when needed. Lower fee than S3, but charged a retrieval fee.</font>

---

**Q: What is S3 One Zone-IA?**

<font color=OrangeRed>When you want a low cost option for infrequently accessed data and don't require the multiple AZ data resilience.</font>

---

**Q: What is S3 - Intelligent Tiering?**

<font color=OrangeRed>Built to optimize costs by automatically moving data to the most cost-effective access tier, without performance impact or operational overhead.</font>

---

**Q: What is S3 Glacier?**

<font color=OrangeRed>A secure, durable, and low-cost storage class for data archiving. Retrieval times can range from minutes to hours.</font>

---

**Q: What is S3 Glacier Deep Archive?**

<font color=OrangeRed>Amazon S3's lowest-cost storage class where retrieval time of 12 hours is acceptable.</font>

---

**Q: A hospital organization wants to store patient health information as cheap as possible for archive purposes and is not worried about retrieval periods. What would be the most appropriate storage class?**

<font color=OrangeRed>Glacier Deep Archive</font>

---

**Q: Upon sign-up of an AWS account, how much Amazon S3 Standard storage will you get for no cost?**

<font color=OrangeRed>5 GB</font>

---

**Q: Which of the following are key components of Amazon Glacier?**

Data is organized in S3 into <font color=OrangeRed>Archives</font>, and <font color=OrangeRed>Vaults</font> are used to group Archives together. <font color=OrangeRed>Access policies</font> control who can access the data in Archives and Vaults.

**Buckets** are a part of S3, but not Glacier. **Volumes** are often associated with hard disks and therefore EBS. **Tables** are database constructs.

---

**Q: You have been asked to archive some data into Glacier that needs to be encrypted. What is the easiest way to achieve this?**

<font color=OrangeRed>Send the data to Glacier and do nothing more - all data in Glacier is encrypted by default.</font>

Data stored in Glacier is encrypted by default so nothing else needs to be done.

---

**Q: Which AWS Glacier data access option retrieves data from an archive in 1-5 minutes?**

<font color=OrangeRed>Expedited</font>

**Expedited retrievals** allow you to quickly access your data when occasional urgent requests for a subset of archives are required. For all but the largest archives (250 MB+), data accessed using Expedited retrievals are typically made available within 1-5 minutes.

---

**Q: What is S3 transfer acceleration?**

<font color=OrangeRed>Instead of uploading to S3 you upload to an edge location (goes on Amazon's internal network and then it's uploaded to the bucket - makes things faster).</font>

---

**Q: What is the AWS storage gateway?**

<font color=OrangeRed>Hybrid Storage Service</font>

---

**Q: What are the names of two types of AWS Storage Gateway? (choose 2)**

- <font color="blue">File Gateway:</font> data is uploaded to S3 for use with object based workloads.
- <font color=OrangeRed>Volume Gateway.</font>
  - <font color="blue">stored volumes:</font> keep the customer data on the customer premises location.
  - <font color="blue">cached volumes:</font> store data in AWS Cloud
- <font color="blue">Virtual Tape Library Gateway:</font> for long term, off-site data archiving. A virtual tape library (VTL) interfaces with the customer's backup software.

---

**Q: Which of these will allow an organization to cache their environment locally and store the data within the AWS cloud?**

<font color=OrangeRed>Cached volumes</font>

---

**Q: Which type of storage stores objects comprised of key, value pairs?**

<font color=OrangeRed>Amazon S3</font>

DynamoDB (not objects, but items)

---

**Q: For cost optimization in AWS, what are two options you must consider for S3?**

> Whether you need to use encryption (Encryption is not an added expense)
> The number of S3 buckets you need. (not an added expense.)
<font color=OrangeRed>The total size in gigabytes of all objects being stored</font>
> Storage class being used or picked to store objects

---

**Q: S3 Pricing Reference:**

- S3 Standard Storage: First 50 TB $0.023/GB, Next 450 TB $0.022/GB, Over 500 TB $0.021/GB
- S3-IA: $0.0125/GB
- S3 One Zone-IA: $0.01/GB
- S3 Glacier: $0.004/GB
- S3 Glacier Deep Archive: $0.00099/GB

---

**Q: An EBS volume is a \_.**

<font color=OrangeRed>highly available and reliable storage volume</font>
<font color=OrangeRed>storage volume that can be attached to any instance in the same AZ (Availability Zone)</font>

---

**Q: Which of the following AWS services uses EBS as a detachable storage?**

<font color=OrangeRed>Amazon EC2</font>

---

**Q: Which of the following is a benefit of using the AWS Cloud? What is the lowest-cost, durable storage option?**

<font color=OrangeRed>S3</font>

---

**Q: How do you know an S3 upload has been successful?**

<font color=OrangeRed>You get an HTTP 200 status code</font>

---

**Q: How can you make entire S3 buckets public?**

<font color=OrangeRed>Use bucket policies</font>

---

**Q: How does S3 scale?**

<font color=OrangeRed>S3 scales automatically to meet your demand.</font> Good for when static websites are going to have a large number of requests coming in.

---

**Q: Read after write consistency is for...**

<font color=OrangeRed>PUTS of new Objects</font>

---

**Q: Eventual Consistency is for...**

<font color=OrangeRed>overwrite PUTS and DELETES (can take some time to propagate)</font>

---

**Q: What are the Key Fundamentals for S3?**

- Key (the name of the object)
- Value (the data, made up of a sequence of bytes)

---

**Q: You are building an online cloud storage platform. Users will be uploading their files for backup to your applications. You are unsure about the capacity requirements. Which AWS service can help you here?**

<font color=OrangeRed>S3</font>

---

## Databases

**Q: What are the types of databases?**

<font color=OrangeRed>RDS</font> and <font color=OrangeRed>DynamoDB (NoSQL)</font>

---

**Q: What are the 6 types of RDS available on Amazon?**

<font color=OrangeRed>SQL, MySQL, PostgreSQL, Oracle, Aurora, and MariaDB</font>

---

**Q: Which of these are relational database engines supported by Amazon RDS?**

<font color=OrangeRed>Amazon Aurora, PostgreSQL, MySQL</font>

---

**Q: Which of the below AWS services supports automated backups as a default configuration?**

<font color=OrangeRed>RDS</font>

---

**Q: When using Amazon RDS databases, which items are you charged for? (choose 2)**

CORRECT: <font color=OrangeRed>"Multi AZ"</font> is a correct answer.
CORRECT: <font color=OrangeRed>"Outbound data transfer"</font> is also a correct answer.
INCORRECT: "Backup up to the DB size" is incorrect - you do not pay for backup storage up to the size of the database. You only pay for backup storage in excess of the database size.

---

**Q: What are the key features of Relational Databases?**

1. Multiple Availability Zones (can be put in multiple AZs in case a disaster ruins one)
2. Read Replicas (there is a copy of the real database sent to an EC2 and <font color="blue">data is read from the copy of the database rather than the actual</font>. Information is written to the real database though. This avoids traffic.)

---

**Q: Which option allows failover to a second database in case the primary database fails?**

<font color=OrangeRed>Multi-AZ Deployment</font>

---

**Q: What are the differences between RDS and DynamoDB?**

> RDS does not support JSON document store models
> DynamoDB does support JSON document store models
> DynamoDB is a NoSQL database and RDS is a SQL database
> RDS provides other database software options
<font color=OrangeRed>DynamoDB does not provide alternative database software options</font>

---

**Q: Which of the benefits are of Amazon RDS?**

<font color=OrangeRed>Cost-Efficient, Scalable, Fully-managed, Resizeable Database</font>

---

**Q: How is a RDS different from a Non-Relational DB?**

<font color=OrangeRed>The columns in the table can vary and this won't affect other rows in the database (example, one row can have a home phone and a cell # while the next just has a cell #)</font>

---

**Q: What is Amazon's non-relational DB?**

<font color=OrangeRed>DynamoDB</font>

---

**Q: Which of the following NoSQL databases does Amazon DynamoDB replace?**

**Oracle NoSQL, Cassandra DB, MongoDB**

---

**Q: Which AWS database service is schema-less and can be scaled dynamically without incurring downtime?**

<font color=OrangeRed>DynamoDB</font>

---

**Q: Which DynamoDB feature provides in-memory acceleration to tables that result in significant performance improvements?**

<font color=OrangeRed>Amazon DynamoDB Accelerator (DAX)</font>

<font color="blue">A fully managed, highly available, in-memory cache for DynamoDB that delivers up to a 10x performance improvement - from milliseconds to microseconds - even at millions of requests per second. DAX does all the heavy lifting required to add in-memory acceleration to your DynamoDB tables, without requiring developers to manage cache invalidation, data population, or cluster management.</font>

"Amazon ElastiCache" is incorrect. This service is also an in-memory cache but it is not a feature of DynamoDB.

---

**Q: What is Elasticache?**

<font color=OrangeRed>A data caching database service</font>

Web server that caches the most common DB queries and returns it faster than a database (takes a big load off the PRODUCTION DB / speeds up performance of existing DBs).

---

**Q: What in-memory database engines does ElastiCache support?**

<font color=OrangeRed>Redis</font>
<font color=OrangeRed>Memcached</font>

---

**Q: What type of queries should be made to ElastiCache?**

<font color=OrangeRed>Common Queries</font>

---

**Q: What type of queries should be made in the production DB?**

<font color=OrangeRed>Unique queries</font>

---

**Q: Which service is best for storing common database query results, which helps to alleviate database access load?**

<font color=OrangeRed>Amazon ElastiCache</font>

---

**Q: What is Amazon's Data Warehouse called?**

<font color=OrangeRed>RedShift</font>

---

**Q: What is Redshift?**

<font color=OrangeRed>A data warehouse database service</font>

---

**Q: What is a Data Warehouse?**

<font color=OrangeRed>Built from ground up for complicated queries</font>

---

**Q: What is Red Shift OLAP used for?**

<font color=OrangeRed>Complex queries (its infrastructure is built for it)</font>

---

**Q: What is a con of OLAP (Online Analytics Processing)?**

<font color=OrangeRed>There is a performance lag</font>

---

**Q: What is Online Transaction Processing (OLTP)?**

<font color=OrangeRed>When you run a simple query and only return one row, OR when you simply add a row.</font>

---

**Q: What is Online Analytics Processing (OLAP)?**

<font color=OrangeRed>When you run a complex query and get several rows back. But there's a performance lag - people use data warehouses instead.</font>

---

**Q: Which AWS services are best suited for analyzing data using standard SQL and Business Intelligence (BI) tools?**

<font color=OrangeRed>Amazon Redshift</font>

---

**Q: What is Amazon's Graph Database called?**

<font color=OrangeRed>Amazon Neptune</font>

---

**Q: Which of the following database migrations are classified as heterogeneous?**

<font color=OrangeRed>Microsoft SQL Server to Amazon Aurora</font>
<font color=OrangeRed>Oracle to Amazon Aurora</font>

---

**Q: What feature of Amazon RDS helps to create globally redundant databases?**

<font color=OrangeRed>Cross-region read replicas</font>

---

**Q: Which of the following are benefits of Amazon RDS read replicas?**

<font color=OrangeRed>Increased availability</font>
<font color=OrangeRed>Enhanced performance</font>
<font color=OrangeRed>Designed for security</font>

**Automated backups are a feature of multi-AZ deployments, not a benefit of read replicas.**

---

**Q: Which AWS managed database provides processing power that is up to five times faster than a traditional MySQL database?**

> Aurora

**Q: Your company needs an application with a .NET layer that connects to a MySQL database. They want this application to be in AWS and use benefits such as five-times throughput, high availability, and automated backups. What database would be the ideal choice?**

<font color=OrangeRed>Aurora</font>

Aurora is a fully managed MySQL- and PostgreSQL-compatible relational database engine. It delivers up to five times the throughput of MySQL and up to three times the throughput of PostgreSQL.

---

**Q: How can a database administrator reduce operational overhead for a MySQL database?**

<font color=OrangeRed>Migrate the database onto an Amazon RDS instance</font>

---

**Q: Which AWS would you use to migrate an existing database to AWS?**

> AWS Snowball (for large data transport, not migration)
> AWS DMS

<font color="blue">AWS DMS (Database Migration Service) supports homogeneous migrations such as Oracle to Oracle, as well as heterogeneous migrations between different database platforms, such as Oracle or Microsoft SQL Server to Amazon Aurora. The source database remains fully operational during the migration, minimizing downtime.</font>

---

**Q: Which AWS service can be used to prepare and load data for analytics using an extract, transform and load (ETL) process?**

<font color=OrangeRed>AWS Glue</font>

---

**Q: Which services can be used to analyze data?**

<font color=OrangeRed>Amazon Kinesis</font> is used to analyze data and video streams in real time.
<font color=OrangeRed>QuickSight</font> is used to analyze visualizations of customer data.

---

## Compute Services

**Q: What is AWS Lambda?**

<font color=OrangeRed>Compute service</font>

---

**Q: Which of the following is not a use case for AWS Lambda?**

- Data processing
- Real-time stream processing
- Real-time file processing
- <font color=OrangeRed>Data warehousing</font> (this is NOT a Lambda use case)

---

**Q: Which of the following languages does AWS Lambda currently support?**

**Node.js, Ruby, Java** (and also Python, Go, C#, PowerShell)

---

**Q: Which of the following are true statements about AWS Lambda?**

<font color=OrangeRed>AWS Lambda integrates with most AWS services</font>
<font color=OrangeRed>AWS Lambda is scalable.</font>
<font color=OrangeRed>AWS Lambda does not require server management.</font>
<font color=OrangeRed>AWS Lambda only charges when code is executed and running.</font>

---

**Q: Which of the following are options for creating Lambda functions?**

<font color=OrangeRed>Author from scratch, using a blueprint, and browsing the serverless app repository</font>

---

**Q: Which of the following services are considered by AWS to be a serverless platform?**

<font color=OrangeRed>Amazon Aurora, Amazon Athena, AWS Lambda</font>

---

**Q: Which services are parts of the AWS serverless platform?**

<font color=OrangeRed>AWS Step Functions, DynamoDB, SNS, Lambda</font>

---

**Q: Which AWS services form the app-facing services of the AWS serverless infrastructure? (choose 2)**

<font color=OrangeRed>AWS Lambda and Amazon API Gateway</font> are both app-facing components of the AWS Serverless infrastructure.

**AWS Step Functions is an orchestration service.**

---

**Q: What is Amazon Athena?**

<font color=OrangeRed>An interactive query service that allows you to query data located in S3 using standard SQL. It's serverless and commonly used to analyze log data in S3.</font>

---

**Q: What are a few Athena use cases?**

1. Query log files in S3 (ELB logs, S3 access logs)
2. Generate business reports on the data stored in S3
3. Analyze AWS cost and usage reports
4. Run queries on click-stream data

---

**Q: Which of the following services is a serverless interactive query service for analytics?**

- AWS Lambda
- <font color=OrangeRed>Amazon Athena</font>

---

**Q: Which AWS service can assist with coordinating tasks across distributed application components for business process workflows?**

<font color=OrangeRed>SWF (Simple Workflow Service)</font>

---

**Q: What AWS service helps process a large amount of data sets?**

<font color=OrangeRed>EMR (Elastic Map Reduce)</font>

Analyzes and processes vast amounts of data by distributing the compute work across a cluster of servers. The cluster is managed using the open-source framework Hadoop.

---

**Q: Which AWS service can be used to process a large amount of data using the Hadoop framework?**

<font color=OrangeRed>Amazon Elastic Map Reduce (EMR)</font>

---

**Q: Which of the following AWS services can scale automatically without intervention? (choose 2)**

<font color=OrangeRed>Both S3 and DynamoDB</font> automatically scale as demand dictates.

**EBS and RDS do not scale automatically.** You must intervene to adjust volume sizes and database instance types to scale these resources.

---

## CloudFront and CDN

**Q: What is CloudFront?**

<font color=OrangeRed>Content Delivery Network</font>

---

**Q: CloudFront and edge locations - how does caching work?**

<font color=OrangeRed>The first time the user requests a file you download it from a bucket. Next time someone wants to download the same file, they will download it from the edge location rather than the actual bucket.</font>

---

**Q: What is an Edge Location?**

<font color=OrangeRed>A location where content will be cached</font>

Endpoints for AWS which are used for caching content.

---

**Q: What is a Distribution?**

<font color=OrangeRed>The name given to CDN which consists of a collection of edge locations</font>

---

**Q: What is an Origin?**

<font color="blue">The origin of all the files that the CDN will distribute.</font>

<font color=OrangeRed>Can be either an S3 Bucket, an EC2 instance, an elastic load balancer, or Route53.</font>

---

**Q: Do you read or write to Edge Locations?**

<font color=OrangeRed>You can read and write (write = put an object in them) to them.</font>

---

**Q: Do you get charged for clearing cached objects?**

<font color=OrangeRed>Yes</font>

---

**Q: How long are objects cached?**

<font color=OrangeRed>For the life of the TTL (time to live)</font>

---

**Q: What is RTMP distribution used for?**

<font color=OrangeRed>Media Streaming</font>

---

**Q: What is web distribution used for?**

<font color=OrangeRed>Used for websites</font>

---

**Q: Which AWS services are associated with Edge Locations? (choose 2)**

<font color=OrangeRed>AWS CloudFront</font>
<font color=OrangeRed>AWS Shield</font>

---

**Q: Use cases for Amazon CloudFront?**

<font color=OrangeRed>Security and encryption</font>
<font color=OrangeRed>Static asset caching</font>
<font color=OrangeRed>Live on-demand video streaming</font>

---

## Route 53

**Q: What is Route 53?**

<font color=OrangeRed>DNS service</font>

---

**Q: What is a DNS?**

<font color=OrangeRed>(Domain Name System) phone book for computers (search domain name in book and get the IP address)</font>

---

**Q: What are the three main functions of Route 53?**

<font color=OrangeRed>Health Checks, DNS (Domain Name System) service, Domain Registration</font>

---

**Q: Is Route53 global or regional?**

<font color=OrangeRed>Global</font>

---

**Q: What AWS service is used to manage DNS?**

<font color=OrangeRed>Route 53</font>

---

**Q: What service would be most useful in a disaster recovery situation?**

> Route 53

---

**Q: What two services in combination aid in DDoS mitigation?**

<font color=OrangeRed>CloudFront and Route 53</font>

---

## CloudWatch, CloudTrail, and Monitoring

**Q: By default, which timeframe does CloudWatch provide free analysis metrics?**

<font color=OrangeRed>5 minutes</font>

---

**Q: You would like to collect custom metrics from a production application every 1 minute. What type of monitoring should you use?**

<font color=OrangeRed>CloudWatch with detailed monitoring</font>

---

**Q: Which of the following are features of Amazon CloudWatch? (choose 2)**

<font color=OrangeRed>It is used to gain system-wide visibility into resource utilization</font>
<font color=OrangeRed>It can be accessed via API, command-line interface, AWS SDKs, and the AWS Management Console</font>

"It records account activity and service events from most AWS services" is incorrect - that is CloudTrail.

CloudWatch is for performance monitoring whereas CloudTrail is for auditing. CloudWatch is used to collect and track metrics, collect and monitor log files, and set alarms.

---

**Q: What can CloudWatch Monitor?**

Compute (EC2 instances, autoscaling groups, elastic load balancers, Route53 health checks), Storage, and Content Delivery (EBS Volumes, Storage Gateways, CloudFront)

---

**Q: How often does CloudWatch with EC2 monitor events?**

<font color=OrangeRed>Every 5 minutes by default</font> (you can make it 1 minute intervals by turning on detailed monitoring)

---

**Q: What are the types of Alarms and Events for AWS?**

1. Amazon <font color=OrangeRed>CloudWatch Alarms</font> (e.g., billing alarms)
2. Amazon <font color=OrangeRed>CloudWatch Events</font> (have the environment proactively respond to a change - e.g., upload a pic to S3 and auto add a watermark)
3. AWS <font color=OrangeRed>Lambda Scheduled Events</font> (setting things to happen at a certain time)
4. AWS <font color=OrangeRed>Web Application Firewall (WAF)</font> (security automations)

---

**Q: What AWS service is triggered to send a message by a CloudWatch Alarm?**

<font color=OrangeRed>SNS</font>

---

**Q: Which of the following services can Amazon CloudWatch use as a target to deliver near real-time streams of system events that describe changes in AWS resources?**

<font color=OrangeRed>EC2 instances, AWS Lambda functions, and Amazon SQS queues</font> are a few of the AWS services that can be configured as targets for CloudWatch events.

---

**Q: What AWS service could you use to see errors encountered when running scripts in Lambda?**

> AWS Inspector (INCORRECT - Inspector checks EC2)
<font color=OrangeRed>CloudWatch metrics and logs to watch for errors</font>
- AWS Config
- CloudTrail to monitor for errors

---

**Q: Which service allows you to monitor and troubleshoot systems using system and application log files generated by those systems?**

<font color=OrangeRed>CloudWatch Logs</font>

---

**Q: What is AWS CloudTrail?**

<font color=OrangeRed>A service that records AWS management console actions and APIs (IDs which users/accounts called AWS).</font>

CLOUD TRAIL IS ON A PER ACCOUNT AND PER REGION BASIS, BUT THE RESULTS FROM SEVERAL ACCOUNTS CAN BE PUT INTO A BUCKET IN THE PAYING ACCOUNT.

---

**Q: AWS CloudTrail is a service that enables which of the following?**

**Governance, Operational auditing, Compliance, Risk auditing**

"Resource metrics" is CloudWatch, not CloudTrail.

---

**Q: Which service stores log events for CloudTrail?**

<font color=OrangeRed>S3</font>

---

**Q: Which service helps in governance, compliance, and risk auditing?**

<font color=OrangeRed>CloudTrail</font>

AWS CloudTrail is a service that enables governance, compliance, operational auditing, and risk auditing of your AWS account.

---

**Q: How do you encrypt CloudTrail logs?**

<font color=OrangeRed>No action is needed since they are automatically encrypted.</font>

- Enable encryption. (INCORRECT)
- Enable KMS encryption. (INCORRECT)
- Send all logs to S3, and enable server-side encryption. (INCORRECT)

---

**Q: There was an incident in your company's AWS environment. You have been asked to review the API activity to determine the cause. What service captures AWS API calls and activity?**

**CloudTrail**

---

**Q: How do you consolidate several AWS account's CloudTrail logs into an S3 bucket?**

1. Turn on <font color="blue">CloudTrail</font> in paying account
2. Create a <font color="blue">bucket policy</font> that allows cross-account access
3. Turn on CloudTrail in the other accounts and use the bucket in the paying account

---

**Q: As an IT support center team member, you begin receiving calls about problems with your company's AWS-based point-of-sale system. You want to check with AWS for any service alerts they may be communicating. Which AWS tool will give you the information you seek?**

<font color=OrangeRed>The AWS Personal Health Dashboard</font>

Publishes <font color="blue">alerts</font> and remediation guidance when issues with AWS services arise. Notifications are also provided for scheduled events that may impact AWS customers.

**Trusted Advisor** provides valuable guidance for architecting your AWS environment and workloads, but doesn't include AWS service health information.

---

**Q: Which AWS service provides alerts when an AWS event may impact a company's AWS resources?**

<font color=OrangeRed>AWS Personal Health Dashboard</font>

---

**Q: Which service provides alerts and remediation guidance when AWS is experiencing events that may impact you?**

<font color=OrangeRed>AWS Personal Health Dashboard</font> provides alerts and remediation guidance when AWS is experiencing events that may impact you.

"AWS Inspector" is incorrect. Inspector is an automated security assessment service that helps improve the security and compliance of applications deployed on AWS.

"AWS Trusted Advisor" is incorrect. Trusted Advisor is an online resource that helps to reduce cost, increase performance and improve security by optimizing your AWS environment.

---

## Security Services

**Q: Which AWS service can be used to generate encryption keys that can be used to encrypt data? (Select TWO.)**

<font color=OrangeRed>AWS KMS</font>
<font color=OrangeRed>AWS CloudHSM</font>

You use Customer Master Keys (CMKs) to create data encryption keys. The data encryption keys can then be used to actually encrypt the data.

---

**Q: In regards to AWS KMS, which of these statements are true?**

AWS KMS is integrated with S3 for the purpose of **logging** AWS KMS key usage.

<font color=OrangeRed>Keys may be generated in KMS, CloudHSM cluster, or imported from other encryption key services.</font>

~~AWS KMS does not integrate with any other AWS services.~~ (INCORRECT)

---

**Q: What service does AWS KMS integrate with for logging of key events?**

<font color=OrangeRed>CloudTrail</font>

---

**Q: In this scenario, we want to enable notifications for KMS activity. What AWS service could be used with AWS KMS to send these notifications?**

<font color=OrangeRed>SNS</font>

---

**Q: Which AWS service helps customers meet corporate, contractual, and regulatory compliance requirements for data security by using dedicated hardware appliances within the AWS Cloud?**

<font color=OrangeRed>AWS CloudHSM</font>

---

**Q: Which AWS service protects against common exploits that could compromise application availability, compromise security or consume excessive resources?**

<font color=OrangeRed>AWS WAF</font>

---

**Q: What is AWS WAF?**

<font color=OrangeRed>A web application firewall that inspects web traffic and looks for people doing malicious things (designed to stop hackers - SQL injections, etc.)</font>

---

**Q: Which service provides protection for web applications behind an ELB?**

- AWS Shield (DDoS)
- Amazon Inspector (analyze VPC)
- AWS GuardDuty (detect)
- <font color=OrangeRed>AWS WAF</font>

---

**Q: In regards to security and compliance on AWS, what AWS service is a threat detection service that monitors for threats to AWS accounts and workloads?**

- AWS Shield (against DDoS)
- AWS WAF
- <font color=OrangeRed>AWS GuardDuty</font> (Detection service)
- Amazon Inspector (VPC)

---

**Q: Which AWS service helps identify malicious or unauthorized activities in AWS accounts and workloads?**

<font color=OrangeRed>Amazon GuardDuty</font>

---

**Q: What is AWS Shield?**

<font color=OrangeRed>A Distributed Denial of Service (DDoS) mitigation service designed to protect web applications on AWS.</font>

---

**Q: Which of the following can be used to protect your environment from DDoS attacks?**

<font color=OrangeRed>AWS CloudFront</font>
<font color=OrangeRed>AWS Shield and AWS Shield Advanced</font>
<font color=OrangeRed>AWS ELB</font>

---

**Q: Which of the following penetration testing activities are prohibited on AWS?**

<font color=OrangeRed>DDoS attacks</font>
<font color=OrangeRed>Port flooding</font>
<font color=OrangeRed>DNS Zone walking via Amazon Route 53 hosted zones</font>

Penetration testing of EC2 instances and AWS CloudFront (allowed without prior approval)

---

**Q: In regards to penetration testing on AWS, which statement is true?**

- No penetration testing is allowed on AWS.
- All penetration testing on AWS requires permission.
- <font color=OrangeRed>Limited penetration testing is allowed, but some require permission from AWS.</font>
- All penetration testing is allowed on AWS.

---

**Q: Which of these are allowed penetration testing WITHOUT prior approval from AWS?**

- Amazon Route 53 (NOT allowed without approval)
- > Amazon CloudFront (listed as allowed in notes)
- <font color=OrangeRed>Amazon EC2 instances</font>
- <font color=OrangeRed>Amazon RDS</font>
- Amazon S3 (NOT allowed without approval per notes)

---

**Q: Which of the following services is NOT allowed penetration testing without prior approval?**

- Amazon RDS
- Amazon EC2
- Amazon Lightsail
- <font color=OrangeRed>Amazon S3</font>

---

**Q: What is Amazon Inspector?**

<font color=OrangeRed>Automatically assesses EC2s for vulnerabilities or deviations from best practices. Results come in the form of detailed list of security findings prioritized by level of severity. (ONLY FOR EC2 INSTANCES!!!)</font>

---

**Q: In this scenario, an AWS datacenter was breached by unauthorized personnel. In terms of the AWS Shared Responsibility Model, who is responsible for this?**

<font color=OrangeRed>AWS</font>

---

**Q: What is Macie?**

<font color=OrangeRed>Uses AI to analyze data in S3 and helps identify Personally Identifiable Information (PII - drivers license id, home address, info that can be used and stolen by criminals). Also used to analyze CloudTrail logs for suspicious API activity.</font>

---

**Q: In this scenario, we want a video/image analysis service for facial recognition purposes. Which of the following services can serve this purpose?**

<font color=OrangeRed>AWS Rekognition</font>

---

**Q: Which of the following techniques can be used to prevent unauthorized access to AWS?**

<font color=OrangeRed>MFA multi-factor authentication</font>

---

**Q: A Cloud Practitioner must determine if any security groups in an AWS account have been provisioned to allow unrestricted access for specific ports. What is the SIMPLEST way to do this?**

<font color=OrangeRed>Trusted Advisor</font> has a check that can review the ports which have unrestricted access (0.0.0.0/0)

---

**Q: What is AWS Config?**

<font color=OrangeRed>A service that provides a detailed view of the configuration (settings) on AWS resources (this includes how resources are related to each other and how they were configured in the past).</font>

---

**Q: If a customer needs to audit the change management of AWS resources, which of the following AWS services should the customer use?**

<font color=OrangeRed>AWS Config</font>

---

**Q: What are AWS Artifacts?**

<font color=OrangeRed>Used to retrieve compliance reports</font>

---

**Q: Where can AWS compliance and certification reports be downloaded?**

<font color=OrangeRed>AWS Artifact</font>

---

**Q: Medium Corp is going through an audit as part of the HIPAA compliance. Auditor wants to see the reports that the AWS services which are being used by Medium Corp are compliant against HIPAA. What can Medium Corp do to get those reports?**

<font color=OrangeRed>Get reports via AWS Artifact</font>

---

**Q: Where are AWS compliance documents, such as an SOC 1 report, located?**

<font color=OrangeRed>AWS Artifact</font>

---

**Q: Which of the following are components of the AWS Assurance Program?**

- Following industry best practices
- <font color=OrangeRed>Compliance with Laws and Regulations</font>
- <font color=OrangeRed>Certifications/Attestations</font>

---

**Q: Which of the following are components of the AWS Risk and Compliance Program?**

<font color=OrangeRed>Control Environment, Risk Management, Information Security</font>

---

## Shared Responsibility Model

**Q: In regards to the AWS Shared Responsibility Model, AWS maintains responsibility \_\_.**

<font color=OrangeRed>of the cloud</font>

---

**Q: In regards to the Shared Responsibility Model, for which of these is AWS Responsible?**

<font color=OrangeRed>CPU on physical hardware</font>
<font color=OrangeRed>Host virtualization hardware</font>
<font color=OrangeRed>Availability Zones</font>

---

**Q: What things will Amazon be responsible for securing on AWS?**

1. Management of Data Centers
2. Security Cameras
3. Cabling
4. Patching RDS Operating Systems

---

**Q: What things will you be responsible for securing on AWS?**

Things you can do yourself on the AWS console or in EC2:
1. Security groups
2. IAM users
3. Patching EC2 operating systems
4. Patching databases running on EC2

---

**Q: Under the shared responsibility model, what are examples of shared controls? (choose 2)**

1. **Patch Management** - AWS is responsible for patching and fixing flaws within the infrastructure, but customers are responsible for patching their guest OS and applications.
2. **Configuration Management** - AWS maintains the configuration of its infrastructure devices, but a customer is responsible for configuring their own guest operating systems, databases, and applications.

---

**Q: Which of the following is a shared control between the customer and AWS?**

<font color=OrangeRed>AWS is responsible for creating awareness and providing training of their employees. Client is responsible to do the same for their employees.</font>

---

**Q: Under the shared responsibility model, which of the following is a shared control between a customer and AWS?**

<font color=OrangeRed>Patch management</font>

---

**Q: In an AWS Shared Responsibility model, which of the following is NOT the responsibility of AWS?**

<font color=OrangeRed>Data of the customer</font>

---

**Q: According to the AWS Shared Responsibility Model, what is AWS responsible for when you create a security group?**

<font color=OrangeRed>Making sure the security groups are linked to the Elastic Network Interface (ENI) of the EC2 instance</font>
~~Defining the outbound rules~~ (INCORRECT)
<font color=OrangeRed>Making sure the security group rules are applied immediately</font>
> Defining the inbound rules (INCORRECT - this is the customer's responsibility)

---

**Q: Which task is AWS responsible for in the shared responsibility model for security and compliance?**

<font color=OrangeRed>Updating Amazon EC2 host firmware</font>

---

**Q: Who is responsible for encryption?**

<font color=OrangeRed>Both you and Amazon</font>

---

**Q: Which of the following is true about data security in AWS?**

<font color=OrangeRed>AWS is responsible for the security of the software that manages the data</font>

---

## Messaging and Application Services

**Q: Which service can be used for building and integrating loosely-coupled, distributed applications?**

<font color=OrangeRed>Amazon SNS</font>

AWS messaging services SQS and SNS can be applied at architectural level to build loosely coupled systems that facilitate multiple business use cases.

---

**Q: The components of SNS are \_.**

<font color=OrangeRed>Subscribers, Publishers, SNS Topics</font>

---

**Q: Which of the following are examples of endpoints for an SNS topic?**

<font color=OrangeRed>Webserver, email address, Amazon SQS queue, SMS, and AWS Lambda function</font>

---

**Q: Which of the following is NOT a way SNS can send a notification?**

- HTTP
- SMS
- Email
- <font color=OrangeRed>Phone call</font> (SNS does NOT support phone calls)

---

**Q: If you want to use decoupled resources, which of the following AWS services can assist you?**

<font color=OrangeRed>Amazon Simple Queue Service (SQS)</font>

A fully managed message queuing service that enables you to decouple and scale microservices, distributed systems, and serverless applications.

---

**Q: One of the main requirements given by your director is to host an environment that reduces inter-dependencies so failures do not impact other components. Which concept is correct?**

> Separation (INCORRECT)
- Integration (INCORRECT)
<font color=OrangeRed>Decoupling</font>
- Tight coupling (INCORRECT)

<font color="blue">In microservice architectures, applications are built and deployed as highly decoupled, focused services. A decoupled application architecture allows each component to perform its tasks independently.</font>

---

**Q: Which services are parts of the AWS serverless platform?**

<font color=OrangeRed>AWS Step Functions, DynamoDB, SNS, Lambda</font>

---

**Q: What AWS service lets connected devices easily and securely interact with cloud applications and other devices?**

<font color=OrangeRed>Amazon IoT Core</font>

---

## Deployment and Automation Services

**Q: What is Elastic Beanstalk?**

<font color=OrangeRed>A way to quickly deploy and manage applications in the AWS Cloud without worrying about the infrastructure that runs those applications.</font>

---

**Q: A user has limited knowledge of AWS services, but wants to quickly deploy a scalable Node.js application in an Amazon VPC. Which service should be used to deploy the application?**

<font color=OrangeRed>AWS Elastic Beanstalk</font> is an easy-to-use service for deploying and scaling web applications and services developed with Java, .NET, PHP, Node.js, Python, Ruby, Go, and Docker.

You can simply upload your code and Elastic Beanstalk automatically handles the deployment, from capacity provisioning, load balancing, auto-scaling to application health monitoring.

---

**Q: Which service provides the ability to simply upload applications and have AWS handle the deployment details of capacity provisioning, load balancing, auto-scaling, and application health monitoring?**

<font color=OrangeRed>AWS Elastic Beanstalk</font>

"AWS OpsWorks" is incorrect. AWS OpsWorks provides a managed service for Chef and Puppet. This service is involved with automation and configuration management.

---

**Q: AWS Elastic Beanstalk handles deployment of which application types?**

<font color=OrangeRed>Java, .NET, PHP, Node.js, Python, Ruby, Go, and Docker</font>

---

**Q: Are Elastic Beanstalk and CloudFormation free?**

<font color=OrangeRed>Yes, but the resources they provision are not (EC2 instances and others).</font>

---

**Q: Can Cloud Formation provision everything? Is it programmable?**

<font color=OrangeRed>Yes, it can provision almost any AWS service and it is programmable.</font>

---

**Q: Can Elastic Beanstalk provision everything? Is it programmable?**

<font color=OrangeRed>No, it is limited in what it can provision and it is not programmable.</font>

---

**Q: What is the difference between CloudFormation and Elastic Beanstalk?**

<font color="blue">CloudFormation can provision almost any AWS service and is programmable. Elastic Beanstalk is limited in what it can provision and is not programmable.</font>

---

**Q: What AWS service provides infrastructure as code?**

> OpsWorks (INCORRECT - OpsWorks is for Chef/Puppet)

<font color="blue">AWS CloudFormation provides infrastructure as code. You make a template of what you want in AWS and then CloudFormation creates it for you.</font>

---

**Q: Which AWS tools can be used for automation? (choose 2)**

<font color=OrangeRed>AWS Elastic Beanstalk</font> and <font color=OrangeRed>AWS CloudFormation</font> are both examples of automation. Beanstalk is a platform service that leverages the automation capabilities of CloudFormation to build out application architectures.

---

**Q: What is the term for describing the action of automatically running scripts on Amazon EC2 instances when launched to install software?**

A. <font color=OrangeRed>Bootstrapping</font> - the execution of automated actions to services such as EC2 and RDS. This is typically in the form of scripts that run when the instances are launched.
B. <font color="blue">Golden Images</font> - snapshots of pre-configured EBS volumes that can be used to launch new instances via Amazon Machine Images (AMIs).
C. <font color="blue">Containers</font> - packaged software that runs in a Docker image. Services such as Amazon ECS and Fargate can run Docker containers.
D. <font color="blue">Workflow automation</font> - a process of orchestrating automated actions. Associated with services such as Chef and Puppet or AWS OpsWorks.

---

**Q: When instantiating compute resources, what are two techniques for using automated, repeatable processes that are fast and avoid human error? (choose 2)**

1. With <font color=OrangeRed>infrastructure as code</font> AWS assets are programmable; apply techniques, practices, and tools from software development to make your whole infrastructure reusable, maintainable, extensible, and testable.
2. With <font color=OrangeRed>bootstrapping</font>, execute automated actions to modify default configurations. This includes scripts that install software or copy data to bring that resource to a particular state.

---

**Q: A mobile shopping list app needs to be able to add, delete, and update items on specific lists anytime a user desires. The backend for the app will run on Amazon EC2 instances with Auto Scaling. What design characteristic must be incorporated into the app?**

<font color=OrangeRed>Make sure the app doesn't store previous transaction or session information on specific EC2 instances.</font>

That way, any EC2 instance provisioned by Auto Scaling can process the request. For horizontal scaling to be effective, make sure the app doesn't store previous transaction or session information on specific EC2 instances.

**Leveraging load balancing** is a good practice, but doesn't address the need for a **stateless app**. **Session affinity** directs a load balancer to route transactions to a specific instance each time. **Bootstrapping** runs scripts each time an EC2 instance is provisioned.

---

**Q: What is the name of the AWS managed Docker registry service used by the Amazon Elastic Container Service (ECS)?**

<font color=OrangeRed>Amazon Elastic Container Registry (ECR)</font>

---

**Q: Which AWS service is primarily used for software version control?**

<font color=OrangeRed>AWS CodeCommit</font> - a fully-managed source control service that hosts secure Git-based repositories.

---

**Q: Which service's PRIMARY purpose is software version control?**

<font color=OrangeRed>AWS CodeCommit</font>

---

**Q: What AWS services can be used on premises?**

1. <font color=OrangeRed>Snowball</font> (large disc Amazon sends you, you upload data and send it back, they upload to S3)
2. <font color=OrangeRed>Snowball Edge</font> (Snowball with CPU, basically a computer with storage)
3. <font color=OrangeRed>Storage Gateway</font> (way of caching your files and replicating to S3 - must stay on-premises the whole time)
4. <font color=OrangeRed>CodeDeploy</font> (way to deploy code to EC2 instances/applications or on-premises web servers)
5. <font color=OrangeRed>Opsworks</font> (used to deploy EC2 or on-premises web servers)
6. <font color=OrangeRed>IoT Greengrass</font> (IoT and connects your devices to cloud)

---

**Q: What is Amazon Mechanical Turk used for?**

<font color=OrangeRed>Crowdsourcing marketplace where you can outsource tasks.</font>

---

**Q: Treating infrastructure as code in the AWS Cloud allows users to:**

<font color=OrangeRed>Automate the infrastructure provisioning process.</font>

---

## AWS Organizations and Multi-Account

**Q: What is AWS Organizations?**

<font color=OrangeRed>An account management service that enables you to consolidate multiple AWS accounts into an organization that you create and centrally manage - 2 main features are: consolidated billing and all features.</font>

---

**Q: Which service can be used to easily create multiple accounts?**

<font color=OrangeRed>AWS Organizations</font> can be used for automating AWS account creation via the Organizations API.

---

**Q: In regards to AWS Organizations, which of the following is true?**

<font color=OrangeRed>AWS Organizations provides policy-based management for multiple AWS accounts.</font>

---

**Q: Which of these is NOT a feature of AWS Organizations?**

- It provides the ability to centrally manage multiple AWS accounts.
- It provides the ability to centrally manage the billing of multiple AWS accounts.
- It provides the ability to centrally manage service usage.
- <font color=OrangeRed>It provides the ability to centrally manage all AWS accounts from ANY account within the organization.</font> (INCORRECT - only allows one account to be the master account)
- > It provides the ability to automate account creation and management.

---

**Q: In this scenario, we want to control service usage across multiple AWS accounts using AWS Organizations. Which of the following would be used?**

<font color=OrangeRed>Service Control Policies</font>

Using AWS Organizations allows for the creation of SCPs (Service Control Policies) to manage service usage across multiple AWS accounts.

---

**Q: Which of the following statements is correct in relation to consolidated billing? (choose 2)**

<font color=OrangeRed>Paying accounts are independent and cannot access resources of other accounts</font>
<font color=OrangeRed>One bill is provided per AWS organization</font>

Consolidated billing is available to all customers. Volume pricing discounts can be applied to resources and this is a key advantage.

---

**Q: How can consolidated billing within AWS Organizations help lower overall monthly expenses?**

<font color=OrangeRed>By pooling usage across multiple accounts to achieve a pricing tier discount</font>

---

**Q: With consolidated billing, can a paying account make changes to any of the resources owned by the linked accounts?**

<font color=OrangeRed>No</font>

---

**Q: How should the paying account be used?**

<font color=OrangeRed>It should be used for billing purposes only. IT SHOULD NOT BE USED TO DEPLOY RESOURCES INTO THE AWS ENVIRONMENT.</font>

---

**Q: What is the maximum number of linked accounts per paying account under consolidated billing?**

<font color=OrangeRed>20 linked accounts</font>

---

**Q: How can a company separate costs for storage, Amazon EC2, Amazon S3, and other AWS services by department?**

<font color=OrangeRed>Add department-specific tags to each resource</font>

---

**Q: What strategy can assist with allocating metadata to AWS resources for cost tracking and visibility?**

<font color=OrangeRed>Tagging</font>

AWS allows customers to assign metadata to their AWS resources in the form of tags. Each tag is a simple label consisting of a customer-defined key and an optional value that can make it easier to manage, search for, and filter resources. AWS Cost Explorer and detailed billing reports support the ability to break down AWS costs by tag.

---

**Q: The use of what AWS feature or service allows companies to track and categorize spending on a detailed level?**

<font color=OrangeRed>Cost allocation tags</font>

---

**Q: What is a resource group?**

<font color=OrangeRed>A collection of resources that share one or more tags (or portions of tags)</font>

---

**Q: What is the tag editor?**

<font color=OrangeRed>A global service that allows us to discover resources and to add additional tags to them as well</font>

---

**Q: Which AWS feature allows a company to take advantage of usage tiers for services across multiple member accounts?**

### <font color=OrangeRed>Consolidated billing</font>

---

**Q: Which AWS service provides a quick and automated way to create and manage AWS accounts?**

<font color=OrangeRed>AWS Organizations</font>

---

## Cost Management and Billing

<font color="#7f0080">AWS Cost Management Tools Summary:</font>

- <font color=OrangeRed>AWS Organizations:</font> consolidate billing between multiple AWS accounts.
- <font color=OrangeRed>AWS Pricing Calculator:</font> replacing the AWS Simple Calculator
- <font color=OrangeRed>AWS TCO Calculator:</font> an estimation of the cost savings to be had by migrating to the AWS Cloud from an on-premises datacenter.
- <font color=OrangeRed>AWS Cost Explorer:</font> free tool that allows for viewing charts and a history of AWS costs. 13 months
- <font color=OrangeRed>AWS Simple Calculator:</font> calculate anticipated bill for resources we are about to create. 3 months

---

**Q: Which accurately describes the function of the AWS Cost Explorer?**

- ~~The AWS Cost Explorer is used to estimate the anticipated AWS bill.~~ (INCORRECT)
- <font color=OrangeRed>The AWS Cost Explorer is a free, easy to use tool that allows for viewing charts and usage history in order to manage AWS costs over time.</font>

---

**Q: AWS Cost Explorer will forecast \_ months of billing.**

- ~~13 months~~ (INCORRECT)
- <font color=OrangeRed>3 months</font>

---

**Q: What is the difference between Budget and Cost Explorer?**

<font color=OrangeRed>BUDGET is used to predict costs BEFORE they are incurred</font>
<font color=OrangeRed>COST EXPLORER is used to explore costs AFTER they have been incurred</font>

---

**Q: You have just set up a new environment in AWS and want to see what costs are being incurred for the resources you are using. What would you use?**

<font color=OrangeRed>Cost Explorer</font>

View your costs and view data for the last 13 months. You can also forecast how much you might spend for the next three months and get recommendations for which instances to purchase.

---

**Q: Which service is used to pay AWS bills, and monitor usage and budget costs?**

<font color=OrangeRed>AWS Billing and Cost Management</font>

---

**Q: Which AWS Cost Management tool allows you to view the most granular data about your AWS bill?**

<font color=OrangeRed>AWS Cost and Usage Report</font>

---

**Q: Which features or services can be used to monitor costs and expenses for an AWS account? (Choose two.)**

<font color=OrangeRed>AWS Cost and Usage Report</font>
<font color=OrangeRed>Billing alerts and Amazon CloudWatch alarms</font>

---

**Q: What are the billing alarms/alerts?**

<font color=OrangeRed>Alert you when a certain level of AWS spend has been reached</font>

---

**Q: Which AWS services can be used to create billing alarms?**

<font color=OrangeRed>Cost Explorer</font>
<font color=OrangeRed>CloudWatch</font>

---

**Q: Which AWS service can a customer use to set up an alert notification when the account is approaching a particular dollar amount?**

<font color=OrangeRed>AWS Budgets</font>

---

**Q: AWS Budgets can be used to:**

<font color=OrangeRed>Set resource limits in account to prevent overspending</font>

---

**Q: A user wants guidance on possible savings when migrating from on-premises to AWS. Which tool is suitable for this scenario?**

<font color=OrangeRed>TCO Calculator</font>

---

**Q: What is the AWS Total Cost of Ownership/TCO calculator?**

<font color=OrangeRed>A calculator used to compare the cost of running your infrastructure on-premises vs. the cloud. Generates nice reports to show the C-level executives.</font>

---

**Q: What is the AWS Simple Monthly Calculator?**

<font color=OrangeRed>Tool used to calculate your running costs on AWS on a per month basis. NOT A COMPARISON TOOL.</font>

---

**Q: A Cloud Practitioner is asked how to estimate the cost of using a new application on AWS. What is the MOST appropriate response?**

<font color="blue">AWS Simple Monthly Calculator for estimates.</font>

---

**Q: How can a company isolate the costs of production and non-production workloads on AWS?**

<font color=OrangeRed>Use different accounts</font>

---

**Q: What two AWS services receive bulk discounted pricing for agreeing to pay for a term?**

<font color=OrangeRed>RDS</font>
<font color=OrangeRed>EC2</font>

---

**Q: Which of the following is TRUE about the AWS Pricing Model?**

<font color=OrangeRed>AWS does not charge a termination fee.</font>

---

**Q: Which of the following statements is TRUE?**

<font color=OrangeRed>AWS Organizations is a service available to all AWS customers at no additional costs.</font>

---

**Q: Which types of pricing policies does AWS offer? (choose 2)**

<font color=OrangeRed>pay-as-you-go</font>
<font color=OrangeRed>save when you reserve</font>
<font color=OrangeRed>pay less by using more.</font>

---

**Q: How is storage typically priced on AWS cloud?**

<font color=OrangeRed>Charged per GB</font>

---

**Q: Which of the following is NOT a pricing factor for EC2?**

- Reserved purchasing
- AMI
- <font color=OrangeRed>Request pricing</font> (this is NOT a factor)
- Region
- Instance type

---

**Q: Which of the following are advantages of the AWS Cloud? (Choose two.)**

- Fixed-rate monthly cost (INCORRECT)
- <font color=OrangeRed>No need to guess capacity requirements</font>
- <font color=OrangeRed>Increased speed to market</font>
- Increased upfront capital expenditure (INCORRECT)
- Physical access to cloud data centers (INCORRECT)

---

## AWS Support Plans

<font color="#7f0080">Support Plan Summary:</font>

| Plan | Cost | Support |
|------|------|---------|
| Basic | Free | No tech support |
| Developer | $29/month (scales on usage) | Business hours via email, 1 person, unlimited cases |
| Business | $100/month (scales on usage) | 24x7 via email, chat, phone - unlimited people/cases |
| Enterprise | $15,000/month (scales on usage) | Has TAM - 24x7, email, chat, phone - unlimited people/cases |

---

**Q: Which support plan is the lowest cost option that allows unlimited cases to be open?**

<font color=OrangeRed>Developer</font>

---

**Q: Which type of account receives only email access to Cloud Support Associates during business hours?**

<font color=OrangeRed>Developer</font>

~~Basic accounts have no access to Cloud Support representative access.~~

---

**Q: Which of the following AWS accounts do NOT have 24/7 access to Cloud Support Engineers?**

<font color=OrangeRed>Basic and Developer</font>

---

**Q: What support do you get with the Basic plan?**

<font color=OrangeRed>None!</font>

---

**Q: Which of the following types of AWS accounts have access to AWS Personal Health Dashboard?**

<font color=OrangeRed>Basic, Developer, Business, and Enterprise</font>

---

**Q: Which of the following types of AWS accounts have access to AWS Trusted Advisor?**

> Basic, Developer, Business, and Enterprise

---

**Q: Which of the following type of account receives the highest priority access to customer service and technical support?**

<font color=OrangeRed>Enterprise</font>

---

**Q: Which of the following type of AWS account will receive support in less than 15 minutes when the support case is related to business-critical systems down?**

<font color=OrangeRed>Enterprise</font>

---

**Q: For a developer account, how long will it take for someone to get back to you when you have a question about general guidance and system impairments?**

<font color=OrangeRed>Less than 24 hours for general guidance</font>
<font color=OrangeRed>Less than 12 hours for system impairments</font>

---

**Q: For a business account, how long will it take for someone to get back to you when you have a question about general guidance, system impairments, production system impairments, and production system down?**

<font color=OrangeRed>Less than 24 hours for general</font>
<font color=OrangeRed>Less than 12 hours for system impairments</font>
<font color="blue">Less than 4 hours for production system impaired</font>
<font color="blue">Less than 1 hour for production system down</font>

---

**Q: For an enterprise account, how long will it take for someone to get back to you?**

<font color=OrangeRed>Less than 24 hours for general</font>
<font color=OrangeRed>Less than 12 hours for system impairments</font>
<font color=OrangeRed>Less than 4 hours for production system impaired</font>
<font color=OrangeRed>Less than 1 hour for production system down</font>
<font color=OrangeRed>Less than 15 minutes for business-critical</font>

---

**Q: Why is the business support plan better than the developer?**

<font color=OrangeRed>You also get support on production system impaired AND production system down issues (response within an hour)</font>

---

**Q: Why is the enterprise support plan better than the business?**

<font color=OrangeRed>You get support on business-critical system down issues (response within 15 minutes)</font>

---

**Q: You need an AWS support plan for your production workloads, but want to keep costs to a minimum. Which of the following plans should you choose?**

**Developer** (if just need support, lowest cost production plan)

The **Business** Support plan is specifically designed for production workloads in AWS.

---

**Q: Which is the MINIMUM AWS Support plan that allows for one-hour target response time for support cases?**

**Business**

---

**Q: Which AWS support plans provide 24x7 access to customer service?**

<font color=OrangeRed>All plans</font>

---

**Q: Which AWS support plan includes a dedicated Technical Account Manager?**

<font color=OrangeRed>Enterprise</font>

---

**Q: Which among them is a unique feature in AWS Enterprise Support Plan?**

<font color=OrangeRed>TAM - dedicated technical account manager</font>

---

**Q: Which among these is an important feature of AWS Business Support plan?**

<font color=OrangeRed>24/7 cloud support engineers</font>

---

**Q: Which among these is one of the features of the AWS Developer Support Plan?**

<font color=OrangeRed>Business hours by cloud support associates.</font>

---

**Q: Which is the minimum AWS Support plan that includes Infrastructure Event Management without additional costs?**

<font color=OrangeRed>Enterprise</font>

---

**Q: How does the AWS Enterprise Support Concierge team help users?**

<font color=OrangeRed>Provide architecture guidance</font>

AWS Enterprise Support provides concierge-like service where the main focus is helping you achieve your outcomes and find success in the cloud.

---

**Q: A user has an AWS account with a Business-level AWS Support plan and needs assistance with handling a production service disruption. Which action should the user take?**

<font color=OrangeRed>Open a production system down support case</font>

---

## AWS Trusted Advisor

**Q: What is AWS Trusted Advisor?**

<font color=OrangeRed>A resource that provides real-time guidance to help you provision your resources following AWS best practices. For ALL of AWS environment. Also advises on cost optimization, performance, security, and fault tolerance.</font>

(Unlike Amazon Inspector which is just for EC2s)

---

**Q: AWS Trusted Advisor provides insight into which five categories of an AWS account?**

> Performance, fault tolerance, cost optimization, security, and service limits

---

**Q: Which of the five best practices does AWS Trusted Advisor use to eliminate unused, underutilized, and idle resources in your environment?**

<font color="blue">Cost optimization</font>

---

**Q: Which is NOT one of the seven core checks performed by AWS Trusted Advisor?**

- IAM use
- <font color=OrangeRed>Amazon EC2 Reserved Instances Optimization</font> (NOT a core check)
- <font color=OrangeRed>Unassociated Elastic IP Addresses</font> (NOT a core check)
- EBS Public Snapshots
- Security Groups (port checks)
- RDS Public Snapshots

---

**Q: How does AWS Trusted Advisor provide guidance to users of the AWS Cloud? (Choose two.)**

<font color=OrangeRed>It provides a list of cost optimization recommendations based on current AWS usage</font>
<font color=OrangeRed>It detects potential security vulnerabilities caused by permissions settings on account resources</font>

---

## Well-Architected Framework

**Q: Which AWS concepts refer to "established best practices developed through lessons learned by working with customers"?**

<font color=OrangeRed>Well-Architected Framework</font>

---

**Q: Which of the pillars of the well-architected framework is defined as the ability to run and monitor systems to deliver business value and to continually improve supporting processes and procedures?**

<font color=OrangeRed>Operational excellence</font>

---

**Q: Which of the following are pillars of the AWS Well-Architected Framework? (Choose two.)**

- Multiple Availability Zones (NOT a pillar)
- <font color=OrangeRed>Performance efficiency</font>
- <font color=OrangeRed>Security</font>
- Encryption usage (NOT a pillar)
- High availability (NOT a pillar)

---

**Q: Which of the following is an AWS Well-Architected Framework design principle related to reliability?**

<font color=OrangeRed>Ability to recover from failure</font>

---

**Q: What option below will increase the fault tolerance of your application in AWS?**

- Deploy resources to multiple AWS accounts
- Deploy resources to multiple subnets
- <font color=OrangeRed>Deploy resources across multiple availability zones</font>
- > Deploying resources across multiple edge locations (this reduces latency, not fault tolerance)

---

## Miscellaneous / AWS Services Reference

**Q: Which AWS services are defined as global instead of regional?**

<font color=OrangeRed>S3</font>
<font color=OrangeRed>Amazon CloudFront</font>

What Amazon services are global: <font color=OrangeRed>Route53, Roles, IAM, and S3</font>

Other global services: IAM, Route53, CloudFront, SNS, SES

---

**Q: Which services are managed at a regional (rather than global) level? (choose 2)**

Both <font color=OrangeRed>EC2</font> and <font color=OrangeRed>S3</font> are managed at a regional level.

---

**Q: Which service allows an organization to view operational data from multiple AWS services through a unified user interface and automate operational tasks?**

<font color=OrangeRed>AWS Systems Manager</font>

"Amazon CloudWatch" is incorrect. CloudWatch is a monitoring service for AWS cloud resources and the applications you run on AWS. You use CloudWatch for performance monitoring, not automating operational tasks.

---

**Q: How does the Systems Manager work?**

<font color=OrangeRed>A piece of software is installed on each virtual machine</font>

---

**Q: Where can the System Manager be housed?**

<font color=OrangeRed>Inside AWS or on-premises</font>

---

**Q: Systems Manager is used to:**

<font color=OrangeRed>Manage fleets of EC2 instances and virtual machines</font>

---

**Q: A Cloud Practitioner wants to build an application stack that will be highly elastic. What AWS services can be used that don't require you to make any capacity decisions upfront? (choose 2)**

<font color=OrangeRed>S3 and Lambda</font>

---

**Q: What is the added value of being able to access your environment using cloud services through an API?**

> Allows you to work with AWS services and resources programmatically

---

**Q: What is AWS Landing Zone?**

<font color=OrangeRed>Tool to help customers quickly set up a secure, multi-account (4 initially) AWS environment based on AWS best practices.</font>

---

**Q: What is AWS Quick Start?**

<font color=OrangeRed>A way of deploying environments quickly using CloudFormation templates built by the AWS Solution Architects (experts).</font>

---

**Q: What are AWS Marketplace functions? (Choose two.)**

<font color=OrangeRed>Sell solutions to other AWS users</font>
<font color=OrangeRed>Buy third-party software that runs on AWS</font>

~~Sell unused Amazon EC2 Spot Instances~~ (INCORRECT)

---

**Q: A company wants to try a third-party ecommerce solution before deciding to use it long term. Which AWS service or tool will support this effort?**

<font color=OrangeRed>AWS Marketplace</font>

---

**Q: Where should a company go to search software listings from independent software vendors to find, test, buy and deploy software that runs on AWS?**

<font color=OrangeRed>AWS Marketplace</font>

---

**Q: How is asset management on AWS easier than in a physical data center?**

<font color=OrangeRed>User can gather asset metadata reliably with a few API calls</font>

---

**Q: Which AWS program can help an organization to design, build, and manage their workloads on AWS?**

<font color=OrangeRed>APN Consulting Partners</font>

---

**Q: A customer would like to design and build a new workload on AWS Cloud but does not have the AWS-related software technical expertise in-house. Which of the following AWS programs can a customer take advantage of to achieve that outcome?**

<font color=OrangeRed>AWS Partner Network Consulting Partners</font>

---

**Q: What AWS team assists customers with accelerating cloud adoption through paid engagements in any of several specialty practice areas?**

<font color=OrangeRed>AWS Professional Services</font>

---

**Q: A company is migrating from on-premises data centers to the AWS Cloud and is looking for hands-on help with the project. How can the company get this support? (Choose two.)**

- Ask for a quote from the AWS Marketplace team - INCORRECT
- Contact AWS Support and open a case for assistance - INCORRECT
- <font color=OrangeRed>Use AWS Professional Services to provide guidance and to set up an AWS Landing Zone in the company's AWS account</font>
- <font color=OrangeRed>Select a partner from the AWS Partner Network (APN) to assist with the migration</font>
- Use Amazon Connect - INCORRECT

---

**Q: Which of the following guidelines should be followed if an AWS account is compromised?**

<font color=OrangeRed>Respond to AWS through the AWS Support Center.</font>
<font color=OrangeRed>Change the AWS account root password.</font>
<font color=OrangeRed>Rotate and delete all API access keys.</font>
<font color=OrangeRed>Delete any resources that you do not remember creating.</font>
<font color=OrangeRed>Change all IAM user passwords.</font>

---

**Q: Where should users report that AWS resources are being used for malicious purposes?**

<font color=OrangeRed>AWS Abuse Team</font>

---

**Q: With AWS services, you can use as many resources as you need, as well as use them when you need them. Which of the following terms can be applied to this concept?**

<font color=OrangeRed>Temporary resources</font>
<font color=OrangeRed>Disposable resources</font>

---

**Q: John wants to build highly available infrastructure. He needs to make sure that even if one data-center goes down, it should not affect his application. Which component in AWS cloud can he use?**

<font color=OrangeRed>Availability Zones</font>

---

**Q: A company has an application with users in both Australia and Germany. All the company infrastructure is currently provisioned in the Europe (Frankfurt) Region, and Australian users are experiencing high latency. What should the company do to reduce latency?**

<font color=OrangeRed>The easiest option is to place resources closer to where the users are.</font>

---

**Q: Which AWS services should be used for read/write of constantly changing data?**

<font color=OrangeRed>RDS</font> or <font color=OrangeRed>AWS EFS</font>

---

**Q: A purchasing department staff member needs access to an application running on EC2 in the company's accounts payable AWS account to reconcile reports each month-end. Which of the following provides the most secure and operationally efficient way to give the staff member access?**

<font color=OrangeRed>Have the user request temporary security credentials for the application by assuming a role</font>

---

**Q: A company wants to migrate its applications to a VPC on AWS. These applications will need to access on-premises resources. What combination of actions will enable the company to accomplish this goal? (Choose two.)**

<font color=OrangeRed>Build a VPN connection between an on-premises device and a virtual private gateway in the new VPC</font>
<font color=OrangeRed>Connect the company's on-premises data center to AWS using AWS Direct Connect</font>

---

**Q: What are the benefits of developing and running a new application in the AWS Cloud compared to on-premises? (Choose two.)**

- AWS automatically distributes the data globally for higher durability (INCORRECT)
- AWS will take care of operating the application (INCORRECT)
- <font color=OrangeRed>AWS makes it easy to architect for high availability</font>
- <font color=OrangeRed>AWS can easily accommodate application demand changes</font>
- AWS takes care of application security patching (INCORRECT)

---

**Q: How does AWS charge for AWS Lambda usage once the free tier has been exceeded? (Choose two.)**

<font color=OrangeRed>By the time it takes for the Lambda function to execute</font>
<font color=OrangeRed>By the number of requests made for a given Lambda function.</font>

---

**Q: Which disaster recovery scenario offers the lowest probability of downtime?**

<font color=OrangeRed>Multi-site active-active</font>

---

**Q: Which disaster recovery option below has the highest downtime?**

> Backup and restore

---

**Q: Small Corp is planning to create a disaster recovery strategy for their workloads in AWS. Which among these is a good DR strategy for the worst case scenario?**

<font color=OrangeRed>AWS Regions.</font>

---

## Services: Free vs. Charged

<font color="#7f0080">Free to use:</font>

- <font color="#7f0080">Identity and Access Management (IAM)</font>
- <font color="#7f0080">Virtual Private Cloud (VPC)</font>
- <font color="#7f0080">Auto-Scaling</font>
- <font color="#7f0080">Elastic Beanstalk</font>
- <font color="#7f0080">CloudFormation</font>
- Consolidated Billing

**Not free:**
- EC2, RDS, EBS, Route53, S3

**Q: For which services does Amazon NOT charge? (choose 2)**

<font color=OrangeRed>Amazon VPC</font> and <font color=OrangeRed>CloudFormation</font> are free of charge. However, in the case of CloudFormation, you pay for the resources it creates.

**Q: Which AWS services are truly free?**

<font color=OrangeRed>Amazon VPC, Elastic Beanstalk, Cloud Formation, IAM, Auto Scaling, Consolidated Billing</font>

---

**Q: Which AWS services are global?**

<font color=OrangeRed>IAM, Route53, CloudFront, SNS, SES</font>

---

**Q: EC2 Reserved Instances that support reserved pricing?**

<font color=OrangeRed>EC2, RDS, Redshift, and Elasticsearch</font>

Amazon SNS is the only one that does not have reserved pricing.

---

**Q: Which of the following are advantages of using AWS?**

<font color=OrangeRed>No guess needed</font> (regarding capacity)

---

**Q: Which of the following is a benefit of using the AWS Cloud?**

<font color=OrangeRed>Focus on revenue-generating activity.</font>

---

**Q: How can an IT department move quickly to provision resources it needs?**

<font color=OrangeRed>Ability to programmatically provision existing resources</font>

---

**Q: Which disaster recovery option has the highest downtime?**

<font color=OrangeRed>Backup and restore</font>

---

**Q: You need an AWS support plan for your production workloads, but want to keep costs to a minimum. Which of the following plans should you choose?**

**Developer** (lowest cost plan for production)
