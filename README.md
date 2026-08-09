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

## 开发环境

- 设备：小米手机（MIUI / Android 13）
- 环境：Termux（Android 终端）+ termux-x11 + XFCE 图形桌面
- 语言：Go / Python 为主，纯 CLI 开发
- 注意：本项目在 Android / Termux 上开发与测试，其他平台运行可能需要调整

## 生成声明

本项目全部代码与文档由 AI 生成（Hermes Agent + DeepSeek 模型），不含一丝人类手写代码。仅供学习交流。

## 寻求帮助

本项目是 AI 生成的实验性游戏/引擎，仍需社区帮助测试与改进：
- 欢迎提交 Issue 反馈 Bug、卡关、体验问题
- 欢迎 PR 改进玩法、数值、画面、平台兼容性
- 目前主要在 Android / Termux 上测试，欢迎在其他平台测试反馈
