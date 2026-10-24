# MyRules

自用的 Clash 规则。mihomo 规则集，适用于 FlClash、Clash Verge Rev、Stash 等客户端。

## 规则文件

| 文件 | 内容 | 条数 | 来源 |
|---|---|---|---|
| muse.yaml | Muse（Meta AI，含 Facebook / Instagram 登录） | 29 | VPSDance/ai-proxy-rules、juner922/muse-loon-rules、v2fly |
| wise.yaml | Wise 国际汇款（原 TransferWise） | 2 | v2fly/domain-list-community |
| paypal.yaml | PayPal（含 Braintree、Venmo 等） | 247 | blackmatrix7/ios_rule_script |
| blued.yaml | Blued | 33 | blackmatrix7/ios_rule_script |
| lgbt.yaml | Grindr、Hornet、Jack'd、Scruff、Romeo、Taimi、HER | 12 | 自行整理 |
| streaming.yaml | Netflix、Disney+、HBO、Prime Video、Spotify | 1424 | blackmatrix7/ios_rule_script |
| douyin.yaml | 抖音（含火山版、汽水音乐、西瓜视频、今日头条） | 78 | blackmatrix7/ios_rule_script、v2fly |
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

## 建议的规则顺序

muse → paypal → wise → blued → lgbt → wechat → xiaohongshu → douyin → line → tiktok → streaming → google → apple

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

lgbt.txt 没有上游，完全靠手动维护。如果某个 App 连不上，在客户端的「连接」页面看它访问了哪些域名，补进 lgbt.txt 就行。

## 来源与许可

- blackmatrix7/ios_rule_script：GPL-2.0，来自它的文件保留了来源说明
- v2fly/domain-list-community：MIT
- VPSDance/ai-proxy-rules：MIT
- juner922/muse-loon-rules
- Grindr 域名参考：RobbieTechie/Grindr-API 文档
