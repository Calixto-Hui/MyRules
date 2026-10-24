#!/usr/bin/env python3
"""每天自动更新规则：拉取上游规则 + 合并 custom/ 里的自定义域名，生成根目录下的 *.yaml。

只用 Python 标准库，GitHub Actions 自带的 Python 就能跑。
某个上游拉取失败时，保留该文件的旧版本，不会把规则清空。
"""
import datetime
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BM = "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash"
V2FLY = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data"
VPSDANCE = "https://raw.githubusercontent.com/VPSDance/ai-proxy-rules/main/rules/clash"

# 输出文件 -> (标题, 上游列表)。上游为空表示只用 custom/ 里手动维护的内容。
RULES = {
    "muse": ("Muse (Meta AI)", [f"{VPSDANCE}/meta-ai.yaml"]),
    "wise": ("Wise 国际汇款（原 TransferWise）", [f"{V2FLY}/wise"]),
    "paypal": ("PayPal（含 Braintree、Venmo 等）", [f"{BM}/PayPal/PayPal.yaml"]),
    "blued": ("Blued", [f"{BM}/Blued/Blued.yaml"]),
    "lgbt": ("LGBT 社交应用（Grindr / Hornet / Jack'd / Scruff / Romeo / Taimi / HER）", []),
    "streaming": ("流媒体（Netflix / YouTube / Disney+ / HBO / Prime Video / Spotify / TikTok）", [
        f"{BM}/Netflix/Netflix_Classical.yaml",
        f"{BM}/YouTube/YouTube.yaml",
        f"{BM}/Disney/Disney.yaml",
        f"{BM}/HBO/HBO.yaml",
        f"{BM}/PrimeVideo/PrimeVideo.yaml",
        f"{BM}/Spotify/Spotify.yaml",
        f"{BM}/TikTok/TikTok.yaml",
    ]),
    "apple": ("Apple", [f"{BM}/Apple/Apple_Classical.yaml"]),
    "google": ("Google", [f"{BM}/Google/Google.yaml"]),
}

RULE_TYPES = ("DOMAIN", "DOMAIN-SUFFIX", "DOMAIN-KEYWORD", "DOMAIN-REGEX", "IP-CIDR",
              "IP-CIDR6", "IP-ASN", "PROCESS-NAME", "PROCESS-PATH", "GEOIP", "GEOSITE")


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "my-rules-updater"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read().decode("utf-8")


def parse_clash_yaml(text):
    out = []
    for line in text.splitlines():
        m = re.match(r"^\s*-\s+(.+?)\s*$", line)
        if m and m.group(1).split(",")[0] in RULE_TYPES:
            out.append(m.group(1).strip("'\""))
    return out


def parse_v2fly(text):
    out = []
    for line in text.splitlines():
        line = line.split("#")[0].strip()
        if not line or line.startswith(("include:", "regexp:", "keyword:")):
            continue
        dom = line.split()[0]  # 去掉 @attr
        if dom.startswith("full:"):
            out.append(f"DOMAIN,{dom[5:]}")
        else:
            out.append(f"DOMAIN-SUFFIX,{dom.removeprefix('domain:')}")
    return out


def parse_upstream(url, text):
    rules = parse_v2fly(text) if url.startswith(V2FLY) else parse_clash_yaml(text)
    if not rules:
        raise ValueError("上游返回内容里没有规则")
    return rules


def read_custom(name):
    path = os.path.join(ROOT, "custom", f"{name}.txt")
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line and not line.startswith("#"):
            out.append(line)
    return out


def build(name, title, upstreams):
    rules = []
    for url in upstreams:
        rules += parse_upstream(url, fetch(url))
    rules += read_custom(name)
    seen, uniq = set(), []
    for r in rules:
        if r not in seen:
            seen.add(r)
            uniq.append(r)
    if not uniq:
        raise ValueError("合并后为空")
    lines = [f"# NAME: {title}"]
    lines += [f"# SOURCE: {u}" for u in upstreams]
    lines += [f"# CUSTOM: custom/{name}.txt", f"# TOTAL: {len(uniq)}", "payload:"]
    lines += [f"  - {r}" for r in uniq]
    return "\n".join(lines) + "\n"


def main():
    failed = []
    for name, (title, upstreams) in RULES.items():
        path = os.path.join(ROOT, f"{name}.yaml")
        try:
            content = build(name, title, upstreams)
        except Exception as e:  # 拉取或解析失败：保留旧文件
            print(f"[跳过] {name}: {e}", file=sys.stderr)
            failed.append(name)
            continue
        old = open(path, encoding="utf-8").read() if os.path.exists(path) else ""
        if content != old:
            open(path, "w", encoding="utf-8").write(content)
            print(f"[更新] {name}.yaml ({content.count(chr(10) + '  - ')} 条)")
        else:
            print(f"[无变化] {name}.yaml")
    print(f"完成于 {datetime.datetime.now(datetime.timezone.utc):%Y-%m-%d %H:%M} UTC")
    if len(failed) == len(RULES):
        sys.exit(1)


if __name__ == "__main__":
    main()
