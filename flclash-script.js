// FlClash 覆写脚本：把机场订阅链接填进 flclash-config.yaml
//
// 用法：FlClash →「配置」→ 右上角「脚本」→ 新建脚本，把本文件全部内容粘贴进去，
//      把下面两个引号里的内容换成你的订阅链接，保存；
//      然后在 URL 导入的那个配置上，把「覆写」设为这个脚本。
//
// ⚠️ 填好链接的脚本只存在你自己的 FlClash 里，不要提交到 GitHub（仓库是公开的）。

function main(config) {
  const subs = {
    "TAG-GLOBAL": "这里粘贴TAG-GLOBAL的订阅链接",
    "EdNovas": "这里粘贴EdNovas的订阅链接",
  };

  const providers = config["proxy-providers"] || {};
  for (const name in subs) {
    if (providers[name]) {
      providers[name].url = subs[name];
    }
  }
  return config;
}
