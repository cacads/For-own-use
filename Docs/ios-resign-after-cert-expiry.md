# 证书过期后的重签名恢复流程

> 设备：iPhone · iOS 27.0.1 (24A446) · 侧载应用 33 个（自签 31 + TestFlight 2）

> 目标：新证书到手后，**一次性下载 → 重签名 → 原地覆盖安装**，App 数据不丢。

> 本文只写步骤和清单，不涉及在本机自动执行。


---

## 步骤总览

| 步骤 | 做什么 | 产出 |
|---|---|---|
| 1 | 准备证书和描述文件 | `证书.p12` + `描述文件.mobileprovision` + p12 密码 |
| 2 | 装一个签名工具（LCSign / Feather / 全能签） | 能用的签名客户端 |
| 3 | 用第 1 步的证书签签名工具本体并装上 | 签名工具可运行 |
| 4 | 导入证书到签名工具 | 证书可选中 |
| 5 | 下载下方清单里的 ipa | 原始 ipa |
| 6 | 逐个重新签名 | 新签名的 ipa |
| 7 | 覆盖安装（不清数据） | App 重新可用 |
| 8 | 补做清单里「源里没有」的 19 个 | 逐个手工处理 |

---

## 步骤 1：准备证书

证书过期后需要先用 Apple ID（或开发者账号）重新导出：

- 通过 **Apple Developer**（免费账号也有）→ Certificates → 创建 **Apple Development / iOS Development** 证书 → 导出 `.p12`（记住密码）
- 或通过 **Sideloadly / AltStore / Feather 内置的「从 Apple ID 生成证书」** 生成新的 p12 + mobileprovision
- 描述文件必须与证书匹配（同一 Team），且有效期覆盖今天
- 建议另存一份到 iCloud 或 Feather 沙盒 `Documents/Certificates/`，以后续签直接复用

> 本机原证书已备份在 Feather 沙盒：`Documents/Certificates/7BA0703A-C9B1-4FF0-9662-FFD436B84962/`（`证书文件.p12` + `描述文件.mobileprovision`）。如果它还没被删，签名工具掉签时可以直接用它重签。

## 步骤 2-3：安装签名工具本体

证书过期 = 签名工具本身也打不开了，所以必须先「用新证书签一次签名工具」。**LCSign 提供了网页端代签**，不用电脑：

1. 打开 https://www.sign.lc/install
2. 上传新证书：可传 ZIP（p12 + mobileprovision + 密码 txt），或分别上传 `.p12` 与 `.mobileprovision`
3. 也可点「使用存取码」，填之前 LCSign 备份证书时给的码
4. 点「签名并分发」→ 服务器用你的证书签 LCSign 本体
5. 弹出系统安装弹窗 → 确认 → LCSign 安装完成

备选签名工具（同样要先用新证书签它们本体）：

- **Feather** 2.9.0：https://github.com/claration/feather/releases/download/v2.9.0/Feather.ipa（AltGallery 源里也有）
- **全能签** `signall.nuosike.sign` / **小源签** `fan.ipapkk.iosq`：本机已装，但官方安装页需要自己找（见第三节）

## 步骤 4：把证书导入签名工具

以 LCSign 为例：打开 LCSign → 证书管理 → 导入 p12 + 描述文件 + 密码 → 设为默认签名证书。

Feather 同理：`Files/Feather/Certificates` 或 App 内 Certificates → Import。

下载的 ipa 放到「文件」App 里任意目录，签名工具能让它访问即可（Feather 建议放 `文件/Feather/Unsigned`）。

## 步骤 5-7：下载 → 重签 → 覆盖安装

要点：

- **Bundle ID 保持不变**，直接覆盖安装，App 内的数据、登录态都会保留；改了 ID 就变成分身，数据不继承
- 先装 ipa 再签名和先签名再装都行，但**同一个 app 不要同时存在两个不同签名的副本**，会互相覆盖报错
- 安装时如果提示「无法安装 / 证书无效」，一般是描述文件与 p12 不匹配，或描述文件里没包含该 Bundle ID
- 全部装完后再检查一遍各 App 是否能正常打开，尤其是要读 Keychain 的（如浏览器、下载器）


---

## 一、源里有、可直接下载的 14 个

AltGallery 源里 Bundle ID 完全一致，点链接即可下载 ipa（`本机 ⬆` = 源内版本比已装的新）。

| 应用 | Bundle ID | 已装版本 | 源内版本 | 开发者 | 下载链接 |
|---|---|---|---|---|---|
| Aidoku | `app.aidoku.Aidoku` | 0.9 | 0.9 | [IPA](https://github.com/Aidoku/Aidoku/releases/download/v0.9-4/Aidoku.ipa) |
| AirCard-iOS | `com.mak5er.aircard` | 1.3.2 | 1.3.2 | [IPA](https://github.com/Mak5er/AirCard-iOS/releases/download/v1.3.2/AirCard-iOS.ipa) |
| EhPanda | `app.ehpanda` | 2.8.1 | 2.8.1 | [IPA](https://github.com/EhPanda-Team/EhPanda/releases/download/v2.8.1/EhPanda.ipa) |
| Feather | `thewonderofyou.Feather` | 2.9.0 | 2.9.0 | [IPA](https://github.com/claration/feather/releases/download/v2.9.0/Feather.ipa) |
| GestaltX | `com.huami.gestultx` | 1.0.6 | 1.0.5 ⬆ | [IPA](https://github.com/huamidev/GestaltX/releases/download/v1.0.5/GestaltX_1.0.5.ipa) |
| iTorrent | `com.xitrix.iTorrent2` | 2.2.0 | 2.2.0-1 ⬆ | [IPA](https://github.com/XITRIX/iTorrent/releases/download/v2.2.0-1/iTorrent.ipa) |
| Kumone | `sb.moe.kumone-ios` | 0.3.28 | 0.3.32 ⬆ | [IPA](https://github.com/missuo/kumone/releases/download/v0.3.32/Kumone-iOS-0.3.32.ipa) |
| MiniWatts | `org.zhaohe.MiniWatts` | 1.6.0 | 1.7.0 ⬆ | [IPA](https://github.com/ResistanceTo/MiniWatts/releases/download/v1.7.0/MiniWatts-unsigned.ipa) |
| PiliPlus | `com.example.piliplus` | 2.2.0 | 2.2.0 | [IPA](https://github.com/bggRGjQaUbCoE/PiliPlus/releases/download/2.2.0.2/PiliPlus_ios_2.2.0%2B5598.ipa) |
| Pixiv-SwiftUI | `org.eu.eslzzyl.Pixiv-SwiftUI` | 0.16.3 | 0.16.3 | [IPA](https://github.com/Eslzzyl/Pixiv-SwiftUI/releases/download/v0.16.3/Pixiv-SwiftUI.ipa) |
| Pure Live | `com.mystyle.purelive.liu` | 3.1.19 | 3.1.19 | [IPA](https://github.com/liuchuancong/pure_live/releases/download/v3.1.19/PureLive-3.1.19-4108-ios-arm64-trollstore.ipa) |
| StikDebug | `com.stik.stikdebug` | 3.2.0 | 3.2.2 ⬆ | [IPA](https://github.com/StikDebug/StikDebug/releases/download/3.2.2/StikDebug-3.2.2.ipa) |
| WQ 文件 | `cz.kolbi.wqfiles` | 0.8 | 0.9.3 ⬆ | [IPA](https://github.com/kolbicz/WQFiles/releases/download/v0.9.3/WQFiles.ipa) |
| 知乎-- | `com.huamu013.ZhihuMinusMinus` | 0.9.5 | 0.9.10 ⬆ | [IPA](https://github.com/huamurui/zhihu-minus-minus/releases/download/v0.9.10/zhihu-minus-minus-v0.9.10-unsigned.ipa) |

## 二、源里没有的 19 个（GitHub 已核过）

2026-11 用 GitHub API 逐个搜过仓库名与 bundle id，结论写在各行「备注」里：**真正开源且有 Release 的一个都没有**，都不是「忘了搜」的漏网。

- 有源码但没发布 ipa：iOS HUB(`zym-cpu/iOSHUB`，源码在 rar 里)、Simple Live(`xiaoyaocz/dart_simple_live`)、AirBeep(`AirBeep/AirBeep` 空仓库)
- 搜到同名但不是同一个 App：wloc(`Yu9191/wloc` 是 Surge 脚本)、亚瑟浏览器(PC 版 Chromium)、Mori、Swipt
- 商业 App：扫描全能王、Trace
- 不是 ipa：Octans / Relay(TestFlight)、iCTRL Runner(随 iCTRL 走)
- 签名工具本体：LCSign / 全能签 / 小源签，走各自官方安装页

**你现在能装着它们，就说明你手上有能拿到它们的渠道**（内部/私源/频道），这部分按你原来的方式重新下载即可。


| 应用 | Bundle ID | 已装版本 | 类型 | 备注（GitHub 核查结论） |
|---|---|---|---|---|
| AirBeep | `com.linkpass888.airbeep` | 2.5.2 | 自签 | `AirBeep/AirBeep` 是空仓库无 Release；**Feather 里留有已签包** `Signed/5B85C2C0…/airbeep.app` |
| iBox | `com.super.tvbox` | 2.5.0 | 自签 | 无独立开源仓库，靠频道分发 |
| iCTRLUITests-Runner | `com.openminis.ictrl.uitests.xctrunner` | 1.0 | 自签 | iCTRL 自带 Runner，随 iCTRL 一起重签 |
| iOS HUB | `com.nevercrynow.ioshub` | 1.0 | 自签 | `zym-cpu/iOSHUB` 只有源码（`iOSHUB.rar`），需自编译 |
| LCSign | `com.huami.LoadController` | 1.4 | 自签 | 签名工具本体，走 https://www.sign.lc/install |
| Mori | `com.mori.downloader` | 4.5.1 | 自签 | GitHub 同名仓库都不是这个 App，别装错 |
| Octans | `app.qpomelo.pigeon` | 1.0 | ⛔ TestFlight | 不是 ipa，需 TestFlight 邀请 |
| Relay | `net.sodion.relay-app` | 1.0.1 | ⛔ TestFlight | 不是 ipa，需 TestFlight 邀请 |
| Rex | `tv.rexnow.app` | 1.0.1 | 自签 | 无独立开源仓库，靠频道分发 |
| Roam Control | `com.roamcontrol` | 0.9.9 | 自签 | 源里 `com.sean.roamcontrol` 同名不同 ID，装错会变分身 |
| Simple Live | `com.xycz.simple-live` | 1.13.2 | 自签 | `xiaoyaocz/dart_simple_live` 是 Flutter 源码，无 iOS Release |
| Swipt | `io.nekohasekai.swipt` | 0.1.0 | 自签 | GitHub 同名仓库与 iOS 无关 |
| Trace | `com.morpholioapps.trace` | 6.86 | 自签 | 商业 App，非开源 |
| wloc | `com.yu9191.wloc` | 1.2.1 | 自签 | `Yu9191/wloc` 是 Surge/Loon 脚本，不是这个 App |
| 亚瑟浏览器 | `com.lxm.ysbrowser` | 25.6 | 自签 | GitHub 上是 PC 版 Chromium，无关；**Feather 里留有已签包** `Signed/37BE4888…/YSBrowser.app` |
| 全能签 | `signall.nuosike.sign` | 27.1.0 | 自签 | 签名工具本体，走官方安装页 |
| 小源签 | `fan.ipapkk.iosq` | 1.4.0 | 自签 | 签名工具本体，走官方安装页 |
| 扫描全能王 | `com.intsig.CamScannerLite` | 7.26.6 | 自签 | 商业 App，可换 App Store 正版 |
| 飓风相机 | `com.ysjf.lutcamera` | 1.8.7 | 自签 | GitHub 无对应仓库 |

## 三、签名工具本体的安装页（证书过期时最先要用）

| 工具 | Bundle ID | 安装方式 |
|---|---|---|
| LCSign | `com.huami.LoadController` | https://www.sign.lc/install （上传 p12+描述文件，服务器代签） |
| Feather | `thewonderofyou.Feather` | [GitHub Releases IPA](https://github.com/claration/feather/releases/download/v2.9.0/Feather.ipa) 或 AltGallery 源，自己签 |
| 全能签 | `signall.nuosike.sign` | 待补（官方页面需自行确认，避免装到山寨包） |
| 小源签 | `fan.ipapkk.iosq` | 待补（同上） |

---

## 重新续签时注意

- 免费 Apple ID 证书 **7 天**有效，开发者账号 **1 年**；到期前 1-2 天重签最省事，过期后 App 会直接打不开（图标还在，点开闪退）
- 重签**不需要卸载**，直接覆盖安装即可，不要把步骤做成「先删后装」
- Feather 的 `Documents/Signed/` 里有 15 个历史签名包（Aidoku / KumoneIOS / Pixiv-SwiftUI / airbeep / RoamControl / AirCard-iOS / LoadController / iTorrent / EhPanda / MiniWatts / MediaStormCamera / Player / YSBrowser / Runner×2），万一源里某个 ipa 拿不到了，可以从这里取出 `.app` 重新打包
- 新证书的 Team ID 变了也没关系，覆盖安装靠的是 Bundle ID 一致

