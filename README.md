# ClashRules

自用的 Clash 规则。mihomo 规则集，适用于 FlClash、Clash Verge Rev、Stash 等客户端。

## 规则文件

| 文件 | 内容 | 条数 | 来源 |
|---|---|---|---|
| muse.yaml | Muse（Meta AI，含 Facebook / Instagram 登录） | 29 | VPSDance/ai-proxy-rules、juner922/muse-loon-rules、v2fly |
| wise.yaml | Wise 国际汇款（原 TransferWise） | 2 | v2fly/domain-list-community |
| paypal.yaml | PayPal（含 Braintree、Venmo 等） | 247 | blackmatrix7/ios_rule_script |
| blued.yaml | Blued | 33 | blackmatrix7/ios_rule_script |
| lgbt.yaml | Grindr、Hornet、Jack'd、Scruff、Romeo、Taimi、HER | 12 | 自行整理 |
| streaming.yaml | Netflix、YouTube、Disney+、HBO、Prime Video、Spotify、TikTok | 1642 | blackmatrix7/ios_rule_script |
| apple.yaml | Apple | 1593 | blackmatrix7/ios_rule_script |
| google.yaml | Google | 701 | blackmatrix7/ios_rule_script |

所有文件都是 classical 格式（`behavior: classical`、`format: yaml`）。

## 其他文件（手动维护，不参与自动更新）

- ClashRules.ini：订阅转换（subconverter）用的配置，基于 ACL4SSR 修改
- PayPal.list、Emby.list：ClashRules.ini 引用的规则

## 使用方法

```yaml
rule-providers:
  muse:
    type: http
    behavior: classical
    format: yaml
    url: https://raw.githubusercontent.com/kekeke-wang/ClashRules/main/muse.yaml
    path: ./ruleset/muse.yaml
    interval: 86400

rules:
  - RULE-SET,muse,Muse
```

完整示例见 flclash-config.yaml。

## 建议的规则顺序

muse → paypal → wise → blued → lgbt → streaming → google → apple

streaming 要放在 google 前面，避免 YouTube 被谷歌规则先匹配。

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
