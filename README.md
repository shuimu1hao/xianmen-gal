# 仙门物语（xianmen-gal）

网页版文字恋爱游戏（galgame / 视觉小说）。纯前端实现：`data.js` 存剧情数据，`index.html` 是游戏引擎，AI 生成的立绘放 `assets/`。

## 运行

直接打开 `index.html`，或起个静态服务器：

```bash
cd xianmen-gal
python3 -m http.server 8080
```

浏览器访问 http://localhost:8080

## 目录

- `data.js` — 剧情/角色/分支数据
- `index.html` — 游戏引擎（对话框/立绘/选项分支）
- `assets/` — 角色立绘与素材
- `gen_assets.py` — 立绘生成脚本

## 协议

MIT License（见 LICENSE）
