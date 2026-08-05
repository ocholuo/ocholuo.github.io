---
title: "Meow's AWS - SAA Exam Practice Q&A"
date: 2026-05-24 11:11:11 -0400
categories: [01Cloud, 01AWS]
tags: [AWS, SAA, exam, practice]
math: false
toc: true
image:
---

# AWS Solutions Architect Associate — Exam Practice Q&A

---

## Overview

This note consolidates exam practice questions and answers for the AWS Solutions Architect Associate (SAA) certification. Questions are grouped by AWS topic. Color coding mirrors the original study notes: correct answers appear in red, explanations in blue, and exam-critical tips in bold.

---

## SQS / SNS / Messaging

**SQS Key Attributes**

> **VisibilityTimeout** — When a consumer instance retrieves a message, that message will be hidden from other consumer instances for a fixed period.

> **DelaySeconds** — When a new message is added to the SQS queue, it will be hidden from consumer instances for a fixed period.

> **WaitTimeSeconds / ReceiveMessageWaitTime** — When the consumer instance polls for new work, the SQS service will allow it to <font color=OrangeRed>wait a certain time for one or more messages to be available</font> before closing the connection.

<font color="blue">SQS: decouple and scale micro-services, distributed systems, and server-less applications.</font>

**Maximum VisibilityTimeout of an SQS message in a FIFO queue?**

> **12 hours**

---

**Q5. A company has a legacy application that processes data in two parts. The second part takes longer. The company rewrites it as two microservices running on ECS that can scale independently. How should the microservices be integrated?**

- A. Implement code in microservice 1 to send data to an S3 bucket. Use S3 event notifications to invoke microservice 2.
- B. Implement code in microservice 1 to publish data to an SNS topic. Implement code in microservice 2 to subscribe to this topic.
- C. Implement code in microservice 1 to send data to Amazon Kinesis Data Firehose. Implement code in microservice 2 to read from Kinesis Data Firehose.
- <font color=OrangeRed>D. Implement code in microservice 1 to send data to an SQS queue. Implement code in microservice 2 to process messages from the queue. (correct)</font>

<font color="blue">SQS is a fully managed queuing service that enables you to decouple and scale micro-services, distributed systems, and server-less applications.</font>

---

**Q36. A solutions architect is designing a two-step order process. Orders must be processed exactly once and in the order in which they are received. How should the components be integrated?**

- <font color=OrangeRed>A. Use SQS FIFO queues. (correct)</font>
- B. Use an AWS Lambda function along with <font color="#ad8456">SQS standard</font> queues.
- C. Create an SNS topic and subscribe an SQS FIFO queue to that topic.
- D. Create an SNS topic and subscribe an <font color="#ad8456">SQS Standard</font> queue to that topic.

---

**Q172. A company is designing a web application that processes insurance quotes. Quotes must be separated by quote type, responded to within 24 hours, and must not be lost. The solution should be simple to set up and maintain.**

- A. Create multiple Amazon Kinesis data streams based on the quote type.
- B. Create <font color="#ad8456">multiple SNS topics</font> and register SQS queues to their own SNS topic.
- <font color=OrangeRed>C. Create a single SNS topic and subscribe the SQS queues to the SNS topic. Configure SNS message filtering to publish messages to the proper SQS queue based on the quote type. Configure each backend application server to work its own SQS queue. (correct)</font>
- D. Create multiple Amazon Kinesis Data Firehose delivery streams based on the quote type to deliver data streams to an Amazon Elasticsearch Service cluster.

---

**Q175. A company's operations team has an existing S3 bucket configured to notify an SQS queue when new objects are created. The development team also wants to receive events when new objects are created. The existing operations team workflow must remain intact. Which solution satisfies these requirements?**

- A. Create another SQS queue. Update the S3 events in the bucket to also update the new queue.
- B. Create a new SQS queue that only allows S3 access. Update S3 to update this queue when a new object is created.
- C. Create an SNS topic and SQS queue for the bucket updates. Update queues to poll SNS.
- <font color=OrangeRed>D. Create an SNS topic and SQS queue for the bucket updates. Update the bucket to send events to the new topic. Add subscription for both queues in the topic. (correct)</font>

<font color="blue">Fan-out pattern: SNS driving two SQS queues.</font>

---

**SQS Standard Queue design concerns:**

> **The order that messages are processed is loosely sequential, but this cannot be relied on.**

> If a message creating system restarts a queue or reprocesses a log, duplicate messages may be generated, sent to SQS, and processed.

---

**Q (SQS facts). Which of the following are true about Amazon SQS?**

> **Data transfer cost between Amazon SQS and Amazon EC2 or AWS Lambda within a single region is free.**

> **Amazon SQS stores all messages and message queues within a <font color=OrangeRed>single highly-available AWS region</font> with multiple redundant Availability Zones.**

---

**SQS WaitTimeSeconds — cost-reduction design change:**

> When the consumer instance polls for new work, the SQS service will allow it to wait a certain time for one or more messages to be available before closing the connection.

---

**SQS with Auto Scaling — appropriate metric:**

> **backlog per instance**

---

## S3 / Storage Classes

**S3 Access Control:**

> <font color=OrangeRed>identity policy</font> — attach to an identity who can then access S3.

> <font color=OrangeRed>presigned URL</font> — see assigned S3 objects using the creator's credentials.

> <font color=OrangeRed>bucket policy / Resource policies</font> — control access to entire buckets.

> <font color=OrangeRed>ACL on the bucket or object</font> — control access to individual objects in an S3 bucket.

**no mention of high availability** — hence S3 One Zone-Infrequent Access is the cheapest option.

---

**Q19. A company is planning to migrate a business-critical dataset to S3. The disaster recovery policy states that all data must reside in multiple AWS Regions.**

- A. Create an additional S3 bucket in another Region and configure cross-Region replication.
- B. Create an additional S3 bucket in another Region and configure cross-origin resource sharing (CORS).
- <font color=OrangeRed>C. Create an additional S3 bucket with versioning in another Region and configure cross-Region replication. (correct)</font>
- D. Create an additional S3 bucket with versioning in another Region and configure cross-origin resource sharing (CORS).

---

**Q34. A solutions architect wants to back up application log data to S3. Unsure how frequently the logs will be accessed or which logs will be accessed the most. The company wants to keep costs as low as possible.**

- A. S3 Glacier
- <font color=OrangeRed>B. S3 Intelligent-Tiering (correct)</font>
- C. S3 Standard-Infrequent Access (S3 Standard-IA)
- D. S3 One Zone-Infrequent Access (S3 One Zone-IA)

---

**Q50. A data science team requires storage for nightly log processing. The size and number of logs is unknown and will persist for 24 hours only. What is the MOST cost-effective solution?**

- A. Amazon S3 Glacier (min of 90 days)
- <font color=OrangeRed>B. Amazon S3 Standard (correct)</font>
- C. Amazon S3 Intelligent-Tiering
- D. Amazon S3 One Zone-IA (min of 30 days)

---

**Q57. A solutions architect is implementing a document review application using an S3 bucket for storage. The solution must prevent accidental deletion of the documents and ensure all versions are available. Which combination of actions should be taken? (Choose two.)**

- A. Enable a read-only bucket ACL.
- <font color=OrangeRed>B. Enable versioning on the bucket. (correct)</font>
- C. Attach an IAM policy to the bucket.
- <font color=OrangeRed>D. Enable MFA Delete on the bucket. (correct)</font>
- E. Encrypt the bucket using AWS KMS.

---

**Q86. A healthcare company stores highly sensitive patient records. Compliance requires multiple copies in different locations. Records must be stored for 7 years. The company must provide records immediately for the first 30 days and then within 4 hours thereafter.**

- <font color=OrangeRed>A. Use S3 with cross-Region replication enabled. After 30 days, transition the data to S3 Glacier using a lifecycle policy. (correct)</font>
- B. Use S3 with cross-origin resource sharing (CORS) enabled. After 30 days, transition to S3 Glacier.
- C. Use S3 with cross-Region replication enabled. After 30 days, transition to <font color="#ad8456">S3 Glacier Deep Archive</font>.
- D. Use S3 with CORS enabled. After 30 days, transition to <font color="#ad8456">S3 Glacier Deep Archive</font>.

<font color="blue">S3 Glacier Deep Archive has a retrieval time of 12 hours, not 4 hours.</font>

---

**Q97. A web application allows users to purchase access to premium S3 content. Upon payment, content will be available for download for 14 days before the user is denied access. Which is the LEAST complicated implementation?**

- A. Use a CloudFront distribution with an OAI. Configure signed URLs. Design a Lambda function to remove data older than 14 days.
- B. Use an S3 bucket and provide direct access. Track purchases in DynamoDB. Configure a Lambda function to remove data older than 14 days.
- <font color=OrangeRed>C. Use a CloudFront distribution with an OAI. Configure the distribution with an S3 origin to provide access through signed URLs. Design the application to set an expiration of 14 days for the URL. (correct)</font>
- D. Use a CloudFront distribution with an OAI. Configure signed URLs. Design the application to set an expiration of <font color="#ad8456">60 minutes</font> for the URL and recreate the URL as necessary.

---

**Q102. A company must migrate 20 TB of data from a data center to the AWS Cloud within 30 days. The company's network bandwidth is limited to 15 Mbps and cannot exceed 70% utilization.**

- <font color=OrangeRed>A. Use AWS Snowball. (correct)</font>
- B. Use AWS <font color="#ad8456">DataSync</font>.
- C. Use a secure VPN connection.
- D. Use Amazon S3 Transfer Acceleration.

<font color="blue">15 Mbps connection at 70% utilization will take months to transfer 20 TB data.</font>

---

**Q105. A company has an on-premises data center that is running out of storage capacity. The company wants to migrate storage to AWS while minimizing bandwidth costs. The solution must allow for immediate retrieval of data at no additional cost.**

- A. Deploy S3 <font color="#ad8456">Glacier Vault</font> and enable expedited retrieval. Enable provisioned retrieval capacity.
- <font color=OrangeRed>B. Deploy AWS Storage Gateway using cached volumes. Use Storage Gateway to store data in S3 while retaining copies of frequently accessed data subsets locally. (correct)</font>
- C. Deploy AWS Storage Gateway using <font color="#ad8456">stored volumes</font> to store data locally. Use Storage Gateway to asynchronously back up snapshots.
- D. Deploy <font color="#ad8456">AWS Direct Connect</font> to connect with the on-premises data center. Configure Storage Gateway.

---

**Q106. A company is processing data on a daily basis. Results are analyzed daily for one week and must remain immediately accessible for occasional analysis. What is the MOST cost-effective storage solution?**

- A. Configure a lifecycle policy to <font color="#ad8456">delete</font> the objects after 30 days.
- B. Configure a lifecycle policy to transition to S3 <font color="#ad8456">Glacier</font> after 30 days.
- C. Configure a lifecycle policy to transition to <font color=OrangeRed>S3 Standard-Infrequent Access (S3 Standard-IA)</font> after 30 days.
- D. Configure a lifecycle policy to transition to <font color="#ad8456">S3 One Zone-Infrequent Access (S3 One Zone-IA)</font> after 30 days.

**<font color=OrangeRed>no mention of high availability</font>** — hence S3 One Zone-Infrequent Access is the cheapest option.

---

**Q107. A company delivers files in S3 to certain users who do not have AWS credentials. These users must be given access for a limited time.**

- A. Enable <font color="#ad8456">public access</font> on an Amazon S3 bucket.
- <font color=OrangeRed>B. Generate a presigned URL to share with the users. (correct)</font>
- C. Encrypt files using AWS KMS and provide keys to the users.
- D. Create and assign <font color="#ad8456">IAM roles</font> that will grant GetObject permissions to the users.

---

**Q130. A company hosts its website on S3. The website serves petabytes of outbound traffic monthly, which accounts for most of the company's AWS costs. How to reduce costs?**

- <font color=OrangeRed>A. Configure CloudFront with the existing website as the origin. (correct)</font>
- B. Move the website to EC2 with EBS volumes for storage.
- C. Use AWS Global Accelerator and specify the existing website as the endpoint.
- D. Rearchitect the website to run on a combination of API Gateway and AWS Lambda.

---

**Q134. An application is running on EC2 instances. Sensitive information is stored in an S3 bucket. The bucket needs to be protected from internet access while only allowing services within the VPC access. (Choose two.)**

- <font color=OrangeRed>A. Create a VPC endpoint for S3. (correct)</font>
- B. Enable server access logging on the bucket.
- <font color=OrangeRed>C. Apply a bucket policy to restrict access to the S3 endpoint. (correct)</font>
- D. Add an <font color="#ad8456">S3 ACL</font> to the bucket.
- E. Restrict <font color="#ad8456">users</font> using the IAM policy to use the specific bucket.

---

**Q164. A company mandates that an S3 gateway endpoint must allow traffic to trusted buckets only. Which method should a solutions architect implement?**

- A. Create a bucket policy for each trusted S3 bucket that allows traffic only from the company's trusted VPCs.
- B. Create a bucket policy for each trusted S3 bucket that allows traffic only from the company's S3 gateway endpoint IDs.
- C. Create an S3 endpoint policy for each S3 gateway endpoint that blocks access from any VPC other than the company's trusted VPCs.
- <font color=OrangeRed>D. Create an S3 endpoint policy for each S3 gateway endpoint that provides access to the Amazon Resource Name (ARN) of the trusted S3 buckets. (correct)</font>

---

**Q170. A solutions architect is tasked with identifying all open S3 buckets and recording any S3 bucket configuration changes.**

- <font color=OrangeRed>A. Enable AWS Config service with the appropriate rules. (correct)</font>
- B. Enable AWS Trusted Advisor with the appropriate checks.
- C. Write a script using an AWS SDK to generate a bucket report.
- D. Enable <font color="#ad8456">S3 server access logging</font> and configure CloudWatch Events.

<font color="blue">Server access logging is for logging all requests that are made to an S3 bucket — not for detecting open bucket configurations.</font>

---

**Q177. A solutions architect is designing a cloud architecture for a new application. Users can interactively download and upload files. Files older than 2 years will be accessed less frequently. (Choose two.)**

- <font color=OrangeRed>A. Store the files on S3 with a lifecycle policy that moves objects older than 2 years to S3 Glacier. (correct)</font>
- <font color=OrangeRed>B. Store the files on S3 with a lifecycle policy that moves objects older than 2 years to S3 Standard-Infrequent Access (S3 Standard-IA). (correct)</font>
- C. Store the files on Amazon EFS with a lifecycle policy that moves objects older than 2 years to <font color="#ad8456">EFS Infrequent Access (EFS IA)</font>.
- D. Store the files in Amazon EBS volumes. Schedule snapshots. Use the snapshots to archive data older than 2 years.
- E. Store the files in RAID-striped EBS volumes. Schedule snapshots.

---

**S3 multipart upload benefits:**

> Delivers quick recovery from network issues.

> Delivers improved throughput.

> <font color=OrangeRed>Delivers the ability to begin an upload before you know the final object size.</font>

> <font color=OrangeRed>Delivers the ability to pause and resume object uploads.</font>

---

**S3 PUT rate limit note:**

**Until 2018 there was a hard limit on S3 PUTs of 100 PUTs per second. As of July 2018 the limit was raised to 3500. Change trigger level to around 3000.**

---

**CloudFront access control for private S3 content:**

> **CloudFront Origin Access Identity** — virtual user identity that gives the CloudFront distribution permission to fetch a private object from an S3 bucket.

> **CloudFront Signed URLs** — authorize users attempting to access files in an S3 bucket.

> **CloudFront Signed Cookies** — authorize users attempting to access files in an S3 bucket.

---

## EC2 / Auto Scaling / Load Balancers

**Q4. A company's web application uses multiple Linux EC2 instances and stores data on EBS volumes. The company is looking for a solution to increase the resiliency and provide storage that complies with ACID.**

- A. Launch the application on EC2 instances in each AZ. Attach EBS volumes to each EC2 instance.
- B. Create an ALB with Auto Scaling groups across multiple AZs. Mount an <font color="#ad8456">instance store</font> on each EC2 instance.
- <font color=OrangeRed>C. Create an ALB with Auto Scaling groups across multiple AZs. Store data on EFS and mount a target on each instance. (correct)</font>
- D. Create an ALB with Auto Scaling groups across multiple AZs. Store data using <font color="#ad8456">S3 One Zone-IA</font>.

---

**Q30. A gaming company has multiple EC2 instances in a single AZ for its multiplayer game that communicates with users on Layer 4. The CTO wants a highly available and cost-effective architecture. (Choose two.)**

- A. Increase the number of EC2 instances.
- B. Decrease the number of EC2 instances.
- <font color=OrangeRed>C. Configure a Network Load Balancer in front of the EC2 instances. (correct)</font>
- D. Configure an Application Load Balancer in front of the EC2 instances.
- <font color=OrangeRed>E. Configure an Auto Scaling group to add or remove instances in multiple Availability Zones automatically. (correct)</font>

---

**Q42. A company hosts a static website on-premises and wants to migrate to AWS. The website should load as quickly as possible for users around the world. The company also wants the most cost-effective solution.**

- A. Copy content to an S3 bucket. Configure the bucket to serve static content. Replicate the S3 bucket to multiple AWS Regions.
- <font color=OrangeRed>B. Copy the website content to an S3 bucket. Configure the bucket to serve static content. Configure CloudFront with the S3 bucket as the origin. (correct)</font>
- C. Copy content to an EBS-backed EC2 instance running Apache HTTP Server. Configure Route 53 geolocation routing.
- D. Copy content to multiple EBS-backed EC2 instances in multiple Regions. Configure CloudFront geolocation routing.

---

**Q46. A company's production application runs OLTP transactions on an RDS MySQL DB instance. A new reporting tool will access the same data. It must be highly available and not impact the performance of the production application.**

- A. Create <font color="#ad8456">hourly snapshots</font> of the production RDS DB instance.
- <font color=OrangeRed>B. Create a Multi-AZ RDS Read Replica of the production RDS DB instance. (correct)</font>
- C. Create multiple RDS Read Replicas of the production RDS DB instance. Place the Read Replicas in an Auto Scaling group.
- D. Create a <font color="#ad8456">Single-AZ</font> RDS Read Replica of the production RDS DB instance. Create a second Single-AZ RDS Read Replica from the replica.

---

**Q51. A company is hosting a web application on AWS using a single EC2 instance that stores user-uploaded documents in an EBS volume. The company duplicated the architecture and created a second EC2 instance and EBS volume in another AZ, placing both behind an ALB. After this change, users reported they could see one subset of their documents or the other, but never all at once. How to ensure users see all documents at once?**

- A. Copy the data so both EBS volumes contain all the documents.
- B. Configure the ALB to direct a user to the server with the documents.
- <font color=OrangeRed>C. Copy the data from both EBS volumes to EFS. Modify the application to save new documents to EFS. (correct)</font>
- D. Configure the ALB to send the request to both servers. Return each document from the correct server.

---

**Q77. A solutions architect is designing a web application that will run on EC2 instances behind an ALB. The company requires the application be resilient against malicious internet activity and attacks, and protect against new common vulnerabilities and exposures.**

- A. Leverage Amazon CloudFront with the ALB endpoint as the origin.
- <font color=OrangeRed>B. Deploy an appropriate managed rule for AWS WAF and associate it with the ALB. (correct)</font>
- C. Subscribe to <font color="#ad8456">AWS Shield Advanced</font> and ensure common vulnerabilities and exposures are blocked.
- D. Configure network ACLs and security groups to allow only ports 80 and 443 to access the EC2 instances.

---

**Q83. A company built an application that lets users check in to places. The single RDS for MySQL instance has triggered alarms related to resource exhaustion due to read requests. To prevent service interruptions at the database layer with minimal changes to code?**

- <font color=OrangeRed>A. Create RDS read replicas and redirect read-only traffic to the read replica endpoints. Enable a Multi-AZ deployment. (correct)</font>
- B. Create an EMR cluster and migrate the data to HDFS with a replication factor of 3.
- C. Create an ElastiCache cluster and redirect all read-only traffic to the cluster.
- D. Create a <font color="#ad8456">DynamoDB</font> table to replace the RDS instance.

---

**Q85. A company has created a VPC with multiple private subnets in multiple AZs and one public subnet in one AZ. There is a NAT gateway in the public subnet. In case of an AZ failure, the company wants to ensure instances are not all experiencing internet connectivity issues. Which solution is MOST highly available?**

- A. Create a new public subnet with a NAT gateway in <font color="#ad8456">the same AZ</font>. Distribute traffic between the two NAT gateways.
- B. Create an EC2 NAT instance in a <font color="#ad8456">not public</font> subnet. Distribute traffic between the NAT gateway and the NAT instance.
- <font color=OrangeRed>C. Create public subnets in each AZ and launch a NAT gateway in each subnet. Configure the traffic from private subnets in each AZ to the respective NAT gateway. (correct)</font>
- D. Create an EC2 NAT instance in the <font color="#ad8456">same public</font> subnet. Replace the NAT gateway with the NAT instance and associate with an Auto Scaling group.

---

**Q90. A public-facing web application queries a database hosted on an EC2 instance in a private subnet. A large number of queries involve multiple table joins and performance has been degrading. (Choose two.)**

- A. Cache query data in SQS.
- <font color=OrangeRed>B. Create a read replica to offload queries. (correct)</font>
- C. Migrate the database to <font color="#ad8456">Athena</font>.
- D. Implement DynamoDB Accelerator to cache data.
- <font color=OrangeRed>E. Migrate the database to RDS. (correct)</font>

---

**Q94. An application requires a DEV and PROD environment for several years. The DEV instances will run for 10 hours each day during normal business hours, while the PROD instances will run 24 hours each day. Which solution is MOST cost-effective?**

- A. DEV with Spot Instances and PROD with On-Demand Instances.
- B. DEV with On-Demand Instances and PROD with Spot Instances.
- <font color=OrangeRed>C. DEV with Scheduled Reserved Instances and PROD with Reserved Instances. (correct)</font>
- D. DEV with On-Demand Instances and PROD with Scheduled Reserved Instances.

---

**Q95. A company runs multiple EC2 Linux instances in a VPC with applications that use a hierarchical directory structure. The applications need to rapidly and concurrently read and write to shared storage.**

- <font color=OrangeRed>A. Create an EFS file system and mount it from each EC2 instance. (correct)</font>
- B. Create an S3 bucket and permit access from all the EC2 instances in the VPC.
- C. Create a file system on an EBS Provisioned IOPS SSD (io1) volume. Attach the volume to all the EC2 instances.
- D. Create file systems on EBS volumes attached to each EC2 instance. Synchronize the EBS volumes.

---

**Q96. A solutions architect observes that a nightly batch processing job is automatically scaled up for 1 hour before the desired EC2 capacity is reached. The peak capacity is the same every night and batch jobs always start at 1 AM. How to meet requirements?**

- A. Increase the minimum capacity for the Auto Scaling group.
- B. Increase the maximum capacity for the Auto Scaling group.
- <font color=OrangeRed>C. Configure scheduled scaling to scale up to the desired compute level. (correct)</font>
- D. Change the scaling policy to <font color="#ad8456">add more EC2 instances</font> during each scaling operation.

---

**Q103. A company has a website running on EC2 instances across 2 AZs. The company is expecting spikes in traffic on specific holidays and wants to provide a consistent user experience.**

- A. Use step scaling.
- B. Use simple scaling.
- C. Use lifecycle hooks.
- <font color=OrangeRed>D. Use scheduled scaling. (correct)</font>

---

**Q138. A company relies on an application that needs at least 4 EC2 instances during regular traffic and must scale up to 12 EC2 instances during peak loads. The application must be highly available.**

- A. Deploy the EC2 instances in an Auto Scaling group. Set minimum to 4 and maximum to 12, <font color="#ad8456">with 2 in AZ A and 2 in AZ B</font>. (not HA — if one AZ fails, only 2 remain)
- B. Deploy the EC2 instances in an Auto Scaling group. Set minimum to 4 and maximum to 12, <font color="#ad8456">with all 4 in AZ A</font>.
- <font color=OrangeRed>C. Deploy the EC2 instances in an Auto Scaling group. Set minimum to 8 and maximum to 12, with 4 in Availability Zone A and 4 in Availability Zone B. (correct)</font>
- D. Deploy the EC2 instances in an Auto Scaling group. Set minimum to 8 and maximum to 12 with <font color="#ad8456">all 8 in Availability Zone A</font>.

---

**Q140. A solutions architect is designing an architecture for a new application that requires low network latency and high network throughput between EC2 instances. Which component should be included?**

- A. An Auto Scaling group with Spot Instance types.
- <font color=OrangeRed>B. A placement group using a cluster placement strategy. (correct)</font>
- C. A placement group using a partition placement strategy.
- D. An Auto Scaling group with On-Demand instance types.

---

**Q149. A monolithic application was recently migrated to AWS and is now running on a single EC2 instance. It is not possible to use automatic scaling to scale out the application. The CTO wants an automated solution to restore the EC2 instance in the unlikely event the underlying hardware fails.**

- <font color=OrangeRed>A. Configure a CloudWatch alarm that triggers the recovery of the EC2 instance if it becomes impaired. (correct)</font>
- B. Configure a CloudWatch alarm to trigger an SNS message that alerts the CTO.
- C. Configure AWS CloudTrail to monitor the health of the EC2 instance.
- D. Configure an Amazon EventBridge event to trigger an AWS Lambda function once an hour that checks the health of the EC2 instance.

---

**Q152. A company runs an application on EC2 instances in private subnets in 3 AZs of the us-east-1 Region. The instances must be able to connect to the internet to download files. The company wants a design that is highly available across the Region.**

- A. Deploy a NAT Instance in a private subnet of each Availability Zone.
- <font color=OrangeRed>B. Deploy a NAT gateway in a public subnet of each Availability Zone. (correct)</font>
- C. Deploy a transit gateway in a private subnet of each Availability Zone.
- D. Deploy an <font color="#ad8456">internet gateway</font> in a public subnet of each Availability Zone.

---

**Q159. A company is planning to migrate its virtual server-based workloads to AWS. The application servers rely on patches from an internet-hosted repository. Which services should be hosted on the public subnet? (Choose two.)**

- <font color=OrangeRed>A. NAT gateway (correct)</font>
- B. <font color="#ad8456">RDS</font> DB instances
- <font color=OrangeRed>C. Application Load Balancers (correct)</font>
- D. EC2 application servers
- E. Amazon EFS volumes

---

**Q169. A company runs a web service on EC2 instances behind an ALB in an EC2 Auto Scaling group across two Availability Zones. The company needs a minimum of four instances at all times. If an AZ fails, how can the company remain compliant with the SLA?**

- A. Add a target tracking scaling policy with a short cooldown period.
- B. Change the Auto Scaling group launch configuration to use a larger instance type.
- C. Change the Auto Scaling group to use six servers across three Availability Zones.
- <font color=OrangeRed>D. Change the Auto Scaling group to use eight servers across two Availability Zones. (correct)</font>

---

**Q171. A company is planning to build a new web application on AWS. The company expects predictable traffic most of the year and very high traffic on occasion. The web application needs to be highly available and fault tolerant with minimal latency.**

- A. Use a Route 53 routing policy to distribute requests to two AWS Regions, each with one EC2 instance.
- <font color=OrangeRed>B. Use EC2 instances in an Auto Scaling group with an Application Load Balancer across multiple Availability Zones. (correct)</font>
- C. Use EC2 instances in a cluster placement group with an ALB across multiple Availability Zones.
- D. Use EC2 instances in a cluster placement group and include the cluster placement group within a new Auto Scaling group.

---

**Q181. A company is hosting multiple websites. Users are routed to appropriate backend EC2 instances based on the subdomain. The websites host static webpages, images, and server-side scripts. Some websites experience peak access during the first two hours of business. A solutions architect needs to automatically adjust capacity. (Choose two.)**

- A. AWS Batch
- B. Network Load Balancer
- <font color=OrangeRed>C. Application Load Balancer (correct)</font>
- <font color=OrangeRed>D. EC2 Auto Scaling (correct)</font>
- E. Amazon S3 website hosting (static content only)

---

**Q232. A customer is running a critical payroll system in production and a DR environment in another data center. The DR process is manual and error-prone. How should a Solutions Architect migrate the system to AWS?**

- A. Migrate the production and DR environments to different AZs within the same region. Let AWS manage failover.
- B. Migrate the production and DR environments to different regions. Let AWS manage failover.
- C. Migrate the production environment to a <font color="#ad8456">single Availability Zone</font>, and set up instance recovery for EC2. Decommission the DR environment.
- <font color=OrangeRed>D. Migrate the production environment to span multiple Availability Zones, using Elastic Load Balancing and Multi-AZ Amazon RDS. Decommission the DR environment. (correct)</font>

---

**Q253. A company is running a series of national TV campaigns. The company expects traffic to increase from five requests each minute to more than 5,000 requests each minute. Which AWS service to ensure traffic surges can be handled?**

- A. AWS Lambda
- B. Amazon ElastiCache
- C. <font color="#ad8456">Size EC2 instances</font> to handle peak load
- <font color=OrangeRed>D. An Auto Scaling group for EC2 instances (correct)</font>

---

**Q267. Which factors determine the health check grace period? (Select TWO.)**

- A. How frequently the Auto Scaling group scales up or down. (consequence of grace period)
- B. How many Amazon CloudWatch alarms are configured for status checks.
- <font color=OrangeRed>C. How much of the application code is embedded in the AMI. (correct — influences grace period length)</font>
- D. How long it takes for the Auto Scaling group to detect a failure. (consequence of grace period)
- <font color=OrangeRed>E. How long the bootstrap script takes to run. (correct — influences grace period length)</font>

---

**Q290. A solutions architect is designing an elastic application that will have between 10 and 50 EC2 concurrent instances running, dependent on load. Each instance must mount storage that will read and write to the same 50 GB folder. Which storage type meets the requirements?**

- A. Amazon S3
- <font color=OrangeRed>B. Amazon EFS (correct)</font>
- C. Amazon EBS volumes
- D. Amazon EC2 instance store

---

**EC2 instance types:**

> **A monolithic application** — runs on Linux or Windows with consistent, long-running compute scenarios — does well on a single EC2 instance.

> **Horizontal scaling is more challenging to set up** than vertical scaling.

**To ensure application can scale as quickly as possible in a cost-effective way:**

> <font color=OrangeRed>Horizontal scaling</font>

> <font color=OrangeRed>Small instances</font> — smaller instances tend to have fewer capacity issues or restrictions; more efficient to use smaller instances.

**Placing instances for maximum throughput between them:**

> Put the instances in a placement group. (6 Gbps throughput requirement)

**Spread Placement Group:**

> Recommended for applications that have a small number of critical instances which need to be kept separate from each other.

> Reduces the risk of simultaneous failures that might occur when instances share the same underlying hardware.

---

**EC2 Enhanced Networking:**

> Allows high-performance networking by bypassing the need for CPU involvement in virtualizing a network interface.

> Increases packets per second and decreases the variability in network performance.

**Use spot instances** for video transcoding workloads to significantly reduce ongoing costs.

---

**NAT Instance:**

> **Ensure that "Source/Destination Checks" is disabled on the NAT instance.**

---

**EC2 metadata URL:**

> `http://169.254.169.254/latest/user-data/`

---

**Load balancer types:**

> **Network Load Balancer in a public subnet** — provides a static IP address; handles tens of millions of requests per second at ultra low latency.

> ALB — for HTTP/HTTPS, XSS protection via WAF, routing based on subdomain.

**EC2 health check:**

> If the load balancer is not sending traffic to one of the EC2 instances, the EC2 instance has failed the load balancer health check.

---

**Auto Scaling with known traffic patterns:**

> **Use a predictive scaling policy** for known recurring spikes (e.g., stock market opening/closing).

---

## RDS / Aurora / DynamoDB

**Q9. An application running on AWS uses an Aurora Multi-AZ deployment. Database reads are causing high I/O and adding latency to write requests. How to separate read requests from write requests?**

- A. Enable read-through caching on the Aurora database.
- B. Update the application to <font color="#ad8456">read from the Multi-AZ standby</font> instance.
- <font color=OrangeRed>C. Create a read replica and modify the application to use the appropriate endpoint. (correct)</font>
- D. <font color="#ad8456">Create a second Aurora database</font> and link it to the primary database as a read replica.

---

**Q14. A popular e-commerce application runs on AWS. The database is running on the RDS Aurora engine on the largest instance size available. How to improve performance?**

- A. Convert the database to Amazon Redshift.
- B. Create a CloudFront distribution. (CF is for content, not DB)
- <font color=OrangeRed>C. Convert the database to use EBS Provisioned IOPS. (queried for write) (correct)</font>
- D. Create one or more read replicas. (Only read)

---

**Q28. A company has been storing analytics data in an RDS instance. The expectation is that the application will experience periods of inactivity but could receive bursts of traffic within seconds. Which solution should the solutions architect suggest?**

- A. Set up an Amazon API Gateway and use ECS.
- B. Set up an Amazon API Gateway and use AWS Elastic Beanstalk.
- <font color=OrangeRed>C. Set up an Amazon API Gateway and use AWS Lambda functions. (correct)</font>
- D. Set up an Amazon API Gateway and use EC2 with Auto Scaling.

<font color="blue">Lambda can be set up to automatically trigger from other AWS services or called directly from any web or mobile app.</font>

---

**Q91. A large multinational company runs a timesheet application on AWS. The application must not be down for more than two hours, and the solution must be as cost-effective as possible. How to meet the CFO's requirements while minimizing data loss?**

- A. In another region, configure a <font color="#ad8456">read replica</font> and create a copy of the infrastructure. When an issue occurs, promote the read replica and configure as an RDS Multi-AZ database instance.
- B. Configure a 1-day window of 60-minute snapshots of the RDS Multi-AZ database instance. Create an AWS CloudFormation template. When an issue occurs, use CloudFormation to create the environment in another region.
- C. Configure a 1-day window of 60-minute snapshots of the RDS Multi-AZ database instance which is copied to another region. Create an AWS CloudFormation template.
- <font color=OrangeRed>D. Configure a read replica in another region. Create an AWS CloudFormation template of the application infrastructure. When an issue occurs, promote the read replica and configure as an RDS Multi-AZ database instance and use the CloudFormation template to create the environment in another region. Update the DNS record to point to the other region's ELB. (correct)</font>

---

**Q98. Designing a mission-critical web application. The database should be highly available and fault tolerant. (Choose two.)**

- A. Amazon Redshift
- B. Amazon DynamoDB
- C. Amazon RDS for MySQL
- <font color=OrangeRed>D. MySQL-compatible Amazon Aurora Multi-AZ (correct)</font>
- <font color=OrangeRed>E. Amazon RDS for SQL Server Standard Edition Multi-AZ (correct)</font>

---

**Q111. A company is investigating potential solutions that would collect, process, and store users' service usage data. The business objective is to create an analytics capability using standard SQL queries. The solution should be highly available and ensure ACID compliance in the data tier.**

- A. Use <font color="#ad8456">DynamoDB</font> transactions.
- B. Create a <font color="#ad8456">Neptune</font> database in a Multi-AZ design.
- <font color=OrangeRed>C. Use a fully managed RDS for MySQL database in a Multi-AZ design. (correct)</font>
- D. Deploy PostgreSQL on an EC2 instance that uses EBS Throughput Optimized HDD storage.

---

**Q119. An ecommerce company has noticed performance degradation of its RDS based web application. The performance degradation is attributed to an increase in read-only SQL queries. How to solve the problem with minimal changes to the existing web application?**

- A. Export the data to <font color="#ad8456">DynamoDB</font> and have the business analysts run their queries.
- B. Load the data into ElastiCache and have the business analysts run their queries.
- <font color=OrangeRed>C. Create a read replica of the primary database and have the business analysts run their queries. (correct)</font>
- D. Copy the data into a Redshift cluster and have the business analysts run their queries.

---

**Q127. A company has a mobile chat application with a data store based in DynamoDB. Users would like new messages to be read with as little latency as possible. A solutions architect needs to design an optimal solution that requires minimal application changes.**

- <font color=OrangeRed>A. Configure Amazon DynamoDB Accelerator (DAX) for the new messages table. Update the code to use the DAX endpoint. (correct)</font>
- B. Add DynamoDB read replicas to handle the increased read load.
- C. Double the number of read capacity units for the new messages table in DynamoDB.
- D. Add an ElastiCache for Redis cache to the application stack.

<font color="blue">DAX is to DynamoDB as ElastiCache is to RDS.</font>

---

**Q128. A mobile app that requires minimal latency. Application beta testing showed there was a slowdown when reading the data. However the EC2 instances do not cross any CPU utilization thresholds.**

- A. Reduce the threshold for CPU utilization in the Auto Scaling group.
- B. Replace the Application Load Balancer with a Network Load Balancer.
- <font color=OrangeRed>C. Add read replicas for the RDS instances and direct read traffic to the replica. (correct)</font>
- D. Add Multi-AZ support to the RDS instances and direct read traffic to the new EC2 instance.

<font color="blue">The DB instance (RDS instance) may have its CPU at 100% while the EC2 instances are fine.</font>

---

**Q148. A company has migrated an on-premises Oracle database to an RDS for Oracle Multi-AZ DB instance in us-east-1. A disaster recovery strategy must provision the database in us-west-2 in a maximum of 2 hours, with a data loss window of no more than 3 hours.**

- <font color=OrangeRed>A. Edit the DB instance and create a read replica in us-west-2. Promote the read replica to master in us-west-2 in case the disaster recovery environment needs to be activated. (correct)</font>
- B. Select the <font color="#ad8456">multi-Region option</font> to provision a standby instance in us-west-2.
- C. Take automated snapshots and copy them to us-west-2 every 3 hours. Restore the latest snapshot in us-west-2.
- D. Create a multimaster read/write instances across multiple AWS Regions.

---

**Q168. A company needs to implement a relational database with a multi-Region disaster recovery RPO of 1 second and an RTO of 1 minute.**

> <font color=OrangeRed>A. Amazon Aurora Global Database (correct)</font>

- B. Amazon <font color="#ad8456">DynamoDB</font> global tables.
- > C. Amazon RDS for MySQL with Multi-AZ enabled.
- D. Amazon RDS for MySQL with a cross-Region snapshot copy.

---

**RDS Read Replicas and Multi-AZ (MariaDB — false statement):**

> <font color=OrangeRed>FALSE: "You cannot combine Read Replicas with Multi-AZ deployments for the MariaDB database engine. Only PostgreSQL, Aurora and Oracle database engines are supported."</font>

<font color="blue">In fact, RDS for MariaDB does support combining Read Replicas with Multi-AZ deployments.</font>

---

**DynamoDB — heavy reads (university enrollment):**

> <font color=OrangeRed>Increase the RCU</font> — most cost effective choice to handle enrollment read load.

**DynamoDB — partition key performance issue:**

> If votes are written with a PK of candidate name (only 3 values), each candidate's partition can support a max of 1,000 WCU. With 5,000 WCU provisioned but only 3 partition key values, only ~3,000 WCU are usable.

**DynamoDB — data consistency across 3 AZs:**

> Code for <font color=OrangeRed>strongly consistent reads</font> — advise the CTO of the increased cost.

**DynamoDB Auto Scaling:**

> **Make sure DynamoDB Auto Scaling is turned on** to handle throttling during peak traffic times.

**DynamoDB performance strategies:**

> Data is stored on Solid State Disks.

> The database is partitioned across a number of nodes.

**DynamoDB use cases:**

> <font color=OrangeRed>Managing web session data</font>

> <font color=OrangeRed>Storing metadata for S3 objects</font>

> High-speed data such as Doppler radar systems (2,000 samples per second)

> Language learning application with 24,000 read units per second and 3,300 write units per second

**ElastiCache — scope:**

> ElastiCache is only a key-value store and cannot store relational data.

> Elasticache for Memcached does not offer native encryption. Elasticache for Redis does.

> ElastiCache can implement: In-Memory Data Store, Pub/Sub, Sorted Sets.

---

**Magento store — database read performance:**

> <font color=OrangeRed>Migrate the database from MySQL to Aurora</font> for better performance, then update the connection string in Magento.

> <font color=OrangeRed>Place the RDS instances behind an ElastiCache instance</font>, then update the connection string in Magento.

<font color="blue">Adding a read replica alone won't solve the problem — you would need to alter the code. Multi-AZ is a reliability technique, not a performance technique.</font>

---

**RDS read contention:**

> <font color=OrangeRed>Add an RDS Read Replica for increased read performance.</font>

> <font color=OrangeRed>Use ElastiCache to cache the frequently read, static data.</font>

> <font color=OrangeRed>Provision a larger instance size with provisioned IOPS.</font>

---

**RDS Provisioned IOPS storage with Microsoft SQL Server — maximum size RDS volume by default:**

> **16 TB**

---

## EBS / EFS / FSx / Storage Gateway

**EFS:**

> Amazon EFS is a regional service storing data within and across multiple Availability Zones (AZs) for high availability and durability.

> Amazon EC2 instances can access the file system across AZs, regions, and VPCs, while on-premises servers can access using AWS Direct Connect or AWS VPN.

> EFS: storage service that provides a simple, scalable, fully managed elastic NFS file system for use with AWS Cloud services and on-premises resources.

---

**Q12. A product team is creating a new application that will store a large amount of data. The data will be analyzed hourly and modified by multiple EC2 Linux instances. The amount of space needed will continue to grow for the next 6 months.**

- A. Store the data in an EBS volume. Mount the EBS volume on the application instances.
- <font color=OrangeRed>B. Store the data in an EFS file system. Mount the file system on the application instances. (correct)</font>
- C. Store the data in S3 <font color="#ad8456">Glacier</font>. Update the vault policy to allow access to the application instances.
- D. Store the data in S3 <font color="#ad8456">Standard-Infrequent Access (S3 Standard-IA)</font>. Update the bucket policy.

---

**Q43. A solutions architect is designing storage for a high performance computing (HPC) environment based on Amazon Linux. The workload stores and processes a large amount of engineering drawings that require shared storage and heavy computing.**

- A. Amazon Elastic File System (Amazon EFS)
- <font color=OrangeRed>B. Amazon FSx for Lustre (correct)</font>
- C. Amazon EC2 <font color="#ad8456">instance store</font>
- D. Amazon <font color="#ad8456">EBS</font> Provisioned IOPS SSD (io1)

---

**Q55. A solutions architect is tasked with transferring 750 TB of data from a network-attached file system located at a branch office to Amazon S3 Glacier. The solution must avoid saturating the branch office's low-bandwidth internet connection.**

- A. Create a site-to-site VPN tunnel to an Amazon S3 bucket and transfer the files directly.
- B. Order 10 AWS Snowball appliances and <font color="#ad8456">select an S3 Glacier vault as the destination</font>.
- C. Mount the network-attached file system to S3 and copy the files directly. Create a lifecycle policy.
- <font color=OrangeRed>D. Order 10 AWS Snowball appliances and select an S3 bucket as the destination. Create a lifecycle policy to transition the S3 objects to Amazon S3 Glacier. (correct)</font>

---

**Q88. A company recently implemented hybrid cloud connectivity using AWS Direct Connect and is migrating data to S3. The company is looking for a fully managed solution that will automate and accelerate the replication of data between the on-premises storage systems and AWS storage services.**

- <font color=OrangeRed>A. Deploy an AWS DataSync agent for the on-premises environment. Configure a sync job to replicate the data and connect it with an AWS service endpoint. (correct)</font>
- B. Deploy an AWS DataSync agent for the on-premises environment. Schedule a batch job to replicate point-in-time snapshots to AWS.
- C. Deploy an AWS Storage Gateway volume gateway for the on-premises environment. Configure it to store data locally, and asynchronously back up point-in-time snapshots to AWS.
- D. Deploy an AWS Storage Gateway file gateway for the on-premises environment.

---

**Q89. A company has 150 TB of archived image data stored on-premises that needs to be moved to the AWS Cloud within the next month. The company's current network connection allows up to 100 Mbps uploads for this purpose during the night only. What is the MOST cost-effective mechanism to move this data and meet the migration deadline?**

- A. Use AWS Snowmobile to ship the data to AWS.
- <font color=OrangeRed>B. Order multiple AWS Snowball devices to ship the data to AWS. (correct)</font>
- C. Enable Amazon S3 Transfer Acceleration and securely upload the data.
- D. Create an Amazon S3 VPC endpoint and establish a VPN to upload the data.

---

**Q108. A company wants to run a hybrid workload for data processing. The data needs to be accessed by on-premises applications for local data processing using an NFS protocol, and must also be accessible from the AWS Cloud for further analytics and batch processing.**

- <font color=OrangeRed>A. Use an AWS Storage Gateway file gateway to provide file storage to AWS, then perform analytics on this data in the AWS Cloud. (correct)</font>
- B. Use an AWS Storage Gateway <font color="#ad8456">tape</font> gateway to copy the backup of the local data to AWS.
- C. Use an AWS Storage Gateway volume gateway in a stored volume configuration.
- D. Use an AWS Storage Gateway volume gateway in a cached volume configuration.

---

**Q115. A recent analysis highlights the need to eliminate the use of physical backup tapes. The company must preserve the existing investment in the on-premises backup applications and workflows.**

- A. Set up AWS Storage Gateway to connect with the backup applications using the NFS interface.
- B. Set up an Amazon <font color="#ad8456">EFS</font> file system that connects with the backup applications using the NFS interface.
- C. Set up an Amazon <font color="#ad8456">EFS</font> file system that connects with the backup applications using the iSCSI interface.
- <font color=OrangeRed>D. Set up AWS Storage Gateway to connect with the backup applications using the iSCSI-virtual tape library (VTL) interface. (correct)</font>

---

**Q118. A company has two applications that need to access the same files at the same time with low latency.**

- A. Configure two AWS Lambda functions to run the applications. Create an EC2 instance with an <font color="#ad8456">instance store volume</font>.
- B. Configure two AWS Lambda functions to run the applications. Create an EC2 instance with an <font color="#ad8456">EBS</font> volume.
- C. Configure one memory optimized EC2 instance to run both applications. Create an <font color="#ad8456">EBS</font> volume with Provisioned IOPS.
- <font color=OrangeRed>D. Configure two Amazon EC2 instances to run both applications. Configure Amazon EFS with General Purpose performance mode and Bursting Throughput mode to store the data. (correct)</font>

<font color="blue">EFS for concurrent access to files. General Purpose is ideal for latency-sensitive use cases.</font>

---

**Q123. A company has several business systems that require access to a file share using the Server Message Block (SMB) protocol. The file share should be accessible from both on-premises and AWS environments. (Choose two.)**

- A. Amazon EBS
- B. Amazon EFS
- <font color=OrangeRed>C. Amazon FSx for Windows (correct)</font>
- D. Amazon S3
- <font color=OrangeRed>E. AWS Storage Gateway file gateway (NFS and SMB) (correct)</font>

---

**Q125. A company has a Microsoft Windows-based application that must be migrated to AWS. The application requires a shared Windows file system attached to multiple Amazon EC2 Windows instances.**

- A. Configure a volume using <font color="#ad8456">EFS</font>. Mount the EFS volume to each Windows Instance.
- B. Configure <font color="#ad8456">AWS Storage Gateway</font> in Volume Gateway mode.
- <font color=OrangeRed>C. Configure Amazon FSx for Windows File Server. Mount the Amazon FSx volume to each Windows Instance. (correct)</font>
- D. Configure an <font color="#ad8456">EBS</font> volume with the required size. Attach each EC2 instance to the volume.

---

**Q132. A media company needs at least 10 TB of storage with the maximum possible I/O performance for video processing, 300 TB of very durable storage for storing media content, and 900 TB of storage to meet requirements for archival media.**

- <font color=OrangeRed>A. EBS for maximum performance, S3 for durable data storage, and S3 Glacier for archival storage. (correct)</font>
- B. EBS for maximum performance, EFS for durable data storage, and S3 Glacier for archival storage.
- C. EC2 <font color="#ad8456">instance store</font> for maximum performance, EFS for durable data storage, and S3 for archival storage.
- D. EC2 instance store for maximum performance, S3 for durable data storage, and S3 Glacier for archival storage.

---

**Q139. A solutions architect must design a solution for a persistent database being migrated from on-premises to AWS. The database requires 64,000 IOPS. If possible, the database administrator wants to use a single EBS volume.**

- A. Use an instance from the I3 I/O optimized family and leverage local ephemeral storage.
- <font color=OrangeRed>B. Create a Nitro-based EC2 instance with an EBS Provisioned IOPS SSD (io1) volume attached. Configure the volume to have 64,000 IOPS. (correct)</font>
- C. Create and map an Amazon EFS volume to the database instance.
- D. Provision two volumes and assign 32,000 IOPS to each.

---

**Q150. A solutions architect is optimizing a legacy document management application running on Windows Server in an on-premises data center. The application stores files on a network file share. How to reduce the on-premises footprint and minimize storage costs?**

- <font color=OrangeRed>A. Set up an AWS Storage Gateway file gateway. (correct)</font>
- B. Set up Amazon EFS.
- C. Set up AWS Storage Gateway as a volume gateway.
- D. Set up an Amazon EBS volume.

---

**Q161. A company is using a tape backup solution. The daily data volume is around 50 TB. The company needs to retain the backups for 7 years. The backups are rarely accessed and a week's notice is typically given if a backup needs to be restored. Which storage solution is MOST cost-effective?**

- A. Use Amazon Storage Gateway to back up to Glacier Deep Archive.
- B. Use AWS <font color="#ad8456">Snowball</font> Edge to directly integrate the backups with S3 Glacier.
- C. <font color="#ad8456">Copy the backup</font> data to S3 and create a lifecycle policy to move the data to S3 Glacier.
- <font color=OrangeRed>D. Use Amazon Storage Gateway to back up to S3 and create a lifecycle policy to move the backup to S3 Glacier. (correct)</font>

---

**Q162. A company requires a durable backup storage solution for its on-premises database servers while ensuring on-premises applications maintain access for quick recovery. A solutions architect is designing a solution with minimal operational overhead.**

- <font color=OrangeRed>A. Deploy an AWS Storage Gateway file gateway on-premises and associate it with an Amazon S3 bucket. (correct)</font>
- B. Back up the databases to an AWS Storage Gateway volume gateway and access it using the Amazon S3 API.
- C. Transfer the database backup files to an Amazon EBS volume attached to an EC2 instance.
- D. Back up the database directly to an AWS Snowball device.

---

**Storage Gateway configurations:**

> <font color=OrangeRed>Gateway-Cached (File Gateway)</font> — volumes retain a copy of frequently accessed data subsets locally. Offers substantial cost savings on primary storage. Suitable for low-latency service of the last few days of files.

> **Amazon Storage Gateway only backs up to S3.**

**Retain old backup solution — migration strategy:**

> AWS Storage Gateway VTL solution. Can be installed in the on-premises environment utilizing the existing enterprise backup product.

> During transition, a second AWS Storage Gateway VTL solution could be commissioned in the customer's new VPC.

> Old tapes could either be restored to the Storage Gateway volume, or migrated to Virtual tapes inside AWS using Tape Gateway.

**EBS capabilities:**

> Create an <font color=OrangeRed>encrypted snapshot</font> from an unencrypted snapshot by creating an encrypted copy of the unencrypted snapshot.

> Create an <font color=OrangeRed>encrypted volume</font> from a snapshot of another encrypted volume.

> Cannot create an unencrypted volume from an encrypted snapshot.

> Cannot encrypt an existing volume.

**EBS — increasing IOPS for a MySQL database on the root volume:**

> **Add 4 additional EBS SSD volumes and create a RAID 10 using these volumes.**

**EBS voting application requiring 40,000 IOPS:**

> <font color=OrangeRed>Change to io1.</font>

---

**Database-style application with frequent multiple reads and writes:**

> <font color=OrangeRed>Elastic File Service (EFS)</font>

> <font color=OrangeRed>EBS</font>

> S3 is for object storage, not applications.

---

**EBS volume preservation before deleting EC2 instances:**

> Take a snapshot of the EBS volumes. Snapshots are stored in S3 and can be used to restore volumes on short notice.

---

## Route 53 / DNS / CloudFront

**Q32. A company is hosting a website behind multiple Application Load Balancers. The company has different distribution rights for its content around the world. A solutions architect needs to ensure that users are served the correct content without violating distribution rights.**

- A. Configure CloudFront with AWS WAF.
- B. Configure Application Load Balancers with AWS WAF.
- <font color=OrangeRed>C. Configure Route 53 with a geolocation policy. (correct)</font>
- D. Configure Route 53 with a geoproximity routing policy.

---

**Q92. A company recently expanded globally and wants to make its application accessible to users in those geographic locations. The company needs the ability to shift traffic from resources in one region to another.**

- A. Configure a Route 53 latency routing policy.
- B. Configure a Route 53 geolocation routing policy.
- <font color=OrangeRed>C. Configure a Route 53 geoproximity routing policy. (correct)</font>
- D. Configure a Route 53 multivalue answer routing policy.

---

**Q99. A company's web application is running on EC2 instances behind an ALB. The company now requires the application to be accessed from one specific country only.**

- A. Configure the security group for the EC2 instances.
- B. Configure the security group on the ALB.
- <font color=OrangeRed>C. Configure AWS WAF on the Application Load Balancer in a VPC. (correct)</font>
- D. Configure the network ACL for the subnet.

---

**Q112. A company recently launched its website to serve content to its global user base. The company wants to store and accelerate the delivery of static content. CloudFront is used with an EC2 instance attached as its origin. How to optimize high availability for the application?**

- <font color=OrangeRed>A. Use Lambda@Edge for CloudFront. (high availability, low latency, improved performance.) (correct)</font>
- B. Use Amazon <font color="#ad8456">S3</font> Transfer Acceleration for CloudFront.
- C. Configure another EC2 instance in a different AZ as part of the origin group.
- D. Configure another EC2 instance as part of the origin server cluster in the same AZ.

---

**Q126. A company has created an isolated backup of its environment in another Region. The application is running in warm standby mode and is fronted by an ALB. The current failover process is manual and requires updating a DNS alias record. How to automate the failover process?**

- A. Enable an <font color="#ad8456">ALB health check</font>.
- <font color=OrangeRed>B. Enable a Route 53 health check. (correct)</font>
- C. Create a <font color="#ad8456">CNAME record</font> on Route 53 pointing to the ALB endpoint.
- D. Create conditional forwarding rules on Route 53.

<font color="blue">Route 53 health check with active-passive failover record.</font>

---

**Q131. A company runs a website on EC2 instances behind an ALB. Route 53 is used for the DNS. The company wants to set up a backup website with a message including a phone number and email address that users can reach if the primary website is down.**

- <font color=OrangeRed>A. Use S3 website hosting for the backup website and Route 53 failover routing policy. (correct)</font>
- B. Use S3 website hosting for the backup website and Route 53 <font color="#ad8456">latency routing</font> policy.
- C. Deploy the application in another AWS Region and use ELB health checks for failover routing.
- D. Deploy the application in another AWS Region and use server-side redirection.

---

**Route 53 Record Types:**

> <font color=OrangeRed>Geolocation routing policy</font> — to route traffic based on the location of your users.

> <font color=OrangeRed>Geoproximity routing policy</font> — to route traffic based on the location of your resources and, optionally, shift traffic from resources in one location to resources in another.

> Route 53 CNAME — provides domain name alias within your zone; allows a single system to have multiple names associated with a single IP address.

> Route 53 Alias record — let you route traffic to selected AWS resources, such as CloudFront distributions and S3 buckets. Also let you route traffic from one record in a hosted zone to another record.

> Route 53 "A" record — <font color=OrangeRed>IPv4</font> address.

> Route 53 health check — active-passive failover record.

**When creating a record in Route 53 to other AWS resources, including ALBs, should use Alias records where available.**

**Route 53 Routing Policies:**

> Failover Routing Policy

> Geoproximity Routing Policy

> Simple Routing Policy

> Geolocation Routing Policy

> Latency Routing Policy

> **Weighted**

---

**DNS configurations for two EC2 instances in different AZs hosting the same content:**

> Assign each EC2 instance with an Elastic IP Address. Configure a Route 53 <font color="#ad8456">"A" multi-value record with both EIPs</font> and health checks.

> Set up an Application Load Balancer and place instances behind this ELB. Configure a Route 53 <font color="#ad8456">Alias record to point to the resource of the Application Load Balancer</font>.

---

**Q (which record type to point DNS name to ALB):**

> <font color=OrangeRed>Alias with an A type record set.</font>

---

## VPC / Networking / Security

**VPC Peering:**

> VPC peering is HA and uses the AWS network backbone.

**Q13. An application running on an EC2 instance in VPC-A needs to access files in another EC2 instance in VPC-B (separate AWS accounts). The connectivity should not have a single point of failure or bandwidth concerns.**

- <font color=OrangeRed>A. Set up a VPC peering connection between VPC-A and VPC-B. (correct)</font>
- B. Set up VPC gateway endpoints for the EC2 instance running in VPC-B.
- C. Attach a virtual private gateway to VPC-B and enable routing from VPC-A.
- D. Create a private virtual interface (VIF) for the EC2 instance running in VPC-B.

<font color="blue">VPC peering is HA and uses the AWS network backbone.</font>

---

**When would a virtual private gateway be used?**

> <font color=OrangeRed>When a VPC connects to a Private VIF with Direct Connect.</font>

> <font color=OrangeRed>When needing to attach to multiple VPN connections.</font>

> <font color=OrangeRed>When using a VPN connection between a customer gateway and a VPC.</font>

**Which has the highest priority in a routing table?**

> <font color=OrangeRed>Local routes</font>

---

**Q54. A company has deployed an API in a VPC behind an internal ALB. A client application is deployed in a second account in private subnets behind a NAT gateway. NAT gateway costs are higher than expected. Which combination of architectural changes will reduce the NAT gateway costs? (Choose two.)**

- A. Configure a <font color="#ad8456">VPC peering connection</font> between the two VPCs. Access the API using the private address.
- B. Configure an <font color="#ad8456">AWS Direct Connect connection</font> between the two VPCs. Access the API using the private address.
- C. Configure a ClassicLink connection for the API into the client VPC.
- <font color=OrangeRed>D. Configure a PrivateLink connection for the API into the client VPC. Access the API using the PrivateLink address. (correct)</font>
- <font color=OrangeRed>E. Configure an AWS Resource Access Manager (RAM) connection between the two accounts. Access the API using the private address. (correct)</font>

<font color="blue">Private link eliminates the need for peering. AWS RAM: easily and securely share AWS resources with any AWS account or within your AWS Organization.</font>

---

**Q82. An application runs on EC2 instances in private subnets. The application needs to access a DynamoDB table. What is the MOST secure way to access the table while ensuring traffic does not leave the AWS network?**

- <font color=OrangeRed>A. Use a VPC endpoint for DynamoDB. (correct)</font>
- B. Use a NAT gateway in a public subnet.
- C. Use a NAT instance in a private subnet.
- D. Use the <font color="#ad8456">internet gateway</font> attached to the VPC.

---

**Q101. A company has an EC2 instance running on a private subnet that needs to access a public website to download patches and updates. The company does not want external websites to see the EC2 instance IP address or initiate connection to it.**

- A. Create a site-to-site VPN connection between the private subnet and the network in which the public site is deployed.
- <font color=OrangeRed>B. Create a NAT gateway in a public subnet. Route outbound traffic from the private subnet through the NAT gateway. (correct)</font>
- C. Create a network ACL for the private subnet that only allows access from the IP address range of the public website.
- D. Create a security group that only allows connections from the IP address range of the public website.

---

**Q110. Moving static content from EC2 instances to an S3 bucket. A CloudFront distribution will be used to deliver the static assets. Access to the static content should be restricted to a limited set of IP ranges. (Choose two.)**

- <font color=OrangeRed>A. Create an origin access identity (OAI) and associate it with the distribution. Change the permissions in the bucket policy so that only the OAI can read the objects. (correct)</font>
- <font color=OrangeRed>B. Create an AWS WAF web ACL that includes the same IP restrictions that exist in the EC2 security group. Associate this new web ACL with the CloudFront distribution. (correct)</font>
- C. Create a new security group that includes the same IP restrictions. Associate this new security group with the CloudFront distribution.
- D. Create a new security group that includes the same IP restrictions. Associate this new security group with the S3 bucket.
- E. Create a new IAM role and associate the role with the distribution.

<font color="blue">A alone is not enough to restrict access to a limited set of IP ranges.</font>

---

**Q117. A company's application hosted on EC2 instances needs to access an S3 bucket. Due to data sensitivity, traffic cannot traverse the internet.**

- A. Create a private hosted zone using Route 53.
- <font color=OrangeRed>B. Configure a VPC gateway endpoint for S3 in the VPC. (correct)</font>
- C. Configure AWS PrivateLink between the EC2 instance and the S3 bucket.
- D. Set up a <font color="#ad8456">site-to-site VPN</font> connection between the VPC and the S3 bucket.

<font color="blue">S3 supports VPC Gateway Endpoint.</font>

---

**Q141. A company has global users accessing an application deployed in different AWS Regions, exposing public static IP addresses. The users are experiencing poor performance when accessing the application over the internet.**

- <font color=OrangeRed>A. Set up AWS Global Accelerator and add endpoints. (correct)</font>
- B. Set up <font color="#ad8456">AWS Direct Connect</font> locations in multiple Regions.
- C. Set up a CloudFront distribution to access an application.
- D. Set up a Route 53 geoproximity routing policy to route traffic.

---

**Q143. A company recently deployed a two-tier application in two AZs in us-east-1. The databases are deployed in a private subnet and the web servers are deployed in a public subnet. An internet gateway is attached to the VPC. The database servers are unable to access patches on the internet. Design a solution that maintains database security with the least operational overhead.**

- <font color=OrangeRed>A. Deploy a NAT gateway inside the public subnet for each Availability Zone and associate it with an Elastic IP address. Update the routing table of the private subnet to use it as the default route. (correct)</font>
- B. Deploy a NAT gateway inside the <font color="#ad8456">private</font> subnet for each Availability Zone.
- C. Deploy two NAT instances inside the public subnet.
- D. Deploy two NAT instances inside the <font color="#ad8456">private</font> subnet.

---

**Q151. Designing a hybrid application using AWS Direct Connect (DX). The application connectivity between AWS and the on-premises data center must be highly resilient. Which DX configuration should be implemented?**

> <font color=OrangeRed>Pink background = subsection marker</font>

- A. Configure a DX connection with <font color="#ad8456">a VPN</font> on top of it.
- <font color=OrangeRed>B. Configure DX connections at multiple DX locations. (correct)</font>
- C. Configure a DX connection using the <font color="#ad8456">most reliable DX partner</font>.
- D. Configure multiple virtual interfaces on top of a DX connection.

---

**Networking High Availability:**

> <font color=OrangeRed>A virtual private gateway is HA by design.</font>

> <font color=OrangeRed>A NAT gateway should be added to each AZ a VPC uses for full HA.</font>

**VPC Subnets — example (web app with 3 AZs, public LB, private web servers, private DB):**

> 9 subnets required (3 AZs × 3 tiers: public/LB, private/web, private/DB)

**Making a subnet public:**

> <font color=OrangeRed>Attach an Internet Gateway (IGW) to the VPC.</font>

> <font color=OrangeRed>Create a route in the route table of the subnet allowing a route out of the Internet Gateway (IGW).</font>

**One VPC deployment for two AZs with one application tier — least infrastructure:**

> One VPC and two subnets.

**HA improvement: tolerate failure of an AWS AZ and a customer internet connection or router:**

> Add another similar VPN connection to a second CGW.

**Valid sources or destinations for a VPC Security Group:**

> The prefix list ID for an AWS service.

> A range of IPv4 Addresses.

> A different security group.

> NOT: An IAM Role, An S3 Bucket, An EC2 Instance (EC2 instance IDs are not valid).

**Network Access Logging:**

> Make use of an OS-level logging tool such as iptables and log events to CloudWatch or S3.

> <font color=OrangeRed>Set up a Flow Log for the group of instances and forward them to CloudWatch or S3.</font>

**NACLs — stateless:**

> Network Access Control lists are stateless. You need to create an outbound rule allowing RDP response traffic to go back out again.

> The * (asterisk) rule cannot be modified or removed.

---

**Direct Connect:**

> Provides a private, dedicated network connection between on-premises network and the VPC.

> For a private, dedicated connection bypassing the Internet with throughput of 10 Gbps: **AWS Direct Connect**.

**AWS VPN:**

> Best meets requirements when the ability to reuse existing internet connections is needed.

**PrivateLink:**

> Provides private connectivity between VPCs and AWS services securely on the AWS network without exposure to the public Internet.

> Implemented by a service provider creating an Endpoint Service and a service consumer connecting via an Interface VPC Endpoint.

> Direct Connect is between customer and AWS, not two AWS customers.

**Shipping company with freight carrier (both on AWS) — best security and operational efficiency:**

> <font color=OrangeRed>Have the freight carrier create an Endpoint Service and use an Interface VPC Endpoint to connect.</font>

<font color="blue">VPC Peering and VPN connections will work, but will require more operational overhead than PrivateLink.</font>

---

## IAM / Security / Compliance

**Q33. A solutions architect has created a new AWS account and must secure AWS account root user access. Which combination of actions? (Choose two.)**

- <font color=OrangeRed>A. Ensure the root user uses a strong password. (correct)</font>
- <font color=OrangeRed>B. Enable multi-factor authentication on the root user. (correct)</font>
- C. Store root user access keys in an encrypted Amazon S3 bucket.
- D. Add the root user to a group containing administrative permissions.
- E. Apply the required permissions to the root user with an inline policy document.

---

**Q35. A company's website uses CloudFront and WAF against SQL injection. The ALB is the origin for the CloudFront distribution. A recent review revealed an external malicious IP that needs to be blocked.**

- A. Modify the network ACL on the CloudFront distribution to add a deny rule.
- <font color=OrangeRed>B. Modify the configuration of AWS WAF to add an IP match condition to block the malicious IP address. (correct)</font>
- C. Modify the <font color="#ad8456">network ACL for the EC2 instances</font> in the target groups behind the ALB.
- D. Modify the <font color="#ad8456">security groups</font> for the EC2 instances.

---

**Q37. A web application is deployed in the AWS Cloud. The web server is vulnerable to cross-site scripting (XSS) attacks.**

- A. Create a Classic Load Balancer. Put the web layer behind the load balancer and enable AWS WAF.
- B. Create a Network Load Balancer. Put the web layer behind the load balancer and enable AWS WAF.
- <font color=OrangeRed>C. Create an Application Load Balancer. Put the web layer behind the load balancer and enable AWS WAF. (correct)</font>
- D. Create an ALB. Put the web layer behind the load balancer and <font color="#ad8456">use AWS Shield Standard</font>.

---

**Q70. IAM policy: EC2 termination action with conditions. What is the effect of this policy?**

- A. Users can terminate an EC2 instance in any AWS Region except us-east-1.
- B. Users can terminate an EC2 instance with the IP address 10.100.100.1 in the us-east-1 Region.
- <font color=OrangeRed>C. Users can terminate an EC2 instance in the us-east-1 Region when the user's source IP is 10.100.100.254. (correct)</font>
- D. Users cannot terminate an EC2 instance in the us-east-1 Region when the user's source IP is 10.100.100.254.

<font color="blue">StringNotEquals condition implies deny all actions on EC2 so far as the request is not coming from us-east-1 — that is, allow actions only from us-east-1 (negate matching). Deny rule takes effect before allow rule. Users can terminate instances in us-east-1 from the specified IP range.</font>

> `deny all action on ec2, the condition is` <font color=OrangeRed>StringNotEquals</font>`!!!`

---

**Q114. A company currently stores symmetric encryption keys in an HSM. The solution should allow for key rotation and support the use of customer-provided keys.**

- A. S3
- B. AWS Secrets Manager
- C. AWS Systems Manager Parameter Store
- <font color=OrangeRed>D. AWS Key Management Service (AWS KMS) (correct)</font>

---

**Q122. A company has enabled AWS CloudTrail logs to deliver log files to an S3 bucket for each of its developer accounts. A central AWS account is needed for streamlining management and audit reviews. An internal auditor needs access to the CloudTrail logs, yet access needs to be restricted for developer account users.**

- A. Configure an <font color="#ad8456">AWS Lambda function in each developer account</font> to copy the log files to the central account. Create an IAM role in the central account for the auditor.
- B. Configure CloudTrail from each developer account to deliver the log files to an S3 bucket in the central account. Create an <font color="#ad8456">IAM user</font> in the central account for the auditor. Attach an <font color="#ad8456">IAM policy providing full permissions</font>.
- <font color=OrangeRed>C. Configure CloudTrail from each developer account to deliver the log files to an S3 bucket in the central account. Create an IAM role in the central account for the auditor. Attach an IAM policy providing read-only permissions to the bucket. (correct)</font>
- D. Configure an <font color="#ad8456">AWS Lambda function in the central account</font> to copy the log files from S3 buckets in each developer account. Create an IAM user in the central account. Attach an <font color="#ad8456">IAM policy providing full permissions</font>.

<font color="blue">CloudTrail can send logs directly to an S3 bucket in another account.</font>

---

**Q129. A company has implemented one of its microservices on AWS Lambda that accesses a DynamoDB table named Books. The IAM policy must allow put, update, and delete items in the Books table and prevent the function from performing any other actions on the Books table or any other table. Which IAM policy would fulfill these needs and provide the LEAST privileged access?**

> <font color=OrangeRed>A. (correct) — Policy with specific DynamoDB actions (PutItem, UpdateItem, DeleteItem) scoped to the exact Books table ARN only.</font>

---

**Q142. A company wants to migrate a workload to AWS. All data must be encrypted at rest. The company wants complete control of encryption key lifecycle management. The company must be able to immediately remove the key material and audit key usage independently of AWS CloudTrail.**

- <font color=OrangeRed>A. AWS CloudHSM with the CloudHSM client. (correct)</font>
- B. AWS KMS with AWS CloudHSM.
- C. AWS KMS with an external key material origin.
- D. <font color="#ad8456">AWS KMS with AWS managed customer master keys (CMKs)</font>.

---

**Q158. A company runs an application using ECS. The application creates resized versions of an original image and then makes S3 API calls to store the resized images in S3. How can a solutions architect ensure that the application has permission to access S3?**

- A. Update the S3 role in AWS IAM to allow read/write access from ECS.
- <font color=OrangeRed>B. Create an IAM role with S3 permissions, and then specify that role as the taskRoleArn in the task definition. (correct)</font>
- C. Create a security group that allows access from ECS to S3.
- D. Create an IAM user with S3 permissions, and then relaunch the EC2 instances while logged in as this account.

---

**Q160. A company has established a new AWS account. The company is concerned about the security of the AWS account root user.**

- A. Create IAM users for daily administrative tasks. Disable the root user.
- <font color=OrangeRed>B. Create IAM users for daily administrative tasks. Enable multi-factor authentication on the root user. (correct)</font>
- C. Generate an access key for the root user. Use the access key for daily administration tasks.
- D. <font color="#ad8456">Provide the root user credentials to the most senior solution architect</font>.

---

**Q231. A company is moving to AWS. Management has identified a set of approved AWS services. The company would like to restrict access to all other unapproved services with the LEAST amount of operational overhead.**

- A. Configure the AWS Trusted Advisor service utilization compliance report.
- B. Use AWS Config to evaluate configuration settings.
- <font color=OrangeRed>C. Configure AWS Organizations. Create an organizational unit (OU) and place all AWS accounts into the OU. Apply a service control policy (SCP) to the OU that denies the use of certain services. (correct)</font>
- D. Create a custom AWS IAM policy. Deploy the policy to each account using AWS CloudFormation StackSets.

---

**IAM — cross-account access to S3 (objects must be owned by your account):**

> <font color=OrangeRed>Create an IAM role for your AWS account to allow access from external IAM users.</font>

**Service Control Policy (SCP):**

> Used to restrict what can occur within an account, including restricting the root user.

**AWS Root Account:**

> The Root account cannot be denied access to resources by Policy.

> You should keep a copy of the MFA URL or QR code when you set up the Root account MFA.

**S3 bucket access for a third of all 200 users — most time efficient:**

> <font color=OrangeRed>Create a new policy which will grant permissions to the bucket. Create a group and attach the policy to that group. Add the users to this group.</font>

**S3 encryption — managing your own encryption keys, using Amazon S3 to manage the encryption itself:**

> <font color=OrangeRed>Server-Side Encryption with Customer-Provided Keys (SSE-C)</font>

**Default security group:**

> You can't delete this group; however, you can change the group's rules.

---

**Q (cross-site scripting and SQL injection):**

> <font color=OrangeRed>Using WAF, set up rules which block SQL injection and cross-site scripting attacks. Associate the rules to the ALB.</font>

**Amazon GuardDuty:** Managed <font color=OrangeRed>threat detection</font> service.

**AWS Shield Advanced:**

> Purchase AWS Shield Advanced, and during an attack lodge a support request asking for assistance from AWS.

---

**CloudTrail — NOT a feature:**

> <font color="#ad8456">Monitor Auto Scaling Groups and optimize resource utilization</font> = CloudWatch.

> <font color=OrangeRed>Answer simple questions about user activity.</font>

> <font color=OrangeRed>Demonstrate compliance.</font>

> <font color=OrangeRed>Track changes to resources.</font>

---

**AWS Trusted Advisor vs Personal Health Dashboard:**

> AWS Personal Health Dashboard — use to check on the status of an AWS service.

**AWS services — checking status:**

> Use AWS Personal Health Dashboard to check on the status of a specific service.

---

**Disaster Recovery strategies:**

> <font color=OrangeRed>Pilot light</font> — have a minimal version of the application always running in another Region.

> **Warm standby**

> **Multi-site**

> **Backup and restore**

---

**ENI attach types:**

> **hot attach** — attach a network interface to an instance when it's running.

> **warm attach** — attach when the instance is stopped.

> <font color=OrangeRed>cold attach</font> — attach when the instance is being launched.

---

## Cost Optimization / Pricing

**Q3. A company must generate sales reports at the beginning of every month. The reporting process launches 20 EC2 instances on the first of the month. The process runs for 7 days and cannot be interrupted. The company wants to minimize costs.**

- A. <font color="#ad8456">Reserved</font> Instances
- B. <font color="#ad8456">Spot</font> Block Instances
- C. On-Demand Instances
- <font color=OrangeRed>D. Scheduled Reserved Instances (correct)</font>

---

**Q124. A company is using EC2 to run its big data analytics workloads. These variable workloads run each night, and it is critical they finish by the start of business the following day. Which solution will accomplish this?**

- A. <font color="#ad8456">Spot Fleet</font> — does NOT guarantee instances in the required time frame.
- B. <font color="#ad8456">Spot Instances</font> — does NOT guarantee instances in the required time frame.
- <font color=OrangeRed>C. Reserved Instances (correct)</font>
- D. On-Demand Instances — most expensive option.

---

**Stateless web tier — most cost-effective HA:**

> Use an Elastic Load Balancer, a multi-AZ deployment of an Auto-Scaling group of EC2 Spot instances (primary) running in tandem with an Auto-Scaling group of EC2 On-demand instances (secondary), DynamoDB.

<font color="blue">The On-demand instances behind the Spot instances deliver the most cost-effective solution because the on-demand will only spin up if the spot instances are not available. DynamoDB lends itself better to supporting stateless web/app installations.</font>

---

**Q154. A company recently started selling to users in Europe and Australia. The application is running in the United States. Design a solution so international users have an improved browsing experience. Which solution is MOST cost-effective?**

- A. Host the <font color="#ad8456">entire website on S3</font>.
- <font color=OrangeRed>B. Use CloudFront and S3 to host static images. (correct)</font>
- C. Increase the number of public load balancers and EC2 instances.
- D. Deploy the two-tier website in AWS Regions in Europe and Australia.

---

**Q (SQS-based video transcoding cost reduction):**

> **Use spot instances** — will significantly reduce the ongoing cost. Even assuming some jobs will fail because of terminating spot instances, the Auto Scaling group will grow to compensate.

---

## Miscellaneous / Architecture Patterns

**Q26. A manufacturing company will install thousands of IoT sensors that will send data to AWS in real time. A solutions architect is tasked with receiving events in an ordered manner for each machinery asset and ensuring that data is saved for further processing.**

- <font color=OrangeRed>A. Use Amazon Kinesis Data Streams for real-time events with a partition for each equipment asset. Use Amazon Kinesis Data Firehose to save data to S3. (correct)</font>
- B. Use Amazon Kinesis Data Streams for real-time events with a shard for each equipment asset. Use Amazon Kinesis Data Firehose to save data to <font color="#ad8456">EBS</font>.
- C. Use an Amazon SQS FIFO queue for real-time events with one queue for each equipment asset. Trigger an AWS Lambda function to save data to Amazon EFS.
- D. Use an Amazon SQS standard queue for real-time events with one queue for each equipment asset.

---

**Q74. A company built a food ordering application. The static front end is deployed on an EC2 instance. The front-end application sends requests to the backend application running on a separate EC2 instance. The backend application stores the data in RDS. How to decouple the architecture and make it scalable?**

- A. Use S3 to serve the front-end application which <font color="#ad8456">sends requests to EC2</font> to execute the backend application.
- B. Use S3 to serve the front-end application and write requests to an <font color="#ad8456">SNS topic</font>.
- C. Use an <font color="#ad8456">EC2 instance to serve the front end</font> and write requests to an SQS queue.
- <font color=OrangeRed>D. Use S3 to serve the static front-end application and send requests to Amazon API Gateway, which writes the requests to an SQS queue. Place the backend instances in an Auto Scaling group, and scale based on the queue depth to process and store the data in RDS. (correct)</font>

---

**Q145. A solutions architect needs to design a low-latency solution for a static single-page application accessed by users utilizing a custom domain name. The solution must be serverless, encrypted in transit, and cost-effective. (Choose two.)**

- <font color=OrangeRed>A. S3 (correct)</font>
- B. <font color="#ad8456">EC2</font>
- C. AWS Fargate
- <font color=OrangeRed>D. CloudFront (correct)</font>
- E. Elastic Load Balancer

---

**Q146. A company is migrating to the AWS Cloud. A file server is the first workload to migrate. Users must be able to access the file share using the Server Message Block (SMB) protocol.**

- A. Amazon EBS
- B. Amazon EC2
- <font color=OrangeRed>C. Amazon FSx (correct)</font>
- D. Amazon S3

<font color="blue">For SMB use Amazon FSx for Windows.</font>

---

**Q156. A company wants to deploy a shared file system for its .NET application servers and Microsoft SQL Server database running on EC2 instances with Windows Server 2016. The solution must be integrated into the corporate Active Directory domain.**

- <font color=OrangeRed>A. Use Amazon FSx for Windows File Server. (correct)</font>
- B. Use Amazon EFS.
- C. Use AWS Storage Gateway in file gateway mode.
- D. Deploy a Windows file server on two On-Demand instances.

<font color="blue">FSx for Windows can be integrated with on-premises Active Directory.</font>

---

**Q164. S3 gateway endpoint — allow traffic to trusted buckets only:**

- <font color=OrangeRed>D. Create an S3 endpoint policy for each S3 gateway endpoint that provides access to the Amazon Resource Name (ARN) of the trusted S3 buckets. (correct)</font>

---

**Q167. Migrate a Windows IIS web application to AWS. The application currently relies on a file share hosted in the user's on-premises NAS. Which replacement to the on-premises file share is MOST resilient and durable?**

- A. Migrate the file share to Amazon RDS.
- B. Migrate the file share to AWS Storage Gateway.
- <font color=OrangeRed>C. Migrate the file share to Amazon FSx for Windows File Server. (correct)</font>
- D. Migrate the file share to Amazon Elastic File System (Amazon EFS).

---

**Step Functions:**

> State machines are used by Step Functions. This product is serverless and can orchestrate long-running workflows involving other AWS services and human interaction.

**VM Import/Export:**

> Used to move VMDK files from a private cloud platform (VMware) to AWS and create EC2 instances.

**ECS task permissions:**

> Create an IAM role with S3 permissions, and then specify that role as the taskRoleArn in the task definition.

---

**AWS services allowing native encryption of data at rest:**

> <font color=OrangeRed>EBS, S3, and EFS</font> — allow the user to configure encryption at rest using either the AWS Key Management Service (KMS) or customer-provided keys.

> Exception: Elasticache for Memcached does not offer a native encryption service.

---

**Redshift:**

> <font color=OrangeRed>Redshift</font> — run complex analytic queries against terabytes of structured data, using sophisticated query optimization, columnar storage on high-performance storage, and massively parallel query execution.

**Durable key-value store on AWS:**

> **S3**

---

**Glacier:**

> Need to be securely stored for 7 years; rare retrieval within 24 hours of a claim: **Glacier**.

> Recovery rate is a key decider. The storage must be safe, durable, low cost, and the recovery can be slow.

---

**CloudWatch custom metrics:**

> Memory utilization

> Disk swap utilization

> Disk space utilization

> Page file utilization

> Log collection

**CloudWatch alarm — automatically reboot instance on health check failure:**

> <font color=OrangeRed>Create an Amazon CloudWatch alarm that monitors an Amazon EC2 instance and automatically reboots the instance if a health check fails.</font>

**SNS + CloudWatch for EBS monitoring:**

> <font color=OrangeRed>SNS</font> and <font color=OrangeRed>CloudWatch</font> — configure to meet requirements for monitoring EBS volumes and notifying the database team by email.

---

**Q — DynamoDB access restricted to specific IP addresses:**

> <font color=OrangeRed>Configure an IAM group (for each level of access) and add the people who need access. Give those groups access to the DynamoDB operations they need, but add a condition to the policy so it has to match the specific IP address.</font>

> Security groups cannot be attached to DynamoDB. DynamoDB is a public service, and security groups are VPC-based security controls.

---

**Q — S3 for a commercial stock images website (pre-signed URLs):**

> <font color=OrangeRed>Move the images to S3 and use pre-signed URLs.</font>

> Moving images to S3 and adding read permissions for everyone makes images available to everyone — goes against requirements.

---

**Q — Workspaces with on-premises Active Directory:**

> <font color=OrangeRed>Configure AD Connector</font> — AD Connector is a directory gateway with which you can redirect directory requests to your on-premises Microsoft Active Directory without caching any information in the cloud.

> Configure Web Identity Federation and Cognito — designed for a web application or mobile application to allow users to authenticate.

---

**Q — IAM role for web application logins (up to 1,000,000 users) that access AWS resources:**

> <font color=OrangeRed>Create an IAM role that trusts an external IDP. Provide this role with permissions for the AWS services.</font>

---

**Q — Application that runs 10 EC2 instances needs to store logs on a file system accessible from all instances natively, and logs need to be accessible from a central location searchable from the AWS console:**

> <font color=OrangeRed>CloudWatch Logs and EFS</font>

---

**Q — EC2 instance in us-east-1a fails. Options to recover the application:**

> <font color=OrangeRed>If available, use a snapshot of the EBS volume to make a new volume AND then create a new EC2 instance in a different availability zone.</font>

> EBS snapshots are stored in S3, don't have a region, not possible to copy snapshots between AZs.

---

**Q — Which are NOT global AWS services:**

> <font color=OrangeRed>EC2</font>

> <font color=OrangeRed>S3</font>

> <font color=OrangeRed>DynamoDB</font>

---

**Q — Minimum subnets to make public:**

> Attach an Internet Gateway (IGW) to the VPC.

> Create a route in the route table of the subnet allowing a route out of the Internet Gateway (IGW).

---

**Q — Bastion host in VPC (corporate data center SSH access only):**

> Create the bastion host (EC2 instance). For the instance security group, add ingress on port 22, and specify the address range of the personnel in the data center. Use a private key to connect to the bastion host. Add an <font color=OrangeRed>internet gateway</font>, a route table, and a route to the IGW in the route table.

---

**Q — NACLs evaluated in order — * rule:**

> **NACL rules: 100 All Traffic Allow / 200 All Traffic Deny / * All Traffic Deny**

> The * rule: if a packet doesn't match any of the other numbered rules, it's denied. **You can't modify or remove this rule.**

---

**Q — CloudFormation template for granular service control and version control of infrastructure:**

> <font color=OrangeRed>CloudFormation</font>

---

**Q — Deploy clustered application on a small number of EC2 instances across multiple AZs with high speed, low latency communication between nodes, and minimize hardware failure risk:**

> <font color=OrangeRed>Deploy the EC2 servers in a Spread Placement Group.</font>

<font color="blue">Spread Placement Groups are recommended for applications that have a small number of critical instances which need to be kept separate from each other. Reduces risk of simultaneous failures that might occur when instances share the same underlying hardware.</font>

---

**Windows + file share:**

> **<font color=OrangeRed>Windows</font> + <font color="blue">file</font> share:** Amazon FSx for Windows File Server.

---

**A principal:**

> A principal is a person or application that can make an authenticated or anonymous request to perform an action on a system.

---

**EC2 IOPS application — io1:**

> For an application needing 40,000 IOPS, change from GP volumes to **io1**.

---

**EFS — concurrent access scenario:**

> An application you are auditing runs from 10 EC2 instances. It needs to store logs on a file system that can be accessed from all the EC2 instances natively. Use **EFS**.

---

**Network configuration for 20 instances (C3.2xLarge) pulling jobs from SQS, ~500 Mbps per instance at the beginning and end of each job:**

> <font color=OrangeRed>Spread the Instances over multiple AZs</font> to minimize traffic concentration and maximize fault-tolerance.

<font color="blue">The 500 Mbps only occurs for short intervals, so sustained throughput is not 10 Gbps. Use simple solutions such as spreading the load out rather than expensive high-tech solutions.</font>

---

**Which native AWS service will act as a file system mounted on an S3 bucket?**

> <font color=OrangeRed>AWS Storage Gateway</font>

---

**Revert from Dedicated hosting tenancy to Default hosting tenancy:**

> Use the AWS CLI to modify the Instance Placement attribute of each instance and the VPC tenancy attribute of the VPC.

---

**Q — Which AWS Database services do NOT withstand an AZ outage within a single cluster:**

> <font color=OrangeRed>RedShift</font>

> MS SQL, MySQL, PostgreSQL — do withstand AZ outage.

---
