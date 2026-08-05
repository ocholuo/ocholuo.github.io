---
title: "Meow's AWS - Developer Associate Exam Q&A"
date: 2026-05-24 11:11:11 -0400
categories: [certification, AWS]
tags: [AWS, STS, IAM, CodeDeploy, CodeCommit, CloudFormation, ElasticBeanstalk, SSM, ExamPrep]
math: false
toc: true
---

# AWS Developer Associate Exam Q&A

AWS Developer Associate 考试练习题，涵盖 STS、IAM、CodeDeploy、CodeCommit、CloudFormation、Elastic Beanstalk 等核心服务。

Practice questions for the AWS Developer Associate exam, covering STS, IAM, CodeDeploy, CodeCommit, CloudFormation, and Elastic Beanstalk.

---

## IAM / STS

---

**Q: When requested through an STS API call, credentials are returned with what three components?**
通过 STS API 调用返回的临时凭证包含哪三个组成部分？

> <font color=OrangeRed>**A: Security Token, Access Key ID, Secret Access Key**</font>

STS 临时凭证包含三个组件：安全令牌（Security Token）、访问密钥 ID（Access Key ID）、秘密访问密钥（Secret Access Key），三者共同用于后续 AWS API 调用的认证。

STS credentials consist of three components — Security Token, Access Key ID, and Secret Access Key — all required to authenticate subsequent AWS API calls.

---

**Q: You would like to use STS to allow end users to authenticate from third-party providers such as Facebook, Google, and Amazon. What is this type of authentication called?**
通过 STS 允许终端用户使用 Facebook、Google、Amazon 等第三方提供商认证，这种认证方式叫什么？

> <font color=OrangeRed>**A: Web Identity Federation**</font>

Web 身份联合（Web Identity Federation）允许用户通过受信任的第三方身份提供商（IdP）获取临时 AWS 凭证，无需在 AWS 中直接管理用户身份。

Web Identity Federation allows users to obtain temporary AWS credentials via a trusted third-party identity provider (IdP), without managing AWS identities directly.

---

**Q: When using Web Identity Federation to allow a user to access an AWS service (such as an S3 bucket), which is the correct order of steps?**
使用 Web 身份联合访问 AWS 服务时，正确的步骤顺序是什么？

> <font color=OrangeRed>**A: The user authenticates with Facebook first → receives an ID token → trades it for temporary security credentials via AWS STS.**</font>

正确流程：

1. 用户向 Facebook 认证，获取 web 身份令牌
2. 调用 AWS STS，将 web 身份令牌作为输入传入
3. AWS STS 验证并返回临时 AWS 访问凭证
4. 用户使用临时凭证承担 IAM 角色，按照角色安全策略访问 AWS 资源

Correct order:

1. User authenticates with Facebook → receives a web identity token
2. Call AWS STS, passing the web identity token as input
3. AWS STS authorizes the call and provides temporary AWS access credentials
4. User assumes an IAM role and accesses AWS resources per the role's security policy

---

**Q: Which of these are necessary fields in an IAM Policy?**
IAM 策略中哪些字段是必需的？

> <font color=OrangeRed>**A: Actions, Resources, Effects**</font>

IAM 策略的三个必需字段：

- **Effect**：`Allow` 或 `Deny`，指定是否允许该操作
- **Action**：策略允许或拒绝的 AWS 服务操作（如 `s3:GetObject`）
- **Resource**：操作适用的 AWS 资源（ARN 格式）

Three required fields in an IAM policy:

- **Effect**: `Allow` or `Deny` — whether the action is permitted
- **Action**: the AWS service actions the policy allows or denies (e.g., `s3:GetObject`)
- **Resource**: the AWS resources the actions apply to (ARN format)

---

**Q: Which service can be used to securely store confidential information like credentials and license codes so that they can be accessed by EC2 instances?**
哪个 AWS 服务可以安全存储凭证和许可码等机密信息，供 EC2 实例访问？

> <font color=OrangeRed>**A: Systems Manager Parameter Store**</font>

AWS Systems Manager Parameter Store 提供安全的分层存储，用于配置数据管理和密钥管理。可以将密码、数据库连接字符串、许可码等作为参数值存储，并通过 IAM 策略控制访问权限。

AWS Systems Manager Parameter Store provides secure, hierarchical storage for configuration data and secrets management. Passwords, database strings, and license codes can be stored as parameter values, with access controlled via IAM policies.

---

## CodeDeploy

---

**Q: When deploying application code to an EC2/On-Premises compute platform, the AppSpec file can be written in which language?**
将应用代码部署到 EC2/On-Premises 计算平台时，AppSpec 文件必须用什么语言编写？

> <font color=OrangeRed>**A: YAML only — the file must be named `appspec.yml` and placed in the root of the application's source code directory.**</font>

EC2/On-Premises 平台的 AppSpec 文件必须是 YAML 格式，文件名必须为 `appspec.yml`，且必须放在应用源代码目录结构的根目录下。否则部署将失败。

AWS Lambda 平台的 AppSpec 文件可以是 YAML 或 JSON 格式。

AppSpec files on an EC2/on-premises platform must be YAML-formatted, named `appspec.yml`, and placed in the root of the source code directory — otherwise deployments fail.

AppSpec files on an AWS Lambda platform can be YAML-formatted or JSON-formatted.

---

## CodeCommit

---

**Q: You want to receive an email whenever a user pushes code to a CodeCommit repository. How can you configure this?**
如何配置在用户向 CodeCommit 仓库推送代码时接收邮件通知？

> <font color=OrangeRed>**A: Configure Notifications in the console — this creates a CloudWatch Events rule that sends a notification to an SNS topic, which triggers an email.**</font>

正确配置路径：

1. 在 CodeCommit 控制台配置通知（Notifications）
2. 自动创建 CloudWatch Events 规则，监听仓库 push 事件
3. CloudWatch Events 将事件发送到 SNS 主题
4. SNS 主题触发邮件发送给订阅者

> **注意：** CodeCommit 可以使用触发器将事件发送到 SNS，但 SNS <font color=OrangeRed>不能</font>主动轮询 CodeCommit 事件。

Configuration path:

1. Configure Notifications in the CodeCommit console
2. A CloudWatch Events rule is automatically created, monitoring push events
3. CloudWatch Events sends the event to an SNS topic
4. SNS topic triggers an email to subscribers

> **Note:** CodeCommit can use a trigger to send events to SNS, but SNS <font color=OrangeRed>cannot</font> poll for CodeCommit events.

---

## CloudFormation

---

**Q: Which two things can you define using the Transforms section of the CloudFormation template?**
CloudFormation 模板的 Transforms 部分可以定义哪两件事？

> <font color=OrangeRed>**A: (1) Re-use code located in S3 / (2) Specify the use of the Serverless Application Model (SAM) for Lambda deployments**</font>

CloudFormation `Transform` 部分的两个主要用途：

- **S3 代码复用**：引用存储在 S3 的代码片段（`AWS::Include` transform），避免重复编写
- **SAM 转换**：声明 `AWS::Serverless-2016-10-31` transform，使用简化的 SAM 语法部署 Lambda 函数和 API Gateway 等无服务器资源

The two primary uses of the CloudFormation `Transform` section:

- **S3 code reuse**: reference code snippets stored in S3 via the `AWS::Include` transform
- **SAM transform**: declare `AWS::Serverless-2016-10-31` to use simplified SAM syntax for Lambda and serverless resources

---

**Q: You want to use the output of one CloudFormation stack as input to another. Which section of the template do you use?**
如何将一个 CloudFormation 栈的输出作为另一个栈的输入？应使用模板的哪个部分？

> <font color=OrangeRed>**A: Outputs**</font>

CloudFormation 模板的 `Outputs` 部分用于声明栈的输出值。其他栈可以通过 `ImportValue` 函数引用这些输出，实现跨栈资源共享（例如将 VPC ID 从基础设施栈传给应用栈）。

The `Outputs` section declares output values that other stacks can import using `ImportValue`, enabling cross-stack resource sharing (e.g., passing a VPC ID from an infrastructure stack to an application stack).

---

**Q: How can you prevent CloudFormation from deleting the entire stack on failure?**
如何防止 CloudFormation 在部署失败时删除整个栈？

> <font color=OrangeRed>**A: Use the `--disable-rollback` flag with the AWS CLI, OR set "Rollback on failure" to "No" in the CloudFormation console.**</font>

两种方式禁用回滚：

- **AWS CLI**：在 `create-stack` 命令中加 `--disable-rollback` 参数
- **控制台**：在创建栈时将"Rollback on failure"设为 No

```bash
aws cloudformation create-stack \
  --stack-name my-stack \
  --template-body file://template.yml \
  --disable-rollback
```

Two ways to disable rollback:

- **AWS CLI**: add `--disable-rollback` to the `create-stack` command
- **Console**: set the "Rollback on failure" radio button to No when creating the stack

---

## Elastic Beanstalk

---

**Q: An application is running using Docker provisioned with Elastic Beanstalk. How should a version upgrade be deployed?**
使用 Elastic Beanstalk 部署的 Docker 应用如何升级到新版本？

> <font color=OrangeRed>**A: Bundle the code into a zip file, then upload and deploy it using the Elastic Beanstalk console.**</font>

Elastic Beanstalk 标准应用版本部署流程：将应用代码打包为 zip 文件 → 通过 Elastic Beanstalk 控制台上传新版本 → 触发部署。Elastic Beanstalk 会自动处理底层 EC2 实例、负载均衡器和容器的更新。

Standard Elastic Beanstalk deployment flow: bundle the application into a zip file → upload the new version via the Elastic Beanstalk console → trigger deployment. Elastic Beanstalk handles updating the underlying EC2 instances, load balancer, and containers automatically.

---

## Key Takeaways

- **STS** 返回三组件临时凭证：<font color=OrangeRed>Security Token + Access Key ID + Secret Access Key</font>。
  STS returns three-component temporary credentials.
- **Web Identity Federation**：第三方 IdP 认证 → ID 令牌 → 换取临时 AWS 凭证。
  Third-party IdP auth → ID token → temporary AWS credentials via STS.
- **IAM Policy** 必需字段：<font color=OrangeRed>Effect、Action、Resource</font>。
  Required fields: Effect, Action, Resource.
- **SSM Parameter Store** 是 EC2 实例访问凭证和配置数据的推荐安全存储。
  Recommended secure storage for credentials accessible by EC2.
- **AppSpec**：EC2/On-Premises 必须用 YAML（`appspec.yml`）；Lambda 支持 YAML 或 JSON。
  EC2 requires YAML only; Lambda supports YAML or JSON.
- **CodeCommit 通知**：Notifications → CloudWatch Events → SNS → 邮件（SNS 不能主动轮询）。
  Notifications → CloudWatch Events → SNS → email; SNS cannot poll CodeCommit.
- **CloudFormation Transforms**：S3 代码复用（`AWS::Include`）+ SAM 无服务器语法。
  S3 code reuse + SAM syntax.
- **CloudFormation Outputs**：`ImportValue` 实现跨栈资源共享。
  Cross-stack resource sharing via `ImportValue`.
- **CloudFormation 禁用回滚**：`--disable-rollback` 或控制台 "Rollback on failure = No"。
- **Elastic Beanstalk 升级**：打包为 zip，通过控制台上传部署。
  Bundle to zip, deploy via console.

## References

- `_posts/01Cloud/01AWS/IAM/2020-07-18-STS.md`
- `_posts/01Cloud/01AWS/CodeDevelop/2020-07-18-3CodeDeploy.md`
- `_posts/01Cloud/01AWS/CodeDevelop/2020-07-18-1CodeCommit.md`
- `_posts/01Cloud/01AWS/CodeDevelop/2020-07-18-ElasticBeanstalk.md`
- `_posts/01Cloud/01AWS/CodeDevelop/CloudFormation/2020-07-18-CloudFormation.md`
- Source: Linux Academy AWS Developer Associate practice questions
