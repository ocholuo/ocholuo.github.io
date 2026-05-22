---
title: GitHub - A successful Git branching model
date: 2020-11-11 11:11:11 -0400
categories: [00CodeNote, SourceMagr]
tags: [git]
toc: true
image:
---

- [A successful Git branching model 成功的 Git 分支模型](#a-successful-git-branching-model-成功的-git-分支模型)
  - [The main branches 主要分支](#the-main-branches-主要分支)
  - [Supporting branches 辅助分支](#supporting-branches-辅助分支)
    - [Feature branches 功能分支](#feature-branches-功能分支)
    - [Release branches 发布分支](#release-branches-发布分支)
    - [Hotfix branches 热修复分支](#hotfix-branches-热修复分支)
  - [Cherry-Pick: Surgical Back-Porting 精准回移](#cherry-pick-surgical-back-porting-精准回移)
    - [何时使用 `cherry-pick` 对比 `merge --no-ff`](#何时使用-cherry-pick-对比-merge---no-ff)
    - [Scenario: release branch is live, main has new features in flight 场景：发布分支已上线](#scenario-release-branch-is-live-main-has-new-features-in-flight-场景发布分支已上线)
    - [Step-by-step cherry-pick workflow 分步操作流程](#step-by-step-cherry-pick-workflow-分步操作流程)
    - [Cherry-picking a range of commits 区间 cherry-pick](#cherry-picking-a-range-of-commits-区间-cherry-pick)
    - [Handling conflicts during cherry-pick 处理冲突](#handling-conflicts-during-cherry-pick-处理冲突)
    - [`merge --no-ff` vs `cherry-pick`: tradeoffs 权衡对比](#merge---no-ff-vs-cherry-pick-tradeoffs-权衡对比)
    - [Key rules 关键规则](#key-rules-关键规则)

---

## A successful Git branching model 成功的 Git 分支模型

[link](https://nvie.com/posts/a-successful-git-branching-model/)

![model](https://i.imgur.com/4O04y4k.png)

<img alt="pic" src="https://i.imgur.com/Eq8uSel.png" width="500">

---

### The main branches 主要分支

该模型定义了两条长期存在的核心分支，贯穿项目整个生命周期。
The model defines two long-lived core branches that persist throughout the entire project lifecycle.

<img alt="pic" src="https://i.imgur.com/zSM149w.png" width="300">

- master
  - 视 origin/master 为主干分支 / consider origin/master to be the main branch
  - HEAD 的源码始终处于 <font color=red>生产就绪状态</font> / the source code of HEAD always reflects a <font color=red>production-ready state</font>
- develop
  - 视 origin/develop 为主干分支 / consider origin/develop to be the main branch
  - HEAD 的源码始终反映 <font color=red>下一个版本最新的开发变更</font> / the source code of HEAD always reflects the <font color=red>latest delivered development changes for the next release</font>
    - 有时也称为"集成分支" / Some would call this the "integration branch".
    - 所有自动夜间构建均从此分支构建 / This is where any automatic nightly builds are built from.
  - 当 develop 分支的代码达到稳定状态并准备发布时 / When the source code in the develop branch reaches a stable point and is ready to be released
    - 所有变更都应以某种方式合并回 master / all of the changes should be merged back into master somehow
    - 并打上发布版本号的 tag / and then tagged with a release number.

---

### Supporting branches 辅助分支

辅助分支用于支持团队成员之间的并行开发，实现功能追踪、生产发布准备，以及快速修复线上问题。与主要分支不同，辅助分支的生命周期有限，最终会被删除。

Supporting branches enable parallel development between team members, feature tracking, production release preparation, and quick production fixes. Unlike the main branches, these branches have a limited lifespan and are removed when their purpose is fulfilled.

辅助分支分为以下三种 / The different types of branches:

- Feature branches 功能分支
- Release branches 发布分支
- Hotfix branches 热修复分支

每种分支都有其特定用途，并受到严格规则约束——规定了它们可以从哪个分支分出，以及必须合并回哪个分支。
Each type has a specific purpose and is bound to strict rules about which branches it may originate from and which branches it must merge back into.

---

#### Feature branches 功能分支

<img alt="pic" src="https://i.imgur.com/rZF6qli.png" width="100">

- 可以从以下分支分出 / May branch off from:
  - develop
- 必须合并回以下分支 / Must merge back into:
  - develop
- 分支命名规范 / Branch naming convention:
  - master、develop、release-*、hotfix-* 以外的任意名称 / anything except master, develop, release-*, or hotfix-*

功能分支（也称主题分支）用于为即将发布或未来某个版本开发新功能。开始开发某个功能时，目标发布版本往往尚未确定。功能分支的核心特性是：<font color=LightSlateBlue>它的存在时间与功能的开发时间一样长</font>，最终将被合并回 develop（将新功能加入下一个版本）或被丢弃（实验性功能失败时）。功能分支通常只存在于开发者的本地仓库，不推送到 origin。

Feature / topic branches are used to develop new features for an upcoming or future release. When starting development, the target release may be unknown. The essence of a feature branch is that <font color=LightSlateBlue>it exists as long as the feature is in development</font> — it will eventually be merged into develop (to add the feature to the upcoming release) or discarded (in case of a disappointing experiment). Feature branches typically exist in developer repos only, not in origin.

```bash
# -------------- 创建功能分支 Creating a feature branch
# 从 develop 分支拉出新分支 / branch off from the develop branch.
# Switched to a new branch "myfeature"
$ git checkout -b myfeature develop


# -------------- 将完成的功能合并到 develop Incorporating a finished feature on develop
# 已完成的功能可合并到 develop，确保加入下一个发布版本
# Finished features may be merged into the develop branch to definitely add them to the upcoming release:

# Switched to branch 'develop'
$ git checkout develop

$ git merge --no-ff myfeature
# Updating ea1b82a..05e9557
# (Summary of changes)

# Deleted branch myfeature (was 05e9557).
$ git branch -d myfeature

$ git push origin develop
```

`--no-ff` 标志的作用 / The --no-ff flag:

- 强制创建一个新的合并提交，即使可以快进合并 / causes the merge to always create a new commit object, even if the merge could be performed with a fast-forward.
- 避免丢失功能分支历史存在的信息，并将所有添加该功能的提交归组在一起 / avoids losing information about the historical existence of a feature branch and groups together all commits that together added the feature.
- 效果对比如下 / Compare:

<img alt="pic" src="https://i.imgur.com/XhtCU90.png" width="400">

---

#### Release branches 发布分支

<img alt="pic" src="https://i.imgur.com/GnPThYo.png" width="400">

- 可以从以下分支分出 / May branch off from:
  - develop
- 必须合并回以下分支 / Must merge back into:
  - develop and master
- 分支命名规范 / Branch naming convention:
  - release-*

发布分支支持新生产版本的准备工作，允许进行最后的细节修正、小 Bug 修复，以及为发布准备元数据（版本号、构建日期等）。在此期间，develop 分支可以继续接收下一个大版本的功能。

Release branches support preparation of a new production release. They allow for last-minute dotting of i's and crossing t's, minor bug fixes, and preparing meta-data for a release (version number, build dates, etc.). By doing all of this work on a release branch, the develop branch is cleared to receive features for the next big release.

从 develop 拉出发布分支的时机：develop 已反映了新版本的期望状态，且所有目标功能均已合并进来。正是在发布分支开始时，即将发布的版本才会被分配版本号——在此之前，develop 分支反映的只是"下一个版本"的变更，具体是 0.3 还是 1.0 尚不确定。

The key moment to branch off a new release branch from develop is when develop reflects the desired state of the new release. It is exactly at the start of a release branch that the upcoming release gets assigned a version number — not any earlier. Up until that moment, develop reflected changes for the "next release" but it is unclear whether that will become 0.3 or 1.0.

发布分支可能存在一段时间，在此期间可对其应用 Bug 修复（而非在 develop 上）。严禁在此阶段加入大型新功能——新功能必须合并进 develop，等待下一个大版本。

This new branch may exist for a while until the release is rolled out. During that time, bug fixes may be applied in this branch (rather than on the develop branch). Adding large new features here is strictly prohibited — they must merge into develop and wait for the next big release.

```bash
# -------------- 创建发布分支 Creating a release branch
# 当前生产版本是 1.1.5，下一个目标版本是 1.2
# version 1.1.5 is the current production release and we have a big release coming up.
# The state of develop is ready for the "next release" version 1.2 (rather than 1.1.6 or 2.0).

# Switched to a new branch "release-1.2"
$ git checkout -b release-1.2 develop

# 自动修改文件以反映新版本号 / Files modified successfully, version number bumped to 1.2.
# bump-version.sh: a fictional shell script that bumps the version number and commits it.
$ ./bump-version.sh 1.2

$ git commit -a -m "Bumped version number to 1.2"
# [release-1.2 74d9424] Bumped version number to 1.2
# 1 files changed, 1 insertions(+), 1 deletions(-)




# -------------- 完成发布分支 Finishing a release branch
# 发布分支就绪后需执行以下步骤：
# When the state of the release branch is ready to become a real release:
# 1. 合并到 master / the release branch is merged into master
# 2. 在 master 上打 tag / commit on master must be tagged for easy future reference
# 3. 合并回 develop，保留修复内容 / the changes need to be merged back into develop

# -------------- 合并到 master / Merge into master
# Switched to branch 'master'
$ git checkout master

$ git merge --no-ff release-1.2
# Merge made by recursive.
# (Summary of changes)

# 发布完成，打 tag 便于以后参考 / The release is now done, tagged for future reference.
$ git tag -a 1.2

# 可使用 -s 或 -u <key> 对 tag 进行密码学签名
# might as well want to use the -s or -u <key> flags to sign your tag cryptographically.


# -------------- 合并回 develop，保留发布分支上的修复内容
# -------------- Keep the changes made in the release branch, merge back into develop
# Switched to branch 'develop'
$ git checkout develop

$ git merge --no-ff release-1.2
# Merge made by recursive.
# (Summary of changes)



# -------------- 删除发布分支，不再需要 / Remove the release branch, no longer needed
# Deleted branch release-1.2 (was ff452fe).
$ git branch -d release-1.2
```

---

#### Hotfix branches 热修复分支

<img alt="pic" src="https://i.imgur.com/2OvkJZO.png" width="400">

- 可以从以下分支分出 / May branch off from:
  - master
- 必须合并回以下分支 / Must merge back into:
  - develop and master
- 分支命名规范 / Branch naming convention:
  - hotfix-*

热修复分支类似于发布分支，同样是为生产发布做准备，但属于计划外的紧急响应。当生产环境出现必须立即修复的严重 Bug 时，从对应生产版本 tag 处拉出热修复分支。<font color=OrangeRed>核心价值</font>在于：团队成员可以继续在 develop 分支上开发，同时另一个人专注于修复生产问题。

Hotfix branches are very much like release branches in that they are also meant to prepare for a new production release, albeit unplanned. They arise from the necessity to act immediately upon an undesired state of a live production version. <font color=OrangeRed>The essence</font> is that work of team members (on the develop branch) can continue while another person is preparing a quick production fix.

```bash
# -------------- 创建热修复分支 Creating the hotfix branch
# 当前生产版本 1.2 存在严重 Bug，但 develop 上的更改尚不稳定
# version 1.2 is the current production release running live, causing troubles due to a severe bug.
# But changes on develop are yet unstable.

# Switched to a new branch "hotfix-1.2.1"
$ git checkout -b hotfix-1.2.1 master

# 分支拉出后立即更新版本号 / Files modified successfully, version bumped to 1.2.1.
# Don't forget to bump the version number after branching off!
$ ./bump-version.sh 1.2.1

$ git commit -a -m "Bumped version number to 1.2.1"
# [hotfix-1.2.1 41e61bb] Bumped version number to 1.2.1
# 1 files changed, 1 insertions(+), 1 deletions(-)


# -------------- 修复 Bug 并提交 Fix the bug and commit the fix in one or more separate commits.
$ git commit -m "Fixed severe production problem"
# [hotfix-1.2.1 abbe5d6] Fixed severe production problem
# 5 files changed, 32 insertions(+), 17 deletions(-)


# -------------- 完成并合并热修复分支 Finishing and merging a hotfix branch
# Bug 修复需同时合并回 master 和 develop，确保修复也包含在下一个版本中
# the bugfix needs to be merged back into master and develop
# to safeguard that the bugfix is included in the next release as well.

# Switched to branch 'master'
$ git checkout master
$ git merge --no-ff hotfix-1.2.1
$ git tag -a 1.2.1

# Switched to branch 'develop'
$ git checkout develop
$ git merge --no-ff hotfix-1.2.1

# 例外情况：若当前存在发布分支，则将热修复合并到发布分支而非 develop
# Exception: when a release branch currently exists, the hotfix changes need to be merged into
# that release branch instead of develop. Back-merging into the release branch will eventually
# result in the bugfix being merged into develop too, when the release branch is finished.



# -------------- 删除临时分支 Remove the temporary branch
# Deleted branch hotfix-1.2.1 (was abbe5d6).
$ git branch -d hotfix-1.2.1
```

---

### Cherry-Pick: Surgical Back-Porting 精准回移

#### 何时使用 `cherry-pick` 对比 `merge --no-ff`

经典 Git Flow 热修复工作流通过 `--no-ff` 将整个热修复分支合并回 develop。当 develop 干净时此方法有效，但以下情况会产生问题：

The classic Git Flow hotfix workflow merges the entire hotfix branch back into develop using `--no-ff`. This works well when develop is clean, but creates problems when:

- develop 已有不稳定的功能提交与热修复冲突 / develop already has unstable feature commits that conflict with the hotfix
- 热修复分支包含不应出现在 develop 上的版本号变更提交 / the hotfix branch contains version-bump commits that do not belong on develop
- 目标是只应用特定的修复提交，而不拉入周围的分支历史 / the goal is to apply only specific fix commits without pulling in surrounding branch history

<font color=OrangeRed>Cherry-pick</font> 允许通过 SHA 将单个提交复制到任意目标分支——精准操作，不合并任何其他内容。
<font color=OrangeRed>Cherry-pick</font> lets you copy individual commits by SHA onto any target branch — surgically, without merging anything else.

---

#### Scenario: release branch is live, main has new features in flight 场景：发布分支已上线

```
main (active features)        release/v1.2 (deployed to prod)
  |                                  |
  o feat: add dashboard              o fix: patch null pointer  <-- need this on main
  |                                  |
  o feat: refactor auth              o v1.2.1 tag
  |
  o ... (future work continues)
```

目标：将 `release/v1.2` 上的修复移植到 `main`，不阻断正在进行的功能开发。
The goal: get the fix from `release/v1.2` onto `main` without blocking the features in flight.

---

#### Step-by-step cherry-pick workflow 分步操作流程

```bash
# 1. 在发布分支上找到修复提交的 SHA / Find the commit SHA of the fix on the release branch
$ git log release/v1.2 --oneline
# abbe5d6 fix: patch null pointer in auth handler
# 41e61bb chore: bump version to v1.2.1
# ff452fe feat: release prep for v1.2

# 只 pick 实际的修复提交，不 pick 版本号变更提交
# Only pick the actual fix commit — not the version bump.
# The version bump does not belong on main.


# 2. 切换到 main / Switch to main
$ git checkout main


# 3. 通过 SHA cherry-pick 修复提交 / Cherry-pick the fix commit by SHA
$ git cherry-pick abbe5d6
# [main 7c3f1a2] fix: patch null pointer in auth handler
# 1 file changed, 3 insertions(+), 1 deletion(-)

# Git 在 main 上创建一个新提交，包含相同的变更但 SHA 不同
# Git creates a NEW commit on main with the same change but a different SHA.
# The original commit on release/v1.2 is untouched.


# 4. 验证修复已正确落地 / Verify the fix landed correctly
$ git log --oneline -5
# 7c3f1a2 fix: patch null pointer in auth handler   <-- cherry-picked
# 9b4da11 feat: add dashboard
# e3a12c0 feat: refactor auth
# ...

# main 上已有的功能不受影响 / Features already on main are unaffected.
# 新功能的部署可以继续 / Deployment of new features can continue.
```

---

#### Cherry-picking a range of commits 区间 cherry-pick

当修复跨越多个连续提交时 / When a fix spans multiple sequential commits:

```bash
# 从 abbe5d6 到 c1f2e3d 的所有提交（不含起点，含终点）
# Cherry-pick commits from abbe5d6 up to and including c1f2e3d (exclusive start, inclusive end)
$ git cherry-pick abbe5d6^..c1f2e3d

# 非连续提交时，显式列出 SHA / Or list individual SHAs explicitly when commits are non-contiguous
$ git cherry-pick abbe5d6 c1f2e3d
```

---

#### Handling conflicts during cherry-pick 处理冲突

```bash
# 若发生冲突，git 会暂停 cherry-pick / If a conflict occurs, git pauses the cherry-pick
$ git cherry-pick abbe5d6
# CONFLICT (content): Merge conflict in src/auth.py
# error: could not apply abbe5d6... fix: patch null pointer

# 解决冲突后暂存文件 / Resolve the conflict in the file, then stage it
$ git add src/auth.py

# 继续 cherry-pick（不要运行 git commit）/ Continue the cherry-pick (do not run git commit)
$ git cherry-pick --continue

# 或完全中止并恢复到 cherry-pick 前的状态 / Or abort entirely and return to the pre-cherry-pick state
$ git cherry-pick --abort
```

---

#### `merge --no-ff` vs `cherry-pick`: tradeoffs 权衡对比

| | `merge --no-ff` | `cherry-pick` |
|---|---|---|
| 应用范围 What gets applied | 整个分支历史 entire branch history | 指定提交 specific commit(s) only |
| 提交身份 Commit identity | 原始 SHA 保留在历史中 original SHAs preserved | 目标分支上生成新 SHA new SHA created on target branch |
| 冲突面 Conflict surface | 完整分支 diff / full branch diff | 仅 pick 提交的 diff / only the picked commit's diff |
| 适用场景 Good when | 分支干净且同步 branches are clean and in sync | 修复夹在不需要的提交中 fix sits alongside unwanted commits |
| 可追溯性 Traceability | 合并提交显示完整来源 merge commit shows full provenance | cherry-pick 丢失"来自发布分支"的上下文 loses "came from release branch" context |
| 使用场景 Use case | 标准 Git Flow 收尾 standard Git Flow finish | 功能分支超前时的热修复回移 hotfix back-port when feature branch is ahead |

为保留可追溯性，cherry-pick 时在提交信息中添加来源说明 / When using cherry-pick, add a reference in the commit message to preserve traceability:

```bash
$ git cherry-pick abbe5d6 -e
# 在编辑器中追加说明 / Opens editor — append a note to the commit message:
# fix: patch null pointer in auth handler
#
# Cherry-picked from release/v1.2 (abbe5d6)
```

---

#### Key rules 关键规则

- 只 cherry-pick 修复提交，不 pick 版本号变更或发布准备提交 / Cherry-pick only the fix commit, not version-bump or release-prep commits.
- cherry-pick 后在目标分支上运行测试——相同的变更在不同代码上下文中可能产生不同副作用 / Run tests on the target branch after cherry-pick — the same change can have different side effects in a different code context.
- 修复确认后为发布分支打 tag；若 main 有独立的发布节奏，也在 main 上独立打 tag / Tag the release branch after the fix is confirmed; tag independently on main if main has its own release cadence.
- 若同一修复需要应用到多个发布分支（v1.1、v1.2），对每个分支分别 cherry-pick 同一 SHA / If the same fix is needed across multiple release branches (v1.1, v1.2), cherry-pick the same SHA onto each.
