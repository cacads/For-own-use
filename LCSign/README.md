# 自用源 · iOS 侧载 / 自签应用集合

给 LCSign（[sign.lc](https://www.sign.lc)）用的软件源，格式兼容 AltStore。
收录的是**我这台手机上实际安装的**第三方应用，其中开源的自动跟踪 GitHub Releases 最新版，
闭源应用只作索引记录（无下载链接）。

## 订阅地址

```
https://raw.githubusercontent.com/cacads/For-own-use/refs/heads/master/LCSign/source.json
```

在 LCSign 里添加：`设置 → 软件源 → 添加`，或直接点下面的链接：

[**一键添加到 LCSign**](loadcontroller://addsource?url=https%3A%2F%2Fraw.githubusercontent.com%2Fcacads%2FFor-own-use%2Frefs%2Fheads%2Fmaster%2FLCSign%2Fsource.json)

> 若要更新，建议用 **jsDelivr CDN**（国内访问更快，raw.githubusercontent 常被墙）：
> ```
> https://cdn.jsdelivr.net/gh/cacads/For-own-use@master/LCSign/source.json
> ```
> 注意 jsDelivr 有约 12 小时缓存，刚推送的新版不会立刻生效。

## 收录清单

| 分类 | 应用 | 本机版本 | 最新版本 | 来源 |
|---|---|---|---|---|
| 签名工具 | Feather | 2.9.0 | 2.9.0 | [claration/feather](https://github.com/claration/feather) |
| 签名工具 | LCSign | 1.4 | 1.4 | 官方 `res.lcsignx.com` |
| 签名工具 | 小源签 | 1.4.0 | — | 闭源 |
| 签名工具 | 全能签 | 27.1.0 | — | 闭源 |
| 系统调试 | StikDebug | 3.1.15 | **3.2.0** | [StikDebug/StikDebug](https://github.com/StikDebug/StikDebug) |
| 系统调试 | AirCard-iOS | 1.3.2 | 1.3.2 | [Mak5er/AirCard-iOS](https://github.com/Mak5er/AirCard-iOS) |
| 系统调试 | MiniWatts | 1.6.0 | 1.6.0 | [ResistanceTo/MiniWatts](https://github.com/ResistanceTo/MiniWatts) |
| 系统调试 | Roam Control | 0.9.9 | 0.9.9 | [seanhowarthdev/Roam-Control](https://github.com/seanhowarthdev/Roam-Control) |
| 系统调试 | AirBeep | 2.5.2 | — | 闭源 |
| 系统调试 | iCTRL Runner | 1.0 | — | XCUITest runner，自签 |
| 影音下载 | PiliPlus | 2.2.0 | **2.2.0.2** | [bggRGjQaUbCoE/PiliPlus](https://github.com/bggRGjQaUbCoE/PiliPlus) |
| 影音下载 | EhPanda | 2.8.1 | 2.8.1 | [EhPanda-Team/EhPanda](https://github.com/EhPanda-Team/EhPanda) |
| 影音下载 | Aidoku | 0.9 | **0.9-4** | [Aidoku/Aidoku](https://github.com/Aidoku/Aidoku) |
| 影音下载 | iTorrent | 2.2.0 | **2.2.0-1** | [XITRIX/iTorrent](https://github.com/XITRIX/iTorrent) |
| 影音下载 | Kumone | 0.3.28 | 0.3.28 | [missuo/kumone](https://github.com/missuo/kumone) |
| 影音下载 | Mori | 4.5.1 | 4.5.1 | [coflyn/Mori](https://github.com/coflyn/Mori) |
| 影音下载 | Pixiv-SwiftUI | 0.16.3 | 0.16.3 | [Eslzzyl/Pixiv-SwiftUI](https://github.com/Eslzzyl/Pixiv-SwiftUI) |
| 影音下载 | Simple Live | 1.13.2 | — | [xiaoyaocz/dart_simple_live](https://github.com/xiaoyaocz/dart_simple_live)（无 IPA 发布） |
| 影音下载 | Pure Live | 3.1.19 | — | 闭源 |
| 浏览电视 | 亚瑟浏览器 / iBox / Rex / 知乎-- | — | — | 闭源 |
| 摄影工具 | 飓风相机 / 扫描全能王 / Trace | — | — | 闭源 |

**加粗** = 比本机安装的新，值得更新。

## 文件结构

```
LCSign/
├── source.json        ← 软件源本体（AltStore / LCSign 格式）
├── App_icons/         ← 源图标、头图、5 个分类图标
├── build_source.py    ← 重新生成 source.json
├── update-source.yml  ← 定时刷新工作流说明
└── README.md

.github/workflows/update-source.yml  ← 每日自动刷新
```

## 自动更新

`update-source.yml` 每天定时（以及手动触发）重新拉取各仓库的最新 Release，
有变化就自动提交 `LCSign/source.json`。

本地手动刷新：

```bash
GITHUB_TOKEN=<your_token> python3 LCSign/build_source.py
```

## 免责声明

仅为自己使用。所有应用版权归各自作者所有，本项目仅提供索引与下载链接转发，
不托管任何二进制文件。请遵守所在地区法律法规，不得商用。
