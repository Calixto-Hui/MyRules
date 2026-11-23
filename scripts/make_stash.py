#!/usr/bin/env python3
"""由 flclash-config.yaml 自动生成 Stash 专用配置 stash-config.yaml。

以后只需要改 flclash-config.yaml，推送后 GitHub Actions 会自动重新生成 Stash 版。
转换内容：
  - 去掉 Stash 不支持的 mihomo 专属字段（listeners、geodata、指纹等）
  - 去掉只给 7891 专用端口用的 AdsPower 分组
  - proxy-providers 去掉 override / health-check（Stash 不支持），订阅链接用 stash-subs.stoverride 覆写填入
  - exclude-filter 改写成 Stash 能用的正则（负向前瞻）
  - GEOSITE,private / GEOIP,private 改成局域网 IP 段直连
  - 加上 Stash 特有的分组图标（icon）和懒测速（lazy）
"""
import os
import sys

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "flclash-config.yaml")
DST = os.path.join(ROOT, "stash-config.yaml")

# Stash 不认识或不需要的顶层字段
DROP_TOP = {
    "listeners", "geodata-mode", "geo-auto-update", "geo-update-interval", "geox-url",
    "unified-delay", "tcp-concurrent", "find-process-mode", "global-client-fingerprint",
    "mixed-port", "allow-lan", "auto-test",
}
DROP_GROUPS = {"AdsPower"}

ICON = "https://raw.githubusercontent.com/Koolson/Qure/master/IconSet/Color/{}.png"
ICONS = {
    "节点选择": "Proxy", "自动选择": "Auto", "全部节点": "Global",
    "TAG-GLOBAL": "Airport", "EdNovas": "Airport",
    "WhatsApp": "Facebook", "Muse": "AI", "Manus": "AI", "AI工具": "ChatGPT",
    "流媒体": "Streaming", "TikTok": "TikTok", "美国金融": "PayPal", "Wise": "Bypass",
    "Blued": "Rainbow", "LGBT应用": "Rainbow_1", "LINE": "Line", "X": "X",
    "微信": "WeChat", "小红书": "Domestic", "抖音": "TikTok_1",
    "英国金融": "United_Kingdom", "中建集团": "China_Map", "国内流媒体": "DomesticMedia",
    "谷歌服务": "Google", "苹果服务": "Apple", "漏网之鱼": "Final",
    "香港节点": "Hong_Kong", "台湾节点": "Taiwan", "日本节点": "Japan",
    "新加坡节点": "Singapore", "韩国节点": "Korea", "美国节点": "United_States",
    "英国节点": "United_Kingdom", "德国节点": "Germany", "中国大陆节点": "China",
}

# 替代 GEOSITE,private / GEOIP,private
LAN_RULES = [
    "DOMAIN-SUFFIX,local,DIRECT",
    "DOMAIN-SUFFIX,lan,DIRECT",
    "IP-CIDR,10.0.0.0/8,DIRECT,no-resolve",
    "IP-CIDR,172.16.0.0/12,DIRECT,no-resolve",
    "IP-CIDR,192.168.0.0/16,DIRECT,no-resolve",
    "IP-CIDR,127.0.0.0/8,DIRECT,no-resolve",
    "IP-CIDR,169.254.0.0/16,DIRECT,no-resolve",
    "IP-CIDR,100.64.0.0/10,DIRECT,no-resolve",
    "IP-CIDR6,fe80::/10,DIRECT,no-resolve",
]

HEADER = """\
# ================================================
# Stash 专用配置（iPhone / iPad / Mac）
# ⚠️ 本文件由 scripts/make_stash.py 根据 flclash-config.yaml 自动生成，请不要直接修改
# 用法：Stash 里用 URL 导入本文件（自动更新），
# 再导入覆写 stash-subs.stoverride 填入机场订阅链接，见 README「Stash 设置」
# 与 FlClash 版的区别：没有 AdsPower 专用端口（7891），安卓包名规则在 Stash 上不生效
# ================================================

"""


def convert(cfg):
    out = {k: v for k, v in cfg.items() if k not in DROP_TOP}

    for p in out.get("proxy-providers", {}).values():
        for k in ("override", "health-check", "type"):
            p.pop(k, None)

    groups = []
    for g in out.get("proxy-groups", []):
        if g["name"] in DROP_GROUPS:
            continue
        if "proxies" in g:
            g["proxies"] = [x for x in g["proxies"] if x not in DROP_GROUPS]
        ex = g.pop("exclude-filter", None)
        if ex and "filter" in g:
            g["filter"] = f"^(?!.*({ex})).*({g['filter']})"
        if g.get("type") == "url-test":
            g.pop("url", None)
            g["lazy"] = True
        if g["name"] in ICONS:
            g["icon"] = ICON.format(ICONS[g["name"]])
        groups.append(g)
    out["proxy-groups"] = groups

    rules = []
    for r in out.get("rules", []):
        if r.startswith(("GEOSITE,private", "GEOIP,private")):
            if not rules or rules[0] != LAN_RULES[0]:
                rules.extend(LAN_RULES)
            continue
        rules.append(r)
    out["rules"] = rules
    return out


def main():
    with open(SRC, encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    body = yaml.safe_dump(convert(cfg), allow_unicode=True, sort_keys=False, width=200)
    text = HEADER + body
    old = open(DST, encoding="utf-8").read() if os.path.exists(DST) else ""
    if text != old:
        with open(DST, "w", encoding="utf-8") as f:
            f.write(text)
        print("已生成 stash-config.yaml")
    else:
        print("stash-config.yaml 无变化")


if __name__ == "__main__":
    sys.exit(main())
