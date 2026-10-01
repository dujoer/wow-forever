# 工具与网站全景导航（Forever 专用）

> 整理时间：**2026-10-01**。离国服上线（11-05）约 5 周，工具生态正快速成型。
>
> **使用本页的三条硬原则**
> 1. **认准 Forever 分支（flavor）**：Forever 跑的是**现代 API（含 12.1.5 大部分 + Midnight 限制）**，Classic / Era 插件**不能直接加载**。下载前必须在项目页确认存在 **Forever** 或 **1.60.1** 字样的文件——CurseForge 的 "Flavors / Game Versions" 栏就是判断依据。
> 2. **内置件优先**：官方已内置**伤害统计**、**冷却管理器**（Beta 中按职业完善中），**挥砍计时器**也确认会来。先试内置的，缺什么再补插件。
> 3. **来源分级**：本页每条标注 **【官方】/【已确认】/【社区】/【商业站】/【待验证】**。**商业站点（代练/金币/礼包促销）的内容需交叉验证，且本库不推荐任何 RMT 行为**（见 `leveling-gold-route.md` 红线）。

---

## 一、官方与准官方（最高优先级）

| 名称 | 网址 | 用途 | 级别 |
|---|---|---|---|
| 国服官网（无限专区） | https://wow.blizzard.cn/ | 新闻、座谈会回顾、预约、规则集/传承系统说明、账号找回 | 【官方】 |
| 国服客户端下载页 | https://wow.blizzard.cn/download/ | 绿色客户端完整版下载（Beta 预下载入口） | 【官方】 |
| 国服商城（礼包对比） | https://shop.battlenet.com.cn/product/world-of-warcraft-forever | 三档礼包内容/价格、配置要求 | 【官方】 |
| 全球官网（中文） | https://worldofwarcraft.blizzard.com/zh-cn/ | 版本入口与说明 | 【官方】 |
| 暴雪新闻中心 | https://news.blizzard.com/ | 公告与媒体稿 | 【官方】 |
| 美服官方论坛 · Forever Beta 区 | https://us.forums.blizzard.com/ | **蓝贴一手来源**（如 10-01「Beta Update Maintenance」升 30 级公告） | 【官方】 |
| 暴雪支持 · 配置要求 | https://us.support.blizzard.com/en/help/article/386366 | 最低/推荐配置、macOS 支持 | 【官方】 |

---

## 二、数据库（查物品/任务/技能/副本）

| 名称 | 网址 | 用途与状态 | 级别 |
|---|---|---|---|
| **The WoW DB · Forever 专区** | https://thewowdb.com/wow-forever | 已上线的 Forever 数据库：种族、团本、天赋、官方日期清单。**离上线最近、结构最完整的英文库** | 【已确认】 |
| **Wowhead** | https://www.wowhead.com/ | 全球最大 WoW 数据库，已开 Forever 专区与**天赋计算器 / Legacy 计算器**；任务与物品库仍在填充 | 【已确认】 |
| **wowforeverguides.com** | https://wowforeverguides.com/addons | 少见的**逐条标注证据等级**（Confirmed / Planned / Reported / Unverified）的站；含插件、Beta 进度、副本指南 | 【社区】 |
| **wowforeverbuilds.com** | https://wowforeverbuilds.com/news | Beta 每日动态聚合（补丁、挖掘、实测），**是 9-30 数据挖掘的主要转述源** | 【社区】 |
| **Daybreak Forever**（数据挖掘） | 经 wowforeverbuilds.com 转述 | 客户端数据挖掘来源：副本具名、坐骑定价、洗点充能机制均出自此处 | 【社区】 |
| **wowforever.be** | https://wowforever.be/forever/ | 官方时间线整理（含 10-10 PAX Aus 日程），欧洲时区友好 | 【社区】 |
| **wowsrc.com/roadmap** | https://wowsrc.com/roadmap/ | 2026-2027 路线图可视化（Beta / 名称预留 / 上线 / 团本 / Hardcore / 2027 两次大更新） | 【社区】 |

> ⚠️ 重要提醒：**物品属性在掉落前完全隐藏**（官方已确认，见 `stats-and-gear.md`）。因此**任何站点的"Forever 满级 BIS 清单"在 12-09 团本解锁前都是猜测**，只能当思路参考。

---

## 三、天赋配点工具（51 点，10 级起）

| 名称 | 网址 | 特点 | 级别 |
|---|---|---|---|
| **WoW Forever Talents** | https://wowforevertalents.com/ | **数据直读客户端 1.60.1 Build 69977**（9-23 核对）；逐条标记"新 / 改写 / 与经典一致 / 未收录"；可开「Show original Classic」逐档对比；有社区投票配装榜 | 【已确认】 |
| **WoW Forever Talent** | https://wowforevertalent.org/ | 27 系全覆盖，**实时校验点数预算、行门槛与前置**；可存档/分享链接；带"来自 Reddit 讨论"的示例配装 | 【社区】 |
| **Wowhead 天赋计算器** | https://www.wowhead.com/ | 与 Wowhead 数据库打通，查完天赋可顺手查技能/物品 | 【已确认】 |
| **Icy Veins 计算器** | https://www.icy-veins.com/ | **金星标新天赋、蓝星标改动天赋**——最适合"我熟悉经典某系，想快速看改了什么" | 【已确认】 |
| **Kovarel 中文站** | https://kovarel.com/cn/wow-forever | **中文界面**：51 点天赋模拟器 + 种族特质 + 技能改动 + 传承规划器 + 地下城名册；含**双名制角色起名器** | 【社区】 |
| **一梦风神 · 无限天赋模拟器** | https://www.fengshen.cn/wuxian/ | **纯中文网页版**，手机电脑通用；左键加点/右键减点，自动生成分享码；按前置依赖排序 | 【社区】 |
| **Guild Manager（Forge）** | https://guildmanager.app/ | 天赋计算器 + **可把配装挂到公会的角色档案上**，便于公会统一规划（谁坦克/谁治疗）；另有社区配装目录 | 【社区】 |

> 规则回顾：**10 级第 1 点 → 60 级共 51 点**；**每系每 5 点解锁下一排**；**16 点 / 11 / 21 / 31 点为单点里程碑**；**双流派 40 级解锁**；洗点在主要城市职业训练师处（含 Legacy 天赋），洗点受"上限 10 充能、每小时回 1 次"的隐藏货币约束。

---

## 四、练级路线与导航插件

| 工具 | 状态（截至 10-01） | 说明 | 级别 |
|---|---|---|---|
| **RestedXP** | ✅ **已在更新 Forever 路线**（v4.11.9 起支持 #classic 路由、扩展天裔路线；v4.11.10 覆盖杜隆塔尔/莫高雷） | 免费插件 + 付费路线；是**目前唯一已实装 Forever 内容的付费练级导引** | 【已确认】 |
| **Zygor Guides** | ⏳ **计划随 11 月上线推出（Elite 订阅）**，Beta 期不出 | 另一大付费路线插件，与 RestedXP 对比选购 | 【社区】 |
| **Questie（Forever 版）** | ✅ **已有 Forever 文件**（v12.0.2+v1.0.4，9-28 更新） | 免费任务助手，CurseForge 的 Flavors 栏可见 Forever。**新任务覆盖仍不完整** | 【已确认】 |
| **Forever Quest Pins** | ✅ 可用（v0.1.28） | 轻量：只在地图上标**任务起点** | 【社区】 |
| **TomTom** | ✅ **已有 Forever 文件**（v4.3.10） | 坐标导航箭头——它**不会替你规划路线**，只负责"到已知点" | 【已确认】 |
| **Guidelime** | ⚠️ 初步 Forever 支持 | 免费导引框架 | 【待验证】 |
| **Leatrix Plus / Leatrix Maps** | ✅ 已有 Forever 构建（1.60.04-forever） | 垃圾出售、自动修理、地图增强等日常便利 | 【已确认】 |
| **EQ Objective Tracker** | ✅ v1.25.1 | 可移动、可整理的任务追踪面板 | 【社区】 |

---

## 五、插件生态、安装与已知坑

**安装路径（Beta）**：`World of Warcraft_classic_beta_\Interface\AddOns\`（正式上线后文件夹名可能变化，以战网所选客户端为准）。
**管理器**：CurseForge App、WowUp、Wago App（选 Forever 分支后再装）。

| 类别 | 项目 | 状态 |
|---|---|---|
| 经典界面还原 | **ClassicUI Forever**（justawower） | ✅ 已上架：狮鹫动作条、旧版单位框、圆形小地图、1.x 背包/拾取/商人/社交窗口，**模块化且接入 Edit Mode 而非替换 UI** |
| 任务/练级装备 | **GearQuest - Forever** | ✅ 社区版，练级期装备目标提示 |
| 首领报警 | **Deadly Boss Mods / BigWigs** | ⏳ **移植中**；能播报多少取决于首领暴露了什么（受"秘密值"约束） |
| PvP | **Spy (Forever)** | ✅ 已有移植 |
| 综合 UI | **EllesmereUI**、ForeverPlus、ForeverUI、RyoUI、Forever Threat、Gathering | ✅ 1.60.1 项目，成熟度参差 |
| 工具型 | **WoW Handbook**（9-29 上架 CurseForge） | ✅ 地下城任务/战利品、按等级法术、动作条升级、地图标记、自动售卖 |
| 伤害统计 | **官方内置** | ✅ 随游戏发布，Details / Recount 变为**可选而非必需** |
| 冷却管理 | **官方内置** | ⚠️ Beta 中"按职业有差异、进行中"；10-01 补丁后继续完善 |
| 挥砍计时器 | 官方内置 | ⏳ 官方称"可能即将推出"（对惩戒骑、增强萨这类靠平砍节奏的专精重要） |
| **WeakAuras** | ❌ **主项目截至 9-22 无 Forever flavor，作者已停止移植** | 只能跟踪**自身** buff/冷却/资源；读敌方施法条、战斗日志、他人状态来"推导该按什么"被限制 |

**两个已报告的 Beta 通用 bug（装插件必读）**
1. **SavedVariables 写入正常但重启后不加载** → 布局与键位会重置，**目前无解决方案**（9-21 玩家报告，尚未进官方 Known Issues）。
2. **发给小号的邮件收不到**（持续一周以上），社区怀疑与「名+姓」双字段解析有关 → **Beta 期别把关键材料寄给小号**。

> ⚠️ **国服治理红线**：国服运营团队已发布「付费插件及其违规商业化行为专项治理公告」，依据《用户界面插件开发政策》**打击违规插件与插件的付费商业化**。→ 只从正规渠道装免费插件，**不要买"付费插件/内部版"**。

---

## 六、经济与拍卖行

| 工具 | Forever 状态 | 说明 |
|---|---|---|
| **TradeSkillMaster (TSM)** | ❓ 截至 10-01 **未见 Forever 专属文件**（CurseForge Flavors 仅列 Retail / MoP Classic / Classic / TBC） | 最强经济插件，但需作者适配；上线后复查 |
| **Auctionator** | ❓ 同上待确认 | 轻量替代，适合"只是想快点挂材料" |
| **GatherMate2** | ❓ 待确认 | 采集节点记录——**无飞行**环境下绕路成本高，价值比正式服更大 |
| **官方内置拍卖行** | ✅ 可用 | 首发期物价混乱，先以内置为主 + 手工记账 |

> 经济红线（务必遵守）：**GDKP 金币拍团被禁**、**第三方购金永久封号**、**RMT 买家同罚**（9-29 蓝贴升级：可没收接收方金币并封号）。Beta 内 30 级赌斗赛事已出现小号递金被查的案例。

---

## 七、公会、组队与社区

| 名称 | 网址 | 用途 | 级别 |
|---|---|---|---|
| **Raidify** | https://www.raidify.app/wow-forever | **公会查找按规则集/地区/团队风格/开团夜晚筛选**；⚠️ 它把**规则集设为硬过滤**——因为不同规则集**根本无法组队**。含开团报名、Discord 机器人、人员分工；装甲库与 WCL 联动待官方支持 | 【社区】 |
| **Guild Manager** | https://guildmanager.app/ | 公会成员/角色档案 + 天赋配装挂载 + 活动与队伍工具 | 【社区】 |
| **WoW Forever NA（Discord）** | https://discord.com/servers/wow-forever-na-1528511731523915907 | 约 **9,445 成员**，含部落/联盟分区、公会目录、地下城与团本 LFG、招募频道 | 【社区】 |
| **NGA 玩家社区** | https://nga.cn/ | 国服最大 WoW 论坛：首发攻略、物价、插件兼容实测 | 【社区】 |
| **178 魔兽世界** | https://wow.178.com/ | 国服资讯 | 【社区】 |
| **Reddit r/classicwow** | https://www.reddit.com/r/classicwow/ | 国际讨论与玩法验证 | 【社区】 |
| **Warcraft Tavern** | https://warcrafttavern.com/ | Beta 新闻与蓝贴转述（首报升 30 级等） | 【社区】 |
| **wow4evernews** | https://wow4evernews.com/ | 插件/练级工具横向对比 | 【社区】 |
| **wowsod.pro** | https://wowsod.pro/ | 开发者问答逐条整理（插件/宏限制的一手转述） | 【社区】 |

> 视频渠道：官方 **YouTube / Twitch World of Warcraft 频道**（座谈会、10-10 PAX Aus 副本深挖）；国服侧 **B 站 / 抖音** 创作者会在 10 月下旬集中产出前瞻。

---

## 八、国服玩家专项清单

| 事项 | 说明 |
|---|---|
| 客户端 | 战网桌面应用（左上「偏好」→《魔兽世界》:无限 →「游戏版本与账号」→ 安装）或官网绿色客户端完整版，**推荐装 SSD** |
| 账号 | 提前确认/找回战网账号（官网有实名/账号两种找回方式） |
| 资格 | 基础游戏**含在月卡/游戏时间内**；**天裔种族**需礼包；**国服 Beta 需 ¥388 史诗礼包或官方活动资格** |
| 资讯节奏 | 上线前 2 周（10 月下旬）起重点盯 **官网公告 + NGA + Wowhead**，数据库与攻略会在那时快速成型 |
| 中文工具 | Kovarel（中文数据库 + 天赋模拟器 + 起名器）、一梦风神（中文天赋模拟器）——**中文界面优先选这两个** |

---

## 九、硬件与外设自检

- **GPU 硬门槛**：需支持 **RGBA16F UAV（compute shader）**；**AMD GCN1 / NVIDIA Maxwell / Intel Skylake 之前架构不支持**（GTX 760/770/780 等 Kepler 卡被排除）。
- **存储**：官方明确 **SSD 128GB 可用**，HDD 会明显影响体验。
- **手柄**：官方支持且在 9-25 补丁中扩展了职业飞出菜单与紧凑布局；但**键鼠仍是效率首选**（多按键滚轮鼠标被写入推荐配置）。
- **显卡驱动**：国服公告要求**先更新显卡驱动**再下载安装。

---

## 十、避坑清单（商业站点与安全）

1. **不要买金币 / 不要参加 GDKP**：封号与没收金币风险，且**买家同样受罚**。
2. **不要买"付费插件/内部版"**：国服正在专项治理插件违规商业化。
3. **不要依赖"一键输出宏"**：暴雪自 2006 年封死宏的变量/循环/分支；外部连点脚本、键鼠硬件宏、读屏读内存的智能宏 **= 违规会封号**。合法上限是"点一下 = 施放优先级最高的可用技能"（见 `macros-and-ui.md`）。
4. **别在 12-09 前重金制造**：新五人本掉落与物价未定型。
5. **别把 Beta 结论直接外推正式服**：9-25 的"1 银币洗点"、职业数值调整均为 **Beta 检查点**。
