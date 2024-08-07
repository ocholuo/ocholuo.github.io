

- [AWS - IAM Identity and Access Management](#aws---iam-identity-and-access-management)
  - [IAM BEST PRACTICES](#iam-best-practices)
  - [basics](#basics)
    - [to use AWS IAM](#to-use-aws-iam)
  - [essential components](#essential-components)
  - [The IAM console](#the-iam-console)
  - [IAM policy](#iam-policy)
    - [Inline Policies vs Managed Policies vs Custom Policies](#inline-policies-vs-managed-policies-vs-custom-policies)
    - [**Identity-based policies**](#identity-based-policies)
    - [**Resource-based policies**](#resource-based-policies)
    - [**Service control policies (SCPs)**](#service-control-policies-scps)
    - [**Permissions boundaries**](#permissions-boundaries)
      - [Evaluating effective permissions with boundaries](#evaluating-effective-permissions-with-boundaries)
      - [Identity-based policies with boundaries](#identity-based-policies-with-boundaries)
      - [Resource-based policies](#resource-based-policies-1)
      - [Organizations SCPs](#organizations-scps)
      - [Session policies](#session-policies)
      - [Delegate 托付 responsibility to others using permissions boundaries](#delegate-托付-responsibility-to-others-using-permissions-boundaries)
  - [IAM Entity](#iam-entity)
    - [root account](#root-account)
    - [IAM users](#iam-users)
    - [IAM group](#iam-group)
    - [IAM roles](#iam-roles)
  - [AWS Organizations](#aws-organizations)

---


# AWS - IAM Identity and Access Management

<img alt="pic" src="https://i.imgur.com/ZW9dsDI.png" width="400">

---


## IAM BEST PRACTICES
- Lock away the AWS root user access keys.
  - <font color=OrangeRed> no access key for the root account user </font>
- not use the root account for anything other than billing.
  - Power user access allows all permissions except the management of groups and users in IAM.

- Create <font color=OrangeRed> individual IAM users </font>
- Use AWS defined `policies` to assign permissions whenever possible.
- <font color=OrangeRed> Use groups to assign permissions </font> to IAM users.
- Grant least privilege.
- Use access levels to review IAM permissions.
- <font color=OrangeRed> Use roles for applications </font> that run on AWS EC2 instances.
- Delegate by using roles instead of sharing credentials.
- Configure a strong password policy for users.
- <font color=OrangeRed> Enable MFA for all users </font>
- Rotate credentials regularly.
- Remove unnecessary credentials.
- Use policy conditions for extra security.
- Monitor activity in your AWS account.
- Use <font color=OrangeRed> Temporary Security Credentials (IAM Roles) </font> Instead of Long-Term Access Keys.
- Manage IAM User Access Keys Properly.

---


## basics

> 颗粒状的 Granular permissions

- a tool that centrally manages access to <font color=OrangeRed> launching, configuring, managing, and terminating resources in the AWS account </font>

- grant different permissions to different people for different resources. 
  - **who, which, how**

- feature of the AWS account, no additional charge.



> IAM has the following features to control access:


- **provides Granular permissions** over access to resources, IAM can be used to manage:
  - provides <font color=OrangeRed> 颗粒状的 Granular permissions </font>
    - grant different permissions to different people / resources.
  - Users. Groups. Access policies. Roles.
  - User credentials. User password policies.
  - for AWS Management Console, AWS CLI, or AWS software development kits (SDKs),
    - every call to an AWS service is an API call.
  - API keys for programmatic access (CLI).
    - including the ability to <font color=OrangeRed> specify exactly which API calls the user is authorized to make to each service </font>



- **Shared access**
  - grant other people permission to administer and use resources in the AWS account
  - without having to share your password or access key.

- **Secure access** to AWS resources
  - Integrated with may AWS services.
  - manage access to AWS services and resources securely.
  - Secure access to AWS resources for applications that run on EC2.
  - create and manage AWS users and groups.
    - should use groups to assign permissions to IAM users
    - should <font color=OrangeRed> avoid embedding access keys in application code </font>

- **Temporary security credentials**
  - IAM can assign temporary security credentials to provide users with temporary access to services/resources.
  - AWS access key ID, secret access key, and security token.

- **Multi-factor authentication (MFA)**
  - Add two-factor authentication to the account and to individual users
  - extra security.
  - authentication device that generates random, six-digit, single-use authentication codes
  - authenticate using an MFA device in the following two ways:
    - `AWS Management Console`: user name, password and authentication code.
    - `AWS API`: restrictions are added to IAM policies and developers can request temporary security credentials and pass MFA parameters in their AWS STS API requests.
    - `AWS CLI`: obtaining temporary security credentials from STS (aws sts get-session-token).

- **Identity federation**
  - Identity Federation (including AD, Facebook etc.) can be configured
  - allow users who already have passwords elsewhere (corporate network) to get temporary access to the AWS account.
  - allowing secure access to resources in an AWS account `without creating an IAM user account`.
  - cannot use IAM to create local user accounts on any system.

- **Eventually consistent**


> IAM is <font color=OrangeRed> not used for application-level authentication </font>

> IAM is <font color=OrangeRed> universal (global)</font> and does not apply to regions.



- Identity information for assurance.


- PCI DSS compliance.


### to use AWS IAM

- AWS Management Console.
- AWS Command Line Tools.
- AWS SDKs.
  - recommend use AWS SDKs to make programmatic API calls to IAM.
- IAM HTTPS API.
- can also use IAM Query API to make direct calls to the IAM web service.
- sign-in URL:
  - `https://AWS_Account_ID.signin.aws.amazon.com/console/`
   - `https://console.aws.amazon.com/.`




## essential components

- `IAM user`:
  - a `person/application` that is defined in an AWS account, and that must make API calls to AWS products.
  - Each user must have a unique name (no spaces in name) within the AWS account,
  - and a set of security credentials that are different from the AWS account root user security credentials.
  - Each user is defined in one and only one AWS account.

- `IAM group`:
  - a collection of users.
  - use groups to `simplify specifying and managing permissions for multiple users`.

- `IAM policy`:
  - a document that defines permissions to determine what users can do in the AWS account.
  - A policy typically `grants access to specific resources to user, or explicitly deny access`.

- `IAM role`:
  - a tool for granting temporary access to specific AWS resources in an AWS account.
  - only selected users or applications.
  - Aws service can access other service.


Use `IAM Policies` to control access to the following:
- `AWS for Principals`
  - Control what the person making the request (theprincipal) is allowed to do.
- `IAM Identities`
  - Control which `IAM identities (groups, users, and roles)` can be accessed and how.
- `IAM Policies`
  - Control who can create, edit, and delete customer managed policies,
  - and who can attach and detach all managed policies.
- `AWS Resources`
  - Control who has access to resources
  - using an `identity-based policy` or a `resource-based policy`.
- `AWS Accounts`
  - Control whether a request is allowed only for members of a specific account.

￼![Screen Shot 2020-06-08 at 12.20.26](https://i.imgur.com/c8OIchz.png)


---



## The IAM console
- provides information about when IAM users and roles last attempted to access AWS services. This information is called `service last accessed data`.
  - help you identify unnecessary permissions
  - to refine your IAM policies
  - to better adhere to the principle of “least privilege.”
  - granting the minimum permissions required to perform a specific task.
- You can find the data on the Access Advisor tab in the IAM console by examining the detail view for any IAM user, group, role, or managed policy.



---


## IAM policy

- By default

- <font color=OrangeRed> the AWS account Root user has full access </font>

- <font color=OrangeRed> the AWS account IAM user has no access to any services </font>

  - All permissions are denied by default.
    - default AWS account users do not have any permissions to any resources/data in AWS account
    - The most restrictive policy is applied.

  - default <font color=LightSlateBlue> implicit deny </font> of an IAM identity can <font color=OrangeRed> be overridden</font> with an <font color=LightSlateBlue> explicit allow </font>
    - must <font color=LightSlateBlue> explicitly grant permissions </font> to a user/group/role by `creating a policy`
    - attaching an IAM access policy to IAM user/group


- When there is a conflict, the most restrictive policy applies.
    - <font color=OrangeRed>  allow vs deny: deny win </font>

- a document in `JavaScript Object Notation (JSON)` format
  - lists permissions that `allow / deny` access to resources in the AWS account.

- follow the principle of least privilege

- `the scope` of the service configurations `is global`.
  - The settings are not defined at an AWS Region level.
  - settings apply across all AWS Regions.


- Resources are defined using the `ARN format`
  - the syntax for ARNs
  - `arn:partition:service:region:account-id:`


3 types of policy:
- `+` **Identity-based policies** (user start with no permission, add Allow)
- `-` **Permission boundary** (setup limit for user Identity-Based policy)
- `+` **Resource-based policies** (add additional permission, not for role)
- `-` **Service control policies (SCPs)**



![Screen Shot 2022-03-23 at 11.09.26](https://i.imgur.com/wfT1Ox7.png)


Overall:
- All must in `Permission boundary && Policy`:
  - Deny <- in policy not in permission boundary
- All must not been deny by SCPs


---

### Inline Policies vs Managed Policies vs Custom Policies

**Managed policies**
- created and administered by AWS
  - prebuild, Standalone identity-based policies
  - cannot change
  - AWS managed policies have automatic updates.
  - has overhead, more rigid out of the two.
- for common use cased based on job function:
  - `AmazonDynamoDBFullAccess`, `AWSCodeCOmmitPowerUser`, `AmazonEC2ReadOnlyAccess`
- one policy can
  - assign to multiple users/groups/roles
  - in <font color=OrangeRed> same/different AWS account </font>
- A Managed Policy `applies policies` to a user, group, or role (without exceptions).



**Customer managed policy**:
- managed by you
- Standalone policy user create
- more flexible but requires administration.
- policy can
  - assign to multiple users/groups/roles
  - in <font color=OrangeRed> only your AWS account </font>



**Inline policies**
- managed by you
- embedded directly to a single user/group/role to which it aaplies.
  - when user/group/role been deleted, the policy also be deleted
- policy can
  - assign to one users/groups/roles
  - <font color=OrangeRed> strict 1:1 relationship between entity and the policy </font>
  - in <font color=OrangeRed> only your AWS account </font>
- usually Inline Policies are used <font color=LightSlateBlue> to create exceptions </font> to a user, group, or role.
  - when you want to be sure that the permissions is not been assigned to any other user.

> create in the user, add inline policy


---

### **Identity-based policies**
- A policy that is attached to an identity in IAM
  - less overhead to use a SCP for the entire AWS account.
  - permissions policies that attach to a principal/identity (user/role/group).

- <font color=OrangeRed> control what actions that identity can perform, on which resources, and under what conditions </font>

- Identity-based policies categorized:
  - **Managed policies**
    - prebuild, Standalone identity-based policies
    - can attach to multiple users/groups/roles in AWS account
    - A Managed Policy `applies policies` to a user, group, or role (without exceptions).
      - **customer managed policy**:
        - more flexible but requires administration.
      - **AWS managed policy**
        - has overhead, more rigid out of the two.
        - AWS managed policies have automatic updates.
  - **Inline policies**
    - Policies embedded directly to a single user/group/role
    - Inline Policies are used to create exceptions to a user, group, or role.

---

### **Resource-based policies**
- <font color=OrangeRed> JSON policy documents that attach to a resource </font> (S3 bucket...)
- <font color=OrangeRed> control what actions a specified principal can perform on that resource, and under what conditions </font>

- **inline only**:
  - define the policy on the resource itself, instead of creating a separate policy document that you attach.
  - For example
    - create an S3 bucket policy (a type of resource-based policy) on an S3 bucket
    - -> the bucket
    - -> Permissions tab
    - -> Bucket Policy button
    - -> define the JSON-formatted policy document there.

- An `Amazon S3 access control list (ACL)` is another example of a resource-based policy

![HVBkIYM](https://i.imgur.com/FW1kVeh.png)

> identity-based policy.
> - An policy that grants access to the S3 bucket is attached to the MaryMajor user.

> resource-based policy.
> - The S3 bucket policy for the `photos bucket` specifies that the user MaryMajor is allowed to list and read the objects in the bucket.
> - An explicit deny statement will always take precedence over any allow statement.
> - could define a deny statement in a bucket policy to restrict access to specific users, even if the users are granted access in a separate identity-based policy.
￼
![X79K6Ni](https://i.imgur.com/MtihYSq.png)

determines permissions
**explicit denial policy -> explicit allow policy -> deny**


Resource-based policies > Identity-based policy


---

### **Service control policies (SCPs)**

- one type of policy

- use <font color=OrangeRed> to manage organization </font>
  - Attaching an SCP to an AWS Organizations entity (root, OU, or account)
  - defines a guardrail for what actions the principals can perform.

- enables <font color=OrangeRed> permission controls </font>
  - can <font color=LightSlateBlue> limit account usage </font> to organizational units or linked accounts.
  - offer <font color=OrangeRed> central control </font> over the maximum available permissions <font color=LightSlateBlue> for all accounts in organization </font>
  - ensure accounts stay in organization’s access control guidelines.

- available only in an organization that <font color=OrangeRed> has all features enabled </font>
  - SCPs are not automatically enabled;
  - including consolidated billing
    - SCPs aren't available if organization has enabled only the consolidated billing feature

- <font color=OrangeRed> restrict the root user of an Organization Unit account </font>
  - SCP is a way to restrict a root user on an account.
  - defines a safeguard for the actions that accounts in the organization root or OU can do.
  - Attaching an SCP to the organization root/unit (OU)
    - Log in to the master account and create the SCP
    - Select the <font color=LightSlateBlue> Organizational Unit </font>
    - <font color=LightSlateBlue> Enable the SCP </font> for the Organizational Unit
    - Attach the SCP to the member account within the Organizational Unit

- <font color=OrangeRed> not a substitute for well-managed each account </font>
  - still need attach IAM policies to users/roles in organization's accounts
  - to actually grant permissions to them.

- similar to IAM permissions policies
  - almost the same syntax. JSON
  - but, SCP policies <font color=LightSlateBlue> never grants permissions. </font>
    - <font color=OrangeRed> it the maximum permissions </font> for an organization or OU.

- <font color=OrangeRed> No permissions are granted by an SCP </font>
  - it defines a guardrail, or sets limits, on the actions that the account's administrator can delegate to the IAM users/roles in the affected accounts.
    - The administrator must still attach `identity/resource-based policies` to IAM users/roles, or to the resources in accounts to actually grant permissions.
  - The <font color=LightSlateBlue> effective permissions </font>
    - the logical intersection between **what is allowed by the SCP** and **what is allowed by the IAM/Resource-based policies**
  - Important
    - SCPs don't affect users or roles in the management account.
    - affect only the member accounts in the organization.

- by default `FullAWSAccess`
  - a service control policy
  - allows users to access services/resources on an attached account.
  - allows access to all AWS services within an attached member account


---



### **Permissions boundaries**


![permissions_boundary](https://i.imgur.com/tnA8au6.png)


- an advanced feature

- AWS supports `permissions boundaries` for IAM entities (users or roles)

- using a managed policy to set the maximum permissions that an <font color=LightSlateBlue> identity-based policy can grant to an IAM entity </font>
- An entity's permissions boundary allows it to <font color=OrangeRed> perform only the actions that are allowed by both its identity-based policies and Permissions boundaries </font>

- can use an <font color=LightSlateBlue> AWS managed policy </font> or a <font color=LightSlateBlue> customer managed policy </font> to set the boundary for an IAM entity (user or role).

- That policy limits the maximum permissions for the user or role.


Example:

```json
// assume IAM user `ShirleyRodriguez` is allowed to manage only Amazon S3, Amazon CloudWatch, and Amazon EC2.
// To enforce this rule, use the following policy to set the permissions boundary for the `ShirleyRodriguez` user:
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "cloudwatch:*",
                "ec2:*"
            ],
            "Resource": "*"
        }
    ]
}
```

- When you use a policy to set the permissions boundary for a user
  - it limits the user's permissions but does not provide permissions on its own.

- example:
  - the policy sets the maximum permissions of `ShirleyRodriguez` as all operations in Amazon S3, CloudWatch, and Amazon EC2.
  -<font color=OrangeRed>  Shirley can never perform operations in any other service, including IAM, even if she has a permissions policy that allows it </font>.

  - you can add the following policy to the `ShirleyRodriguez` user:
  - allows creating a user in IAM.
  - If you attach this permissions policy to the `ShirleyRodriguez` user, and Shirley tries to create a user, the operation fails.
  - It fails because the permissions boundary does not allow the `iam:CreateUser` operation.

  - Given these two policies, Shirley does not have permission to perform any operations in AWS.
  - You must add a different permissions policy to allow actions in other services, such as Amazon S3.
  - Alternatively, you could update the permissions boundary to allow her to create a user in IAM.

```json

{
  "Version": "2012-10-17",
  "Statement": {
    "Effect": "Allow",
    "Action": "iam:CreateUser",
    "Resource": "*"
  }
}
```

---

#### Evaluating effective permissions with boundaries

The permissions boundary for an IAM entity (user or role) sets the maximum permissions that the entity can have.
- This can change the effective permissions for that user or role.
- The effective permissions for an entity are the permissions that are granted by all the policies that affect the user or role.

- Within an account, the permissions for an entity can be affected by
  - identity-based policies,
  - resource-based policies,
  - permissions boundaries,
  - Organizations SCPs
  - or session policies.

- If any one of these policy types explicitly denies access for an operation, then the request is denied.
- The permissions granted to an entity by multiple permissions types are more complex.
- check [Policy evaluation logic]().

---

#### Identity-based policies with boundaries

Identity-based policies
- are <font color=OrangeRed> inline or managed policies attached to a user, group of users, or role </font>

- effective permissions
  - Identity-based policies grant permission to the entity
  - and <kbd>Permissions boundaries</kbd> limit those permissions.
  - The effective permissions are the intersection of both policy types.
  - An explicit deny in either of these policies overrides the allow.

![permissions_boundary](https://i.imgur.com/tnA8au6.png)

---

#### Resource-based policies

**Resource-based policies**
![EffectivePermissions-rbp-boundary-id](https://i.imgur.com/IaeaipQ.png)

- control how the specified principal can access the resource to which the policy is attached.

1. <font color=OrangeRed> Resource-based policies for IAM users </font>
   - Within an account
     - an <font color=LightSlateBlue> implicit deny in a permissions boundary </font> <font color=OrangeRed> does not limit the permissions granted </font> to an IAM user by a resource-based policy.
   - Permissions boundaries reduce permissions that are granted to a user by identity-based policies.
   - Resource-based policies can provide additional permissions to the user.

2. <font color=OrangeRed>Resource-based policies for IAM roles and federated users </font>
   - Within an account
     - an <font color=LightSlateBlue> implicit deny in a permissions boundary </font> <font color=OrangeRed> does limit the permissions granted </font>  to the ARN of the underlying IAM role/user by the resource-based policy.
   - However
     - <font color=LightSlateBlue> if resource-based policy grants permissions directly to the session principal </font> (the assumed-role ARN or federated user ARN)
     - an <font color=LightSlateBlue> implicit deny in the permissions boundary </font> <font color=OrangeRed> does not limit those permissions </font>
   - [Session policies](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies.html#policies_session).

---

#### Organizations SCPs

![EffectivePermissions-scp-boundary-id](https://i.imgur.com/UfyiKlF.png)

SCPs
- are applied to an entire AWS account.
- limit permissions for every request made by a principal within the account.

- An IAM entity (user or role) can make a request that is affected by an SCPs, a permissions boundary, and an identity-based policy.
  - the request is allowed only if all three policy types allow it.
  - The effective permissions are the intersection of all three policy types.
  - An explicit deny in any of these policies overrides the allow.

account member in AWS Organizations.
- Organization members might be affected by an SCPs
- To view this data using the AWS CLI command or AWS API operation, permissions: `organizations:DescribeOrganization` action for your Organizations entity
- You must have additional permissions to perform the operation in the Organizations console.

---

#### Session policies

![EffectivePermissions-session-boundary-id](https://i.imgur.com/LCcnM4u.png)

Session policies
- advanced policies
- pass as a parameter when programmatically create a temporary session for a role or federated user.
- The permissions for a session come from the `IAM entity (user or role) used` to create the session and from the session policy.
- The entity's identity-based policy permissions are limited by the session policy and the permissions boundary.
  - The effective permissions for this set of policy types are the intersection of all three policy types.
  - An explicit deny in any of these policies overrides the allow.

---

#### Delegate 托付 responsibility to others using permissions boundaries

use <kbd>Permissions boundaries</kbd> to delegate permissions management tasks
- such as user creation, to IAM users in your account.
- This permits others to perform tasks on your behalf within a specific boundary of permissions.

Example
- María is the administrator of the X-Company AWS account.
  - She wants to delegate user creation duties to Zhang.
  - However, she must ensure that Zhang creates users that adhere to the following company rules:
    * Users cannot use IAM to create or manage users, groups, roles, or policies.
    * Users are denied access to the Amazon S3 `logs` bucket and cannot access the `i-1234567890abcdef0` Amazon EC2 instance.
    * Users cannot remove their own boundary policies.

- To enforce these rules, María completes the following tasks
  1. María creates the `XCompanyBoundaries` managed policy
     1. to use as a permissions boundary for all new users in the account.
  2. María creates the `DelegatedUserBoundary` managed policy
     1. and assigns it as the permissions boundary for Zhang.
     2. Maria makes a note of her admin IAM user's ARN and uses it in the policy to prevent Zhang from accessing it.
  3. María creates the `DelegatedUserPermissions` managed policy
     1. and attaches it as a permissions policy for Zhang.
  4. María tells Zhang about his new responsibilities and limitations.


**Task 1:**

María must first create a managed policy to define the boundary for the new users.
- María will allow Zhang to give users the permissions policies they need, but she wants those users to be restricted.
- To do this, she creates the following customer managed policy with the name `XCompanyBoundaries`.
- This policy does the following:
  * Allows users full access to several services
  * Allows limited self-managing access in the IAM console.
    * This means they can change their password after signing into the console.
    * They can't set their initial password.
    * To allow this, add the `"*LoginProfile"` action to the `AllowManageOwnPasswordAndAccessKeys` statement.
  * Denies users access to the Amazon S3 logs bucket or the `i-1234567890abcdef0` Amazon EC2 instance


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            // allows full access to the specified AWS services.
            // This means that a new user's actions in these services are limited only by the permissions policies that are attached to the user.
            "Sid": "ServiceBoundaries",
            "Effect": "Allow",
            "Action": [
                "s3:*",
                "cloudwatch:*",
                "ec2:*",
                "dynamodb:*"
            ],
            "Resource": "*"
        },
        {
            // allows access to list all IAM users.
            // This access is necessary to navigate the **Users** page in the AWS Management Console.
            // It also allows viewing the password requirements for the account, which is necessary when changing your own password.
            "Sid": "AllowIAMConsoleForCredentials",
            "Effect": "Allow",
            "Action": [
                "iam:ListUsers",
                "iam:GetAccountPasswordPolicy"
            ],
            "Resource": "*"
        },
        {
            // allows the users manage only their own console password and programmatic access keys.
            // This is important if Zhang or another administrator gives a new user a permissions policy with full IAM access.
            // In that case, that user could then change their own or other users' permissions.
            // This statement prevents that from happening.
            "Sid": "AllowManageOwnPasswordAndAccessKeys",
            "Effect": "Allow",
            "Action": [
                "iam:*AccessKey*",
                "iam:ChangePassword",
                "iam:GetUser",
                "iam:*ServiceSpecificCredential*",
                "iam:*SigningCertificate*"
            ],
            "Resource": ["arn:aws:iam::*:user/${aws:username}"]
        },
        {
            // explicitly denies access to the `logs` bucket.
            "Sid": "DenyS3Logs",
            "Effect": "Deny",
            "Action": "s3:*",
            "Resource": [
                "arn:aws:s3:::logs",
                "arn:aws:s3:::logs/*"
            ]
        },
        {
            // explicitly denies access to the `i-1234567890abcdef0` instance.
            "Sid": "DenyEC2Production",
            "Effect": "Deny",
            "Action": "ec2:*",
            "Resource": "arn:aws:ec2:*:*:instance/i-1234567890abcdef0"
        }
    ]
}
```

**Task 2:**

María wants to allow Zhang to create all X-Company users, but only with the `XCompanyBoundaries` permissions boundary.
- She creates the following customer managed policy named `DelegatedUserBoundary`.
  - This policy defines the maximum permissions that Zhang can have.
  - Each statement serves a different purpose:
  1. The `CreateOrChangeOnlyWithBoundary` statement allows Zhang to create IAM users but only if he uses the `XCompanyBoundaries` policy to set the permissions boundary. This statement also allows him to set the permissions boundary for existing users but only using that same policy. Finally, this statement allows Zhang to manage permissions policies for users with this permissions boundary set.
  2. The `CloudWatchAndOtherIAMTasks` statement allows Zhang to complete other user, group, and policy management tasks. He has permissions to reset passwords and create access keys for any IAM user not listed in the condition key. This allows him to help users with sign-in issues.
  3. The `NoBoundaryPolicyEdit` statement denies Zhang access to update the `XCompanyBoundaries` policy. He is not allowed to change any policy that is used to set the permissions boundary for himself or other users.
  4. The `NoBoundaryUserDelete` statement denies Zhang access to delete the permissions boundary for himself or other users.
- María then assigns the `DelegatedUserBoundary` policy <font color=OrangeRed> as the permissions boundary </font> for the `Zhang` user.


```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            // allows Zhang to create IAM users but only if he uses the `XCompanyBoundaries` policy to set the permissions boundary.
            // allows him to set the permissions boundary for existing users but only using that same policy.
            // allows Zhang to manage permissions policies for users with this permissions boundary set.
            "Sid": "CreateOrChangeOnlyWithBoundary",
            "Effect": "Allow",
            "Action": [
                "iam:CreateUser",
                "iam:DeleteUserPolicy",
                "iam:AttachUserPolicy",
                "iam:DetachUserPolicy",
                "iam:PutUserPermissionsBoundary",
                "iam:PutUserPolicy"
            ],
            "Resource": "*",
            "Condition": {
                "StringEquals": {
                    "iam:PermissionsBoundary": "arn:aws:iam::123456789012:policy/XCompanyBoundaries"
                }
            }
        },
        {
            // allows Zhang to complete other user, group, and policy management tasks.
            // He has permissions to reset passwords and create access keys for any IAM user not listed in the condition key.
            // This allows him to help users with sign-in issues.
            "Sid": "CloudWatchAndOtherIAMTasks",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:*",
                "iam:GetUser",
                "iam:ListUsers",
                "iam:DeleteUser",
                "iam:UpdateUser",
                "iam:CreateAccessKey",
                "iam:CreateLoginProfile",
                "iam:GetAccountPasswordPolicy",
                "iam:GetLoginProfile",
                "iam:ListGroups",
                "iam:ListGroupsForUser",
                "iam:CreateGroup",
                "iam:GetGroup",
                "iam:DeleteGroup",
                "iam:UpdateGroup",
                "iam:CreatePolicy",
                "iam:DeletePolicy",
                "iam:DeletePolicyVersion",
                "iam:GetPolicy",
                "iam:GetPolicyVersion",
                "iam:GetUserPolicy",
                "iam:GetRolePolicy",
                "iam:ListPolicies",
                "iam:ListPolicyVersions",
                "iam:ListEntitiesForPolicy",
                "iam:ListUserPolicies",
                "iam:ListAttachedUserPolicies",
                "iam:ListRolePolicies",
                "iam:ListAttachedRolePolicies",
                "iam:SetDefaultPolicyVersion",
                "iam:SimulatePrincipalPolicy",
                "iam:SimulateCustomPolicy"
            ],
            "NotResource": "arn:aws:iam::123456789012:user/Maria"
        },
        {
            // denies Zhang access to update the `XCompanyBoundaries` policy.
            // He is not allowed to change any policy that is used to set the permissions boundary for himself or other users.
            "Sid": "NoBoundaryPolicyEdit",
            "Effect": "Deny",
            "Action": [
                "iam:CreatePolicyVersion",
                "iam:DeletePolicy",
                "iam:DeletePolicyVersion",
                "iam:SetDefaultPolicyVersion"
            ],
            "Resource": [
                "arn:aws:iam::123456789012:policy/XCompanyBoundaries",
                "arn:aws:iam::123456789012:policy/DelegatedUserBoundary"
            ]
        },
        {
            // denies Zhang access to delete the permissions boundary for himself or other users.

            "Sid": "NoBoundaryUserDelete",
            "Effect": "Deny",
            "Action": "iam:DeleteUserPermissionsBoundary",
            "Resource": "*"
        }
    ]
}
```




**Task 3:**

- the <font color=OrangeRed> permissions boundary </font>
  - limits the maximum permissions
  - does not grant access on its own,
  - Maria must create a permissions policy for Zhang.
- She creates the following policy named `DelegatedUserPermissions`.
  - This policy defines the operations that Zhang can perform, within the defined boundary.
  - Each statement serves a different purpose:
    1. The `IAM` statement of the policy allows Zhang full access to IAM. However, because his permissions boundary allows only some IAM operations, his effective IAM permissions are limited only by his permissions boundary.
    2. The `CloudWatchLimited` statement allows Zhang to perform five actions in CloudWatch. His permissions boundary allows all actions in CloudWatch, so his effective CloudWatch permissions are limited only by his permissions policy.
    3. The `S3BucketContents` statement allows Zhang to list the `ZhangBucket` Amazon S3 bucket. However, his permissions boundary does not allow any Amazon S3 action, so he cannot perform any S3 operations, regardless of his permissions policy.
  - Note
    - Zhang's policies allow him to create a user that can then access Amazon S3 resources that he can't access.
    - By delegating these administrative actions, Maria effectively trusts Zhang with access to Amazon S3.

- María then attaches the `DelegatedUserPermissions` policy as the permissions policy for the `Zhang` user.

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            // allows Zhang full access to IAM.
            // However, because his permissions boundary allows only some IAM operations, his effective IAM permissions are limited only by his permissions boundary.
            "Sid": "IAM",
            "Effect": "Allow",
            "Action": "iam:*",
            "Resource": "*"
        },
        {
            // allows Zhang to perform five actions in CloudWatch.
            // His permissions boundary allows all actions in CloudWatch, so his effective CloudWatch permissions are limited only by his permissions policy.
            "Sid": "CloudWatchLimited",
            "Effect": "Allow",
            "Action": [
                "cloudwatch:GetDashboard",
                "cloudwatch:GetMetricData",
                "cloudwatch:ListDashboards",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:ListMetrics"
            ],
            "Resource": "*"
        },
        {
            // allows Zhang to list the `ZhangBucket` Amazon S3 bucket.
            // However, his permissions boundary does not allow any Amazon S3 action, so he cannot perform any S3 operations, regardless of his permissions policy.
            "Sid": "S3BucketContents",
            "Effect": "Allow",
            "Action": "s3:ListBucket",
            "Resource": "arn:aws:s3:::ZhangBucket"
        }
    ]
}
```


**Task 4:**

She gives Zhang instructions to create a new user.
- She tells him that he can create new users with any permissions that they need,
- but he must assign them the `XCompanyBoundaries` policy as a permissions boundary.

- Zhang completes the following tasks:
  1. Zhang creates a user with the AWS Management Console.
     1. He types the user name `Nikhil` and enables console access for the user.
     2. He clears the checkbox next to **Requires password reset**, because the policies above allow users to change their passwords only after they are signed in to the IAM console.
  2. On the **Set permissions** page
     1. Zhang chooses the **IAMFullAccess** and **AmazonS3ReadOnlyAccess** permissions policies that allow Nikhil to do his work.
  3. Zhang skips the **Set permissions boundary** section
     1. <font color=OrangeRed> forgetting María's instructions </font>
  4. Zhang reviews the user details and chooses **Create user**.
     1. The operation fails and access is denied.
     2. Zhang's `DelegatedUserBoundary` permissions boundary requires that any user he creates have the `XCompanyBoundaries` policy used as a permissions boundary.
  5. Zhang returns to the previous page.
     1. In the **Set permissions boundary** section, he chooses the `XCompanyBoundaries` policy.
  6. Zhang reviews the user details and chooses **Create user**.
  7. The user is created.

- When Nikhil signs in
  - he has access to IAM and Amazon S3
  - except those operations that are denied by the permissions boundary.
  - For example
    - he can change his own password in IAM but can't create another user or edit his policies.
    - Nikhil has read-only access to Amazon S3.

- If someone adds a resource-based policy to the `logs` bucket that allows Nikhil to put an object in the bucket, he still cannot access the bucket.
  - The reason
  - any actions on the `logs` bucket are explicitly denied by his permissions boundary.
  - An explicit deny in any policy type results in a request being denied.

- However
  - if a resource-based policy attached to a Secrets Manager secret allows Nikhil to perform the `secretsmanager:GetSecretValue` action, then Nikhil can retrieve and decrypt the secret.
  - The reason is that Secrets Manager operations are not explicitly denied by his permissions boundary, and implicit denies in <kbd>Permissions boundaries</kbd> do not limit resource-based policies.





---


## IAM Entity

---

### root account


The root account has full administrative permissions and these cannot be restricted.

- Best practice for root accounts:
  - Don’t use the root user credentials.
  - Don’t share the root user credentials.
  - Create an IAM user and assign administrative permissions as required.
  - Enable MFA.

---

### IAM users

- maximum amount of IAM users per account: 5,000
- IAM users can be created to represent applications and these are known as “service accounts”.
- Each user account has a friendly name and an <font color=OrangeRed> ARN </font> which uniquely identifies the user across AWS.
    - A unique ID is also created which is returned only when you create the user using the API, Tools for Windows PowerShell or the AWS CLI.

> You should create individual IAM accounts for users (best practice not to share accounts).


authenticate: how the user is permitted to use to access AWS resources.
- 2 types: 
  - programmatic access 
  - AWS Management Console access.
  - only or both


- **programmatic access**:
  - `access key ID` and a `secret access key`
    - cannot be used to login to the AWS console.
    - can only be used once and must be regenerated if lost.
  - to make an `AWS API call` by `AWS CLI/SDK/other development tool`.


- **AWS Management Console access**
  - browser login window.
    - 12-digit account ID / corresponding account alias.
    - `user name and password`
  - If multi-factor authentication (MFA) is enabled: an authentication code.
    - With MFA, users and systems must provide an `MFA token + the regular sign-in credentials`, before access AWS services and resources.
    - **for generating the MFA authentication token**:
      - `virtual MFA-compliant applications`(Google Authenticator / Authy 2-Factor Authentication...),
      - `U2F security key devices` (Yubikey)
      - `hardware MFA devices` (Gemalto)

![dwVKXzD](https://i.imgur.com/Fbc0udg.png)


---


### IAM group
Important characteristics of groups:
- A group can contain many users
- a user can belong to multiple groups.
- **Groups cannot be nested**.
  - A group can contain only users,
  - a group cannot contain other groups.
- There is `no default group` that automatically includes all users in the AWS account.
- group with all account users in it, you need to create the group and add each new user to it.
- A group is not an identity and `cannot be identified as a principal in an IAM policy`.

---

### IAM roles

![ilJwlvj](https://i.imgur.com/W0u4eW2.png)

- an identity in account that has specific permissions.
- is an AWS identity that can attach permissions policies
- but instead of being uniquely associated with one person, a role is `intended to be assumable by anyone who needs it.`
- an IAM entity that defines a set of permissions for making AWS service requests.

- Roles can be assumed temporarily through the console or programmatically with the AWS CLI, Tools for Windows PowerShell or API.


- not using permanent credentials
  - `does not have standard long-term credentials` (password/access keys associated with it...)
  - assume a role, the role provides `temporary security credentials` for role session.
  - Temporary credentials are primarily used with IAM roles and automatically expire.
  - IAM users or AWS services can assume a role to obtain temporary security credentials that can be used to make AWS API calls.


- IAM roles are not associated with a specific user or group.
  - Instead, trusted entities assume roles, such as IAM users, applications, or AWS services such as EC2.
  - delegate permissions to resources for users and services
  - IAM users can temporarily assume a role to take on permissions for a specific task.


- assign limitation
  - A role can be assigned to a federated user who signs in using an external identity provider.
  - an IAM user in the same AWS account as the role or a user in a different AWS account.
  - but cannot apply multiple roles to a single instance.


- allowed to assume IAM Roles
  - `IAM Users`
    - When an IAM User is needing elevated permissions for a temporary task
  - `External accounts`
    - grant access to your account to third parties to perform an audit on your resources.
    - When a trusted remote account needs access to AWS resources
  - `AWS services/resources`
    - When an AWS service or resource needs access to other AWS service or resource
  - `Applications`
    - allow a mobile app to use AWS resources, but do not want to embed AWS keys within the app (difficult to rotate and can potentially extract).
    - When an external application needs access to an AWS resource like `DynamoDB`
  - **IAM Groups are not allowed to assume IAM Roles**.

- use roles to `delegate 托付 access to users/app/services` that do not normally have access to your AWS resources.
  - For example
  - grant users in the AWS account access to resources don't usually have, or grant users in one AWS account access to resources in another account.
  - grant AWS access to users who already have identities that are defined outside of AWS, such as in your corporate directory.


- two types of policies in an IAM Role
  - The `trust policy`
    - allows identities to assume roles
  - the `permission policy`
    - defines the permissions provided.
    - A permissions policy must also be attached to the user in the trusted account.

- Wildcards (`*`) cannot be specified as a principal.

- For all of these example use cases, roles are an essential component to implementing the cloud deployment.


- IAM roles with EC2 instances:
  - IAM roles can be used for granting applications running on EC2 instances permissions to AWS API requests using instance profiles.
  - Only one role can be assigned to an EC2 instance at a time.
  - A role can be assigned at the EC2 instance creation time or at any time afterwards.
  - When using the AWS CLI or API instance profiles must be created manually (it’s automatic and transparent through the console).
  - Applications retrieve temporary security credentials from the instance metadata.








---


## AWS Organizations


- With AWS Organizations, **Consolidated Billing** is always enabled.
  - All other features are either enabled / disabled as a group
  - cannot individually enable or disable a feature - it's all or nothing
