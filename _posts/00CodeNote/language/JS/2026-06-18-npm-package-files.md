---
title: "Meow's CodeNote - npm Package Files: package.json, package-lock.json and the Ecosystem / npm 包文件体系详解"
date: 2026-06-18 11:11:11 -0400
categories: [00CodeNote, JS]
tags: [npm, nodejs, package.json, package-lock, yarn, pnpm, dependencies, javascript]
math: false
toc: true
image:
---

# npm Package Files: package.json, package-lock.json and the Ecosystem

---

## Overview 概述

Node.js 项目的依赖管理由一组相互协作的文件共同完成。`package.json` 是项目的声明式清单，描述项目是什么、依赖什么；`package-lock.json` 是精确的依赖快照，保证所有人安装到完全相同的版本；`node_modules/` 是这些依赖的实际存储位置。理解这三者的职责边界，是管理任何 Node.js 项目的基础。

A Node.js project's dependency management is handled by a set of cooperating files. `package.json` is the declarative project manifest describing what the project is and what it depends on. `package-lock.json` is a precise dependency snapshot ensuring everyone installs exactly the same versions. `node_modules/` is where those dependencies are physically stored. Understanding the responsibility boundary of these three is the foundation of managing any Node.js project.

---

## Part 1: package.json — The Project Manifest 项目清单

`package.json` 是 Node.js 项目的核心配置文件，由开发者手动维护。它同时服务于两个角色：项目的描述卡片和 npm 的指令文件。

`package.json` is the core configuration file of a Node.js project, maintained manually by developers. It serves two roles simultaneously: a description card for the project and an instruction file for npm.

### 完整结构示例 Full Structure Example

```json
{
  "name": "my-app",
  "version": "1.2.3",
  "description": "A sample Node.js application",
  "main": "dist/index.js",
  "types": "dist/index.d.ts",
  "engines": {
    "node": ">=18.0.0",
    "npm": ">=9.0.0"
  },
  "scripts": {
    "start": "node dist/index.js",
    "dev": "ts-node src/index.ts",
    "build": "tsc",
    "test": "jest",
    "lint": "eslint src/",
    "pretest": "npm run build",
    "postbuild": "echo Build complete"
  },
  "dependencies": {
    "express": "^4.18.2",
    "axios": "~1.6.0"
  },
  "devDependencies": {
    "typescript": "^5.3.0",
    "jest": "^29.0.0",
    "@types/express": "^4.17.21"
  },
  "peerDependencies": {
    "react": ">=17.0.0"
  },
  "optionalDependencies": {
    "fsevents": "^2.3.3"
  },
  "private": true,
  "license": "MIT",
  "repository": {
    "type": "git",
    "url": "https://github.com/org/my-app.git"
  },
  "keywords": ["web", "api"],
  "author": "Grace Luo"
}
```

### 关键字段详解 Key Fields

#### `name` 和 `version`

`name` 和 `version` 共同构成包的唯一标识符。对于发布到 npm 的库，这两个字段是必填的。对于私有应用，建议加上 `"private": true` 防止意外发布。

`name` and `version` together form the unique identifier of the package. For libraries published to npm, both fields are required. For private applications, add `"private": true` to prevent accidental publishing.

```json
{
  "name": "@org/my-lib",
  "version": "2.0.0-beta.1",
  "private": true
}
```

#### `main`, `module`, `exports`

这三个字段控制 `require()` / `import` 时加载哪个入口文件：

These three fields control which entry file is loaded on `require()` / `import`:

| 字段 Field | 用途 Purpose |
|---|---|
| `main` | CommonJS 入口（`require()`）/ CommonJS entry |
| `module` | ES Module 入口（打包工具使用）/ ES module entry (used by bundlers) |
| `exports` | 现代精确导出映射，覆盖 `main` 和 `module` / Modern precise export map, overrides `main` and `module` |

```json
{
  "main": "dist/cjs/index.js",
  "module": "dist/esm/index.js",
  "exports": {
    ".": {
      "import": "./dist/esm/index.js",
      "require": "./dist/cjs/index.js"
    }
  }
}
```

#### `engines`

声明项目要求的 Node.js 和 npm 版本范围。这是一个声明，不强制执行（除非配置了 `engine-strict`），但工具和 CI 系统会读取它。

Declares the required Node.js and npm version ranges. This is advisory, not enforced (unless `engine-strict` is configured), but tooling and CI systems read it.

```json
{
  "engines": {
    "node": ">=18.0.0 <21.0.0"
  }
}
```

---

## Part 2: Dependency Types 依赖类型

### 四种依赖类型对比 Four Dependency Types

| 字段 Field | 安装时机 Installed When | 典型内容 Typical Contents |
|---|---|---|
| `dependencies` | 生产安装和开发安装 / Production + dev installs | 运行时框架、库 / Runtime frameworks, libraries |
| `devDependencies` | 仅开发安装 / Dev installs only (`npm install`) | 测试框架、构建工具、类型定义 / Test frameworks, build tools, type defs |
| `peerDependencies` | 不自动安装，由宿主项目提供 / Not auto-installed; provided by host project | 插件声明宿主库版本要求 / Plugin's required host lib version |
| `optionalDependencies` | 安装失败不阻断构建 / Install failure does not break the build | 平台特定的原生模块 / Platform-specific native modules |

### 选择哪个字段 Which Field to Use

```
这个包在应用运行时需要吗？
Is this package needed when the app runs?
        |
       是 Yes → dependencies
        |
       否 No
        |
        v
这个包是构建/测试/开发工具吗？
Is it a build/test/dev tool?
        |
       是 Yes → devDependencies
        |
       否 No
        |
        v
这个包是由使用方（宿主项目）提供的吗？
Is this package provided by the consumer (host project)?
        |
       是 Yes → peerDependencies
```

**实际例子 Practical Examples:**

```json
{
  "dependencies": {
    "express": "^4.18.2",
    "pg": "^8.11.0"
  },
  "devDependencies": {
    "jest": "^29.0.0",
    "eslint": "^8.0.0",
    "typescript": "^5.3.0",
    "@types/node": "^20.0.0"
  },
  "peerDependencies": {
    "react": ">=17.0.0"
  }
}
```

---

## Part 3: Version Ranges 版本范围语法

npm 使用 [SemVer](https://semver.org/)（语义化版本）规范：`MAJOR.MINOR.PATCH`

npm uses [SemVer](https://semver.org/) (semantic versioning): `MAJOR.MINOR.PATCH`

- **MAJOR** — 破坏性变更 / Breaking changes
- **MINOR** — 向后兼容的新功能 / Backwards-compatible new features
- **PATCH** — 向后兼容的 bug 修复 / Backwards-compatible bug fixes

### 版本符号速查 Version Specifier Cheatsheet

| 符号 Specifier | 含义 Meaning | 示例 Example | 允许范围 Allows |
|---|---|---|---|
| `^` | 锁定 MAJOR，允许 MINOR 和 PATCH 升级 / Lock MAJOR, allow MINOR+PATCH | `^4.1.0` | `>=4.1.0 <5.0.0` |
| `~` | 锁定 MAJOR.MINOR，仅允许 PATCH 升级 / Lock MAJOR.MINOR, allow PATCH only | `~4.1.0` | `>=4.1.0 <4.2.0` |
| `*` 或空白 | 任意版本（危险！）/ Any version (dangerous!) | `*` | any |
| 精确版本 Exact | 锁定到具体版本 / Pinned to exact version | `4.1.0` | `4.1.0` only |
| `>=` / `<` | 手动范围 / Manual range | `>=4.0.0 <5.0.0` | custom range |
| `latest` | npm registry 上的最新标签 / Latest tag on npm registry | `latest` | varies |

### `^` vs `~` 对比 Comparison

```
express: "^4.1.0"  →  4.1.0, 4.2.0, 4.99.0  ✓  |  5.0.0  ✗
express: "~4.1.0"  →  4.1.0, 4.1.5           ✓  |  4.2.0  ✗
express: "4.1.0"   →  4.1.0                  ✓  |  4.1.1  ✗
```

**推荐实践 Recommended Practice:**

- 应用项目（Application）：使用 `^` 保持安全补丁更新，`package-lock.json` 负责精确锁定
- 库项目（Library）：`peerDependencies` 用宽范围（`>=17`），`devDependencies` 用 `^`

- In application projects: use `^` to stay current with security patches; `package-lock.json` handles exact pinning
- In library projects: use wide ranges in `peerDependencies` (`>=17`), use `^` in `devDependencies`

---

## Part 4: scripts 字段 — npm 脚本系统

`scripts` 字段定义可通过 `npm run <name>` 执行的命令，是项目的统一任务入口。

The `scripts` field defines commands executable via `npm run <name>` and serves as the unified task entry point for the project.

### 生命周期钩子 Lifecycle Hooks

npm 在特定操作前后自动运行以 `pre` 和 `post` 为前缀的同名脚本：

npm automatically runs scripts prefixed with `pre` and `post` around specific operations:

```json
{
  "scripts": {
    "preinstall": "node check-node-version.js",
    "install": "node-gyp build",
    "postinstall": "patch-package",

    "prebuild": "rm -rf dist/",
    "build": "tsc",
    "postbuild": "cp -r public/ dist/public/",

    "pretest": "npm run lint",
    "test": "jest",
    "posttest": "npm run coverage"
  }
}
```

**执行顺序 Execution Order for `npm run build`:**

```
prebuild  →  build  →  postbuild
```

### 内置脚本名称 Built-in Script Names

某些脚本名称有特殊含义，可以不加 `run` 直接执行：

Certain script names have special meaning and can be run without the `run` keyword:

| 脚本 Script | 快捷命令 Shortcut | 触发时机 Trigger |
|---|---|---|
| `start` | `npm start` | 启动应用 / Start app |
| `test` | `npm test` | 运行测试 / Run tests |
| `stop` | `npm stop` | 停止应用 / Stop app |
| `restart` | `npm restart` | 重启（`stop` + `start`）|
| `install` / `postinstall` | 自动 / auto | `npm install` 完成后 / after install |

### 脚本中的环境变量 Environment Variables in Scripts

```json
{
  "scripts": {
    "start:prod": "NODE_ENV=production node dist/index.js",
    "start:dev": "NODE_ENV=development nodemon src/index.ts"
  }
}
```

npm 还自动将 `package.json` 的所有字段作为 `npm_package_*` 环境变量注入：

npm also automatically injects all `package.json` fields as `npm_package_*` env vars:

```bash
npm run build
# process.env.npm_package_name      → "my-app"
# process.env.npm_package_version   → "1.2.3"
```

---

## Part 5: package-lock.json — The Exact Snapshot 精确快照

`package-lock.json` 由 npm 自动生成和维护，**不应手动编辑**。它记录了安装时依赖树的精确版本，包括所有直接依赖和间接依赖（传递性依赖）。

`package-lock.json` is automatically generated and maintained by npm and should **never be edited manually**. It records the exact version of the dependency tree at install time, including all direct and transitive dependencies.

### 为什么需要 lockfile Why Lockfiles Exist

```
package.json 写了: "express": "^4.18.2"
package.json says: "express": "^4.18.2"

没有 lockfile 的情况 Without lockfile:
  开发者 A 安装时 → express@4.18.2  (express 当时最新)
  开发者 B 三个月后安装 → express@4.19.0  (新版本发布了)
  CI 服务器安装 → express@4.20.0  (又发布了新版本)
  → 三台机器运行不同版本！

有 lockfile 的情况 With lockfile:
  所有人都安装 → express@4.18.2  (lockfile 锁定了这个版本)
  → 每台机器运行完全相同的版本 ✓
```

### lockfile 的结构 Structure

```json
{
  "name": "my-app",
  "version": "1.2.3",
  "lockfileVersion": 3,
  "requires": true,
  "packages": {
    "": {
      "name": "my-app",
      "version": "1.2.3",
      "dependencies": {
        "express": "^4.18.2"
      }
    },
    "node_modules/express": {
      "version": "4.18.2",
      "resolved": "https://registry.npmjs.org/express/-/express-4.18.2.tgz",
      "integrity": "sha512-...",
      "dependencies": {
        "body-parser": "~1.20.1",
        "debug": "2.6.9"
      }
    },
    "node_modules/body-parser": {
      "version": "1.20.1",
      "resolved": "https://registry.npmjs.org/body-parser/-/body-parser-1.20.1.tgz",
      "integrity": "sha512-..."
    }
  }
}
```

关键字段 Key fields:
- `resolved` — 包的精确下载 URL / Exact download URL for the package
- `integrity` — SHA-512 哈希，用于验证下载内容未被篡改 / SHA-512 hash to verify the downloaded content is unmodified
- `lockfileVersion` — 格式版本：1=npm5, 2=npm7, 3=npm7+(v3) / Format version

### `npm install` vs `npm ci`

| 命令 Command | 行为 Behavior | 适用场景 Use Case |
|---|---|---|
| `npm install` | 读取 `package.json`，更新 `package-lock.json` | 开发时添加/更新依赖 / Dev: add or update deps |
| `npm ci` | 严格按 `package-lock.json` 安装，不修改任何文件，lockfile 不存在则报错 | CI/CD 和生产构建 / CI/CD and production builds |

```bash
# 开发环境 Development
npm install              # 安装所有依赖并更新 lockfile
npm install express      # 添加新依赖
npm install --save-dev jest  # 添加 devDependency

# CI / 生产环境 CI / Production
npm ci                   # 严格按 lockfile 安装，速度更快
```

### 应该提交 lockfile 吗？ Should lockfile Be Committed?

| 项目类型 Project Type | 是否提交 Commit? | 原因 Reason |
|---|---|---|
| 应用（App） | **是 Yes** | 保证团队、CI、生产环境版本一致 / Guarantees consistent versions across team, CI, prod |
| 库（Library） | **通常否 Usually No** | 库的使用方有自己的 lockfile，提交库的 lockfile 会造成冲突 / The consumer has its own lockfile; committing the lib's lockfile causes conflicts |

---

## Part 6: node_modules/ — The Install Directory 安装目录

`node_modules/` 是 npm 将所有依赖实际安装到的目录。它由 npm 完全管理，内容应始终可以通过 `npm install` 重新生成。

`node_modules/` is the directory where npm physically installs all dependencies. It is entirely managed by npm, and its contents should always be reproducible via `npm install`.

### 关键规则 Key Rules

- **始终加入 `.gitignore`** — `node_modules/` 体积巨大（数万文件），且可以从 lockfile 完全重建 / Always add to `.gitignore` — it is enormous (tens of thousands of files) and fully reproducible from the lockfile
- **不要手动修改其中的文件** — 重新运行 `npm install` 会覆盖任何手动修改 / Never manually modify files inside it — `npm install` will overwrite any manual changes
- **嵌套结构** — npm v3+ 使用扁平化安装策略，但某些版本冲突时仍会产生嵌套的 `node_modules/` / Nested structure — npm v3+ uses flat install strategy, but version conflicts can still produce nested `node_modules/`

```
node_modules/
├── express/          ← 直接依赖 direct dependency
│   ├── package.json
│   ├── index.js
│   └── lib/
├── body-parser/      ← express 的传递性依赖，被提升到顶层 / express's transitive dep, hoisted to top level
├── debug/
└── .package-lock.json  ← npm 内部使用的锁文件副本 / internal lockfile copy used by npm
```

---

## Part 7: Related Files 相关文件

### .npmrc — npm 配置文件

`.npmrc` 控制 npm 的行为，支持项目级（`<project>/.npmrc`）和用户级（`~/.npmrc`）两层配置。

`.npmrc` controls npm behavior, supporting both project-level (`<project>/.npmrc`) and user-level (`~/.npmrc`) configuration.

```ini
# .npmrc 示例 / .npmrc example

# 使用私有 registry / Use private registry
registry=https://registry.npmjs.org/
@myorg:registry=https://npm.pkg.github.com/

# 禁用 package-lock.json 生成（不推荐）/ Disable lockfile generation (not recommended)
package-lock=false

# 安装时保存确切版本 / Save exact versions on install
save-exact=true

# 设置 Node 版本引擎检查为严格模式 / Set engine check to strict
engine-strict=true

# CI 环境中禁用进度条 / Disable progress bar in CI
progress=false
```

### yarn.lock — Yarn 的 lockfile

Yarn（Classic v1 和 Berry v2+）使用 `yarn.lock` 替代 `package-lock.json`，格式不同但职责相同。

Yarn (Classic v1 and Berry v2+) uses `yarn.lock` instead of `package-lock.json`. Different format, same responsibility.

```yaml
# yarn.lock 片段 / yarn.lock excerpt
express@^4.18.2:
  version "4.18.2"
  resolved "https://registry.yarnpkg.com/express/-/express-4.18.2.tgz#..."
  integrity sha512-...
  dependencies:
    body-parser "~1.20.1"
    debug "2.6.9"
```

### pnpm-lock.yaml — pnpm 的 lockfile

pnpm 使用内容寻址存储和硬链接，其 lockfile 格式为 YAML。

pnpm uses content-addressable storage and hard links; its lockfile format is YAML.

```yaml
# pnpm-lock.yaml 片段 / pnpm-lock.yaml excerpt
lockfileVersion: '6.0'
dependencies:
  express:
    specifier: ^4.18.2
    version: 4.18.2
packages:
  /express@4.18.2:
    resolution:
      integrity: sha512-...
      tarball: https://registry.npmjs.org/express/-/express-4.18.2.tgz
```

### .nvmrc 和 .node-version — Node 版本声明

这两个文件声明项目所需的 Node.js 版本，供 nvm、fnm、volta 等版本管理工具自动切换版本使用。

These files declare the required Node.js version for the project, used by version managers like nvm, fnm, and volta to automatically switch versions.

```bash
# .nvmrc
18.19.0

# .node-version (same format, used by fnm and volta)
18.19.0
```

```bash
# 使用方式 / Usage
nvm use          # reads .nvmrc and switches to that Node version
fnm use          # reads .node-version or .nvmrc
```

### 文件职责一览 File Responsibility Summary

| 文件 File | 谁创建 Created By | 谁修改 Modified By | 提交到 Git? | 职责 Responsibility |
|---|---|---|---|---|
| `package.json` | 开发者 Developer | 开发者 Developer | **是 Yes** | 项目声明和依赖范围 / Project manifest and dep ranges |
| `package-lock.json` | npm 自动 npm auto | npm 自动 npm auto | **是 Yes**（应用）/ Yes (apps) | 依赖树精确快照 / Exact dependency snapshot |
| `node_modules/` | npm 自动 npm auto | npm 自动 npm auto | **否 No** | 依赖的实际代码 / Actual dependency code |
| `.npmrc` | 开发者 Developer | 开发者 Developer | **是 Yes** | npm 行为配置 / npm behavior config |
| `.nvmrc` | 开发者 Developer | 开发者 Developer | **是 Yes** | Node 版本声明 / Node version declaration |
| `yarn.lock` | yarn 自动 yarn auto | yarn 自动 yarn auto | **是 Yes**（应用）/ Yes (apps) | Yarn 的依赖快照 / Yarn dependency snapshot |
| `pnpm-lock.yaml` | pnpm 自动 pnpm auto | pnpm 自动 pnpm auto | **是 Yes**（应用）/ Yes (apps) | pnpm 的依赖快照 / pnpm dependency snapshot |

---

## Part 8: Common Workflows 常见操作

### 项目初始化 Project Initialization

```bash
# 交互式创建 package.json / Interactive create
npm init

# 使用默认值创建 / Create with defaults
npm init -y

# 安装所有依赖（按 package.json）/ Install all deps (per package.json)
npm install
```

### 添加和删除依赖 Adding and Removing Dependencies

```bash
# 添加运行时依赖 / Add runtime dependency
npm install express
npm install express@4.18.2        # 指定版本 / specific version

# 添加开发依赖 / Add dev dependency
npm install --save-dev jest
npm install -D typescript          # -D 是 --save-dev 的简写 / -D is shorthand

# 删除依赖 / Remove dependency
npm uninstall express

# 更新依赖到 package.json 允许的最新版本 / Update to latest allowed by package.json ranges
npm update

# 检查过期依赖 / Check outdated dependencies
npm outdated
```

### 检查依赖树 Inspecting the Dependency Tree

```bash
# 查看所有已安装包 / List all installed packages
npm list

# 只看直接依赖 / Direct dependencies only
npm list --depth=0

# 查看某个包被谁依赖 / Who depends on a specific package
npm why express

# 检查安全漏洞 / Check for security vulnerabilities
npm audit

# 自动修复低风险漏洞 / Auto-fix low-risk vulnerabilities
npm audit fix
```

### 清理重装 Clean Reinstall

```bash
# 删除 node_modules 并重新安装 / Delete node_modules and reinstall
rm -rf node_modules
npm ci                    # 严格按 lockfile / strictly per lockfile

# 或者使用工具 / or use a tool
npx rimraf node_modules && npm ci
```

---

## Key Takeaways 关键要点

- `package.json` 是开发者维护的声明式清单，定义依赖范围；`package-lock.json` 是 npm 自动生成的精确快照，不要手动编辑 / `package.json` is the developer-maintained manifest defining dep ranges; `package-lock.json` is npm's auto-generated exact snapshot — never edit manually
- `^` 锁定 MAJOR，允许 MINOR/PATCH 升级；`~` 锁定 MAJOR.MINOR，仅允许 PATCH 升级；精确版本无符号 / `^` locks MAJOR, allows MINOR/PATCH; `~` locks MAJOR.MINOR, allows PATCH only; no prefix means exact version
- `dependencies` 是运行时依赖；`devDependencies` 是工具链依赖；`peerDependencies` 是插件声明宿主要求 / `dependencies` are runtime; `devDependencies` are toolchain; `peerDependencies` declare host requirements for plugins
- 应用项目应提交 lockfile 到 Git；库项目通常不提交 / Applications should commit the lockfile to Git; libraries usually should not
- CI/CD 应使用 `npm ci` 而不是 `npm install`，前者更快且严格复现 lockfile / CI/CD should use `npm ci`, not `npm install` — faster and strictly reproduces the lockfile
- `node_modules/` 永远不要提交到 Git；始终加入 `.gitignore` / `node_modules/` should never be committed to Git; always add to `.gitignore`
- `scripts` 字段中 `pre<name>` 和 `post<name>` 钩子会在对应脚本前后自动运行 / `pre<name>` and `post<name>` hooks in `scripts` run automatically before and after the named script
- `.nvmrc` / `.node-version` 配合版本管理工具（nvm、fnm）确保团队使用一致的 Node 版本 / `.nvmrc` / `.node-version` with version managers (nvm, fnm) ensures consistent Node versions across the team

---

## References 参考资料

- [npm Docs: package.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-json)
- [npm Docs: package-lock.json](https://docs.npmjs.com/cli/v10/configuring-npm/package-lock-json)
- [npm Docs: npm ci](https://docs.npmjs.com/cli/v10/commands/npm-ci)
- [semver.org](https://semver.org/) — Semantic Versioning specification
- [Yarn docs: yarn.lock](https://yarnpkg.com/configuration/yarnrc)
- [pnpm docs: pnpm-lock.yaml](https://pnpm.io/lockfile/5.4)
