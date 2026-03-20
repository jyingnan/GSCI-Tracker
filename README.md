# GSCI-Tracker — Global Severity-weighted Conflict Index

[![Data Update](https://img.shields.io/badge/data-weekly%20auto--update-brightgreen)](https://github.com/jyingnan/GSCI-Tracker/actions)
[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![GitHub Pages](https://img.shields.io/badge/dashboard-live-blue)](https://jyingnan.github.io/GSCI-Tracker/)

**[English](#english) | [中文](#chinese)**

---

<a name="english"></a>
## English

### Overview

**GSCI** (Global Severity-weighted Conflict Index) is a daily, event-based measure of global conflict intensity constructed from the [GDELT Project](https://www.gdeltproject.org/). It aggregates conflict-related events coded under the CAMEO taxonomy and weights them by Goldstein severity scores, providing a real-time, multilingual, and open-source complement to perception-based geopolitical risk indicators such as the GPR index of Caldara and Iacoviello (2022).

This repository provides:
- **`gsci_data.csv`** — the full daily GSCI series from March 2015 to present, including the raw `total_sources` denominator
- **`index.html`** — an interactive dashboard (live at [jyingnan.github.io/GSCI-Tracker](https://jyingnan.github.io/GSCI-Tracker/))
- **`events.json`** — annotated geopolitical event database for dashboard overlays
- **`update_gsci.py`** — automated weekly update script via BigQuery
- **`.github/workflows/update.yml`** — GitHub Actions workflow for scheduled updates

---

### Index Construction

GSCI is defined as:

$$GSCI_t = \frac{\sum_{i \in C_t} |G_i| \times S_{i,t}}{N_t}$$

| Symbol | Definition |
|--------|------------|
| $C_t$ | Set of conflict events with strictly negative Goldstein scores on day $t$ |
| $\|G_i\|$ | Absolute Goldstein severity weight of event $i$ (range: 0 to 10) |
| $S_{i,t}$ | Number of news sources reporting event $i$ on day $t$ |
| $N_t$ | Total number of news sources on day $t$ (`total_sources`) |

Source-share normalization by $N_t$ ensures cross-day comparability and controls for variation in total daily news volume. Only events with **strictly negative Goldstein scores** are included, covering CAMEO-coded conflict categories.

---

### Data Description

**File:** `gsci_data.csv`

| Column | Type | Description |
|--------|------|-------------|
| `date` | string (YYYY-MM-DD) | Calendar date |
| `total_sources` | integer | Total number of news sources on day $t$ — the GSCI denominator $N_t$ |
| `gsci` | float | Daily GSCI value (severity-weighted conflict intensity) |

- **Coverage:** March 1, 2015 – present
- **Frequency:** Daily
- **Update schedule:** Every Monday (automated via GitHub Actions + Google BigQuery)
- **Source:** GDELT v2 Event Stream

#### Data Quality — Source Count Variability

The `total_sources` column records the GSCI denominator $N_t$ and is included for transparency. Abnormally low values can distort the index, and users should be aware of the following known causes:

- **Holiday Effect** — global news production declines on public holidays, reducing GDELT ingestion volume.
- **GDELT Crawler Outages** — GDELT's infrastructure occasionally experiences 12–24 hour data gaps due to Google Cloud sync delays or external crawl rate-limit events.
- **Major News Crowding** — a dominant breaking story can compress coverage of other events, skewing source distribution.
- **Deduplication & Versioning Changes** — GDELT's internal deduplication logic or versioning updates can cause step-changes in reported source counts.

**Recommended practice:** Days where `total_sources < 10,000` should be interpreted with caution. The interactive dashboard flags these dates with amber highlights and a tooltip warning. For robust analysis, consider excluding such observations or applying a threshold appropriate to your use case.

---

### Live Dashboard

An interactive dashboard is available at:

🔗 **[https://jyingnan.github.io/GSCI-Tracker/](https://jyingnan.github.io/GSCI-Tracker/)**

Features:
- Time range selector (1Y / 3Y / 5Y / All)
- Toggle for geopolitical event annotations (Armed Conflict / Terrorism / Political Crisis / Domestic)
- Low-source highlight toggle — flags days with `total_sources < 10,000` in amber
- Hover tooltip showing GSCI value, sample mean, and raw source count (with warning if below threshold)
- 1-year peak stat (calculated over clean-data days only, excluding low-source observations)
- Light / dark theme
- Downloadable CSV

---

### Replication

To recompute GSCI from scratch using Google BigQuery:

**1. Install dependencies**
```bash
pip install pandas google-cloud-bigquery db-dtypes
```

**2. Set up GCP credentials**

Create a service account with BigQuery read access and export the key as an environment variable:
```bash
export GCP_SERVICE_ACCOUNT_KEY='<your_json_key>'
```

**3. Run the update script**
```bash
python update_gsci.py
```

The script queries the `gdelt-bq.gdeltv2.events` table, applies the GSCI formula, and overwrites `gsci_data.csv` with the full series including `total_sources`.

---

### Automated Updates

The repository uses GitHub Actions for weekly updates:

- **Trigger:** Every Monday at 00:00 UTC (or manual dispatch via `workflow_dispatch`)
- **Process:** Authenticates to GCP → queries BigQuery → overwrites `gsci_data.csv` → commits and pushes
- **Required secret:** Add `GCP_SERVICE_ACCOUNT_KEY` (full JSON) in your repository's **Settings → Secrets and variables → Actions**

---

### Relationship to GPR

GSCI is designed as an **event-based complement** to the Geopolitical Risk (GPR) index of Caldara and Iacoviello (2022), not a replacement. The two indices measure different dimensions:

| | GSCI | GPR |
|-|------|-----|
| **Basis** | Recorded conflict events (GDELT) | Editorial newspaper coverage |
| **Languages** | 100+ languages | English only (10 newspapers) |
| **Update frequency** | Weekly (near real-time) | Weekly |
| **Historical coverage** | 2015–present | 1900–present |
| **Nature** | Event severity | Perceived risk |

---

### Citation

If you use GSCI data in your research, please cite:

> [Author(s)]. "From Ten Newspapers to the World: An Event-Based Conflict Intensity Index." *Working Paper*, 2026. GitHub: [https://github.com/jyingnan/GSCI-Tracker](https://github.com/jyingnan/GSCI-Tracker)

The GSCI data series is also directly citable as a dataset:

> [Author(s)]. *Global Severity-weighted Conflict Index (GSCI)*. Daily data, March 2015–present. Available at: [https://github.com/jyingnan/GSCI-Tracker](https://github.com/jyingnan/GSCI-Tracker)

---

### References

- Caldara, D., Iacoviello, M. (2022). Measuring geopolitical risk. *American Economic Review*, 112(4), 1194–1225.
- GDELT Project: [https://www.gdeltproject.org/](https://www.gdeltproject.org/)

---

### License

This dataset and associated code are released under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/). You are free to use, share, and adapt the material for any purpose, including commercial use, provided appropriate credit is given.

The underlying GDELT data is made available by the GDELT Project under its own open access terms.

---

---

<a name="chinese"></a>
## 中文

### 概述

**GSCI**（全球冲突严重程度加权指数，Global Severity-weighted Conflict Index）是一个基于事件的每日全球冲突强度指标，数据来源于 [GDELT 项目](https://www.gdeltproject.org/)。该指数汇总了 CAMEO 编码框架下的冲突相关事件，并以 Goldstein 严重程度分数进行加权，为 Caldara 和 Iacoviello（2022）的 GPR 指数等基于文本感知的地缘政治风险指标提供实时、多语言、开源的事件侧补充。

本仓库提供：
- **`gsci_data.csv`** — 2015 年 3 月至今的完整每日 GSCI 时间序列，含原始分母 `total_sources`
- **`index.html`** — 交互式可视化面板（在线访问：[jyingnan.github.io/GSCI-Tracker](https://jyingnan.github.io/GSCI-Tracker/)）
- **`events.json`** — 用于面板标注的地缘政治重大事件数据库
- **`update_gsci.py`** — 通过 BigQuery 自动更新的脚本
- **`.github/workflows/update.yml`** — 定时更新的 GitHub Actions 工作流

---

### 指数构建

GSCI 的计算公式为：

$$GSCI_t = \frac{\sum_{i \in C_t} |G_i| \times S_{i,t}}{N_t}$$

| 符号 | 含义 |
|------|------|
| $C_t$ | 第 $t$ 日 Goldstein 分数严格为负的冲突事件集合 |
| $\|G_i\|$ | 事件 $i$ 的 Goldstein 严重程度绝对值（范围：0 至 10） |
| $S_{i,t}$ | 第 $t$ 日报道事件 $i$ 的新闻来源数量 |
| $N_t$ | 第 $t$ 日新闻来源总数（即 `total_sources`） |

以 $N_t$ 进行来源份额归一化，确保跨日可比性，并控制每日新闻总量的波动。指数仅纳入 **Goldstein 分数严格为负**的事件。

---

### 数据说明

**文件：** `gsci_data.csv`

| 字段 | 类型 | 说明 |
|------|------|------|
| `date` | 字符串（YYYY-MM-DD） | 日期 |
| `total_sources` | 整数 | 第 $t$ 日新闻来源总数，即 GSCI 分母 $N_t$ |
| `gsci` | 浮点数 | 当日 GSCI 值（严重程度加权冲突强度） |

- **覆盖时间：** 2015 年 3 月 1 日至今
- **频率：** 每日
- **更新周期：** 每周一自动更新（GitHub Actions + Google BigQuery）
- **数据来源：** GDELT v2 事件流

#### 数据质量 — 来源数量波动

`total_sources` 字段记录 GSCI 分母 $N_t$，随数据集一并公开以供用户核查。该值异常偏低时可能扭曲指数，已知原因包括：

- **假日效应（Holiday Effect）** — 公共假日期间全球新闻产量下降，GDELT 抓取量随之减少。
- **GDELT 爬虫断档** — GDELT 基础设施偶发 12–24 小时的数据缺口，通常与 Google Cloud 同步延迟或外部抓取频率限制有关。
- **重大事件新闻挤压** — 单一突发性重大事件可压缩其他新闻的报道量，导致来源分布偏斜。
- **去重与版本逻辑变更** — GDELT 内部去重逻辑或版本更新有时会造成报告来源数的阶跃变化。

**建议实践：** `total_sources < 10,000` 的日期应谨慎解读。交互式面板会以琥珀色色带标注此类日期，并在悬停提示中显示警告。进行严谨分析时，建议剔除此类观测值，或根据研究目的自行设定合适的阈值。

---

### 在线面板

交互式可视化面板：

🔗 **[https://jyingnan.github.io/GSCI-Tracker/](https://jyingnan.github.io/GSCI-Tracker/)**

主要功能：
- 时间区间选择（近 1 年 / 3 年 / 5 年 / 全部）
- 地缘政治事件标注开关（武装冲突 / 恐怖袭击 / 政治危机 / 国内冲突）
- 低来源标注开关 — 以琥珀色高亮 `total_sources < 10,000` 的日期
- 鼠标悬停提示，显示当日 GSCI 值、样本均值及原始来源数（低于阈值时附加警告）
- 近一年峰值统计（仅基于来源数正常的日期计算）
- 亮色 / 暗色主题切换
- CSV 数据下载

---

### 复现方法

如需从头通过 Google BigQuery 重新计算 GSCI：

**1. 安装依赖**
```bash
pip install pandas google-cloud-bigquery db-dtypes
```

**2. 配置 GCP 凭据**

创建具有 BigQuery 读取权限的服务账号，并将密钥导出为环境变量：
```bash
export GCP_SERVICE_ACCOUNT_KEY='<your_json_key>'
```

**3. 运行更新脚本**
```bash
python update_gsci.py
```

脚本将查询 `gdelt-bq.gdeltv2.events` 表，应用 GSCI 公式，并以完整序列（含 `total_sources`）覆盖写入 `gsci_data.csv`。

---

### 自动更新机制

本仓库通过 GitHub Actions 实现每周自动更新：

- **触发条件：** 每周一 UTC 00:00（或通过 `workflow_dispatch` 手动触发）
- **流程：** GCP 认证 → 查询 BigQuery → 覆盖写入 `gsci_data.csv` → 提交并推送
- **所需密钥：** 在仓库 **Settings → Secrets and variables → Actions** 中添加 `GCP_SERVICE_ACCOUNT_KEY`（完整 JSON 格式）

---

### 与 GPR 的关系

GSCI 被设计为 Caldara 和 Iacoviello（2022）GPR 指数的**事件侧补充**，而非替代。两者衡量不同维度：

| | GSCI | GPR |
|-|------|-----|
| **构建基础** | 实际冲突事件记录（GDELT） | 报纸编辑内容 |
| **语言覆盖** | 100+ 种语言 | 仅英语（10 家报纸） |
| **更新频率** | 每周（近实时） | 每周 |
| **历史覆盖** | 2015 年至今 | 1900 年至今 |
| **指标性质** | 事件严重程度 | 风险感知 |

---

### 引用格式

如在研究中使用 GSCI 数据，请引用：

> [作者]. "From Ten Newspapers to the World: An Event-Based Conflict Intensity Index." *Working Paper*, 2026. GitHub: [https://github.com/jyingnan/GSCI-Tracker](https://github.com/jyingnan/GSCI-Tracker)

如直接引用数据集：

> [作者]. *全球冲突严重程度加权指数（GSCI）*. 每日数据，2015 年 3 月至今. 获取地址：[https://github.com/jyingnan/GSCI-Tracker](https://github.com/jyingnan/GSCI-Tracker)

---

### 参考文献

- Caldara, D., Iacoviello, M. (2022). Measuring geopolitical risk. *American Economic Review*, 112(4), 1194–1225.
- GDELT 项目官网：[https://www.gdeltproject.org/](https://www.gdeltproject.org/)

---

### 许可协议

本数据集及相关代码采用 [知识共享署名 4.0 国际许可协议（CC BY 4.0）](https://creativecommons.org/licenses/by/4.0/deed.zh) 发布。您可以自由使用、共享和改编本材料（包括商业用途），但须注明原始出处。

底层 GDELT 数据由 GDELT 项目依其开放访问条款提供。
