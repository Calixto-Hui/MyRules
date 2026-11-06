# MyRules

自用的 Clash 规则。mihomo 规则集，适用于 FlClash、Clash Verge Rev、Stash 等客户端。

## 规则文件

| 文件 | 内容 | 条数 | 来源 |
|---|---|---|---|
| muse.yaml | Muse（Meta AI，含 Facebook / Instagram 登录） | 29 | VPSDance/ai-proxy-rules、juner922/muse-loon-rules、v2fly |
| manus.yaml | Manus AI 智能体（含 manus.space 部署站点、安卓 App 进程） | 6 | VPSDance/ai-proxy-rules、v2fly、自行补充 |
| ai.yaml | AI 工具：ChatGPT、Claude、Gemini、Grok、Perplexity、Copilot、Cursor、Midjourney 等 100 多个（不含 Muse、Manus） | 296 | VPSDance/ai-proxy-rules |
| wise.yaml | Wise 国际汇款（原 TransferWise） | 2 | v2fly/domain-list-community |
| finance.yaml | 美国支付与银行：PayPal（含 Venmo、Braintree）、Stripe、Cash App、Zelle、Plaid、Affirm、Kikoff、大通/美银/富国/花旗/运通等银行、Nubank US（Nu）、三大征信机构（Experian / Equifax / TransUnion）、myFICO、Credit Karma | 324 | blackmatrix7、v2fly、自行整理 |
| blued.yaml | Blued | 33 | blackmatrix7/ios_rule_script |
| lgbt.yaml | Grindr、Hornet、Jack'd、Scruff、Romeo、Taimi、HER | 12 | 自行整理 |
| streaming.yaml | Netflix、Disney+、HBO、Prime Video、Spotify | 1424 | blackmatrix7/ios_rule_script |
| douyin.yaml | 抖音（含火山版、汽水音乐、西瓜视频、今日头条） | 78 | blackmatrix7/ios_rule_script、v2fly |
| chinamedia.yaml | 国内流媒体：爱奇艺、优酷、腾讯视频、芒果TV、B站、央视、QQ音乐、网易云音乐等 | 412 | blackmatrix7/ios_rule_script |
| cscec.yaml | 中建集团（cscec.com、chinaconstruction.com） | 2 | 自行整理 |
| ukwifi.yaml | 英国运营商 Wi-Fi 通话（ePDG + Vodafone 授权服务器） | 3 | 自行整理 |
| xiaohongshu.yaml | 小红书（含 RedNote） | 11 | blackmatrix7/ios_rule_script、v2fly |
| wechat.yaml | 微信 | 31 | blackmatrix7/ios_rule_script |
| line.yaml | LINE | 37 | blackmatrix7/ios_rule_script、v2fly |
| tiktok.yaml | TikTok | 35 | blackmatrix7/ios_rule_script |
| apple.yaml | Apple | 1593 | blackmatrix7/ios_rule_script |
| google.yaml | Google（含 YouTube） | 881 | blackmatrix7/ios_rule_script |

所有文件都是 classical 格式（`behavior: classical`、`format: yaml`）。

## 使用方法

```yaml
rule-providers:
  muse:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/Calixto-Hui/MyRules/main/muse.yaml
    path: ./ruleset/muse.yaml
    interval: 86400

rules:
  - RULE-SET,muse,Muse
```

完整示例见 flclash-config.yaml。

## FlClash 设置（只做一次，以后不用再手动导入）

1. **用 URL 导入配置**：FlClash →「配置」→ 添加 →「URL」，填
   `https://raw.githubusercontent.com/Calixto-Hui/MyRules/main/flclash-config.yaml`，
   自动更新间隔设成 1 天（或更短）。以后仓库里的配置一改，FlClash 自动同步。
2. **新建覆写脚本**：「配置」右上角「脚本」→ 新建，把 flclash-script.js 的内容粘贴进去，
   在里面填上两个机场（TAG-GLOBAL、EdNovas）的订阅链接，保存。
3. **绑定脚本**：在第 1 步导入的配置上，打开「覆写」，选脚本模式，选中第 2 步的脚本。

订阅链接只保存在 FlClash 本地，不会出现在 GitHub 上。需要 FlClash 0.8.85 或更新版本。

## 建议的规则顺序

muse → manus → finance → ai → wise → blued → lgbt → wechat → xiaohongshu → douyin → chinamedia → cscec → line → tiktok → streaming → google → apple

YouTube 已经并入 google.yaml，跟谷歌服务走同一个节点。

## 自动更新

仓库里有一个 GitHub Actions 定时任务（.github/workflows/update.yml），每天沙特时间凌晨 1:17 自动运行：

1. 从上游（blackmatrix7、v2fly、VPSDance）拉取最新规则
2. 合并 custom/ 文件夹里你自己加的域名
3. 有变化就自动提交，没变化就什么都不做

某个上游拉取失败时，对应文件保留旧版本，不会被清空。

想立刻更新：打开仓库的 Actions 页面，选「每日更新规则」，点「Run workflow」。

## 怎么加自己的域名

⚠️ 不要直接改根目录下的 .yaml 文件，第二天会被自动更新覆盖。

要改 custom/ 文件夹里同名的 .txt 文件，每行一条，例如：

```
DOMAIN-SUFFIX,example.com
```

保存提交后，定时任务会立刻重新生成对应的 .yaml。

想从上游规则里剔除某些条目，写到 custom/同名.exclude.txt（例如 custom/ai.exclude.txt）。

lgbt.txt 没有上游，完全靠手动维护。如果某个 App 连不上，在客户端的「连接」页面看它访问了哪些域名，补进 lgbt.txt 就行。

## 来源与许可

- blackmatrix7/ios_rule_script：GPL-2.0，来自它的文件保留了来源说明
- v2fly/domain-list-community：MIT
- VPSDance/ai-proxy-rules：MIT
- juner922/muse-loon-rules
- Grindr 域名参考：RobbieTechie/Grindr-API 文档

## Wi-Fi 通话（安卓，需要在 FlClash 里手动设置一次）

- **英国 eSIM（VOXI / Vodafone 等）**：走「英国WiFi通话」分组，经英国节点出去。「英国节点」里固定选一个节点，不要换。
- **美国卡（Tello / T-Mobile 等）**：经过 FlClash 转发会报 ER081，必须绕开 VPN。
  FlClash →「工具」→「进阶配置」→「网络」→「排除路由地址」添加 `208.54.0.0/16`（T-Mobile 的 IP 段），
  配合配置里的 fake-ip-filter（美国国家码 310-316 拿真实 IP）生效。
- 不要在「访问控制」里把电话服务排除出 VPN，否则英国卡拿不到英国 IP。

