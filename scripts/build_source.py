#!/usr/bin/env python3
"""生成 LCSign / AltStore 兼容软件源 JSON"""
import json, os, re, time, urllib.request, urllib.error

TOKEN = os.environ.get('GITHUB_TOKEN', '')
REPO = 'cacads/For-own-use'
BRANCH = 'master'
RAW = f'https://raw.githubusercontent.com/{REPO}/refs/heads/{BRANCH}'

# 手机上实际安装的第三方应用（名称, bundleId, 已装版本, GitHub 仓库/None）
# repo 为 None = 闭源或未找到公开源，仍列出但标记为手动更新
APPS = [
    # ── 签名工具 ──
    dict(name='Feather', bid='thewonderofyou.Feather', ver='2.9.0', repo='claration/feather',
         dev='claration', cat='签名工具', desc='开源的 iOS 设备端签名与应用管理工具。'),
    dict(name='LCSign', bid='com.huami.LoadController', ver='1.4', repo=None,
         dev='huamidev', cat='签名工具', desc='简洁顺手的 iOS 签名工具，支持 IPA 签名、插件注入与安装。',
         extra_url='https://res.lcsignx.com/LCSign.ipa'),
    dict(name='小源签', bid='fan.ipapkk.iosq', ver='1.4.0', repo=None,
         dev='小源签', cat='签名工具', desc='iOS 签名分发工具（闭源）。'),
    dict(name='全能签', bid='signall.nuosike.sign', ver='27.1.0', repo=None,
         dev='全能签', cat='签名工具', desc='全能签名工具，支持证书管理与 IPA 签名安装（闭源）。'),
    # ── 系统调试 ──
    dict(name='StikDebug', bid='com.stik.stikdebug', ver='3.1.15', repo='StikDebug/StikDebug',
         dev='StikDebug', cat='系统调试', desc='设备端调试器与 JIT 启用工具，为模拟器等场景提供支持。'),
    dict(name='AirCard-iOS', bid='com.mak5er.aircard', ver='1.3.2', repo='Mak5er/AirCard-iOS',
         dev='Mak5er', cat='系统调试', desc='Apple Wallet 卡片皮肤与锁屏密码界面定制（无需越狱）。'),
    dict(name='MiniWatts', bid='org.zhaohe.MiniWatts', ver='1.6.0', repo='ResistanceTo/MiniWatts',
         dev='ResistanceTo', cat='系统调试', desc='iPhone 电池、充电与温度仪表盘。'),
    dict(name='Roam Control', bid='com.roamcontrol', ver='0.9.9', repo='seanhowarthdev/Roam-Control',
         dev='seanhowarthdev', cat='系统调试', desc='选择、测试并迁移 iPhone 报告的位置。'),
    dict(name='AirBeep', bid='com.linkpass888.airbeep', ver='2.5.2', repo=None,
         dev='LinkPass888', cat='系统调试', desc='通话录音提示音处理工具（闭源分发）。'),
    dict(name='iCTRL Runner', bid='com.openminis.ictrl.uitests.xctrunner', ver='1.0', repo=None,
         dev='OpenMinis', cat='系统调试', desc='iCTRL 的 XCUITest 常驻 runner，提供 HTTP JSON-RPC 设备自动化接口。'),
    # ── 影音下载 ──
    dict(name='PiliPlus', bid='com.example.piliplus', ver='2.2.0', repo='bggRGjQaUbCoE/PiliPlus',
         dev='bggRGjQaUbCoE', cat='影音下载', desc='第三方 Bilibili 客户端，支持多端同步。'),
    dict(name='EhPanda', bid='app.ehpanda', ver='2.8.1', repo='EhPanda-Team/EhPanda',
         dev='EhPanda-Team', cat='影音下载', desc='使用 SwiftUI 与 TCA 构建的非官方 E-Hentai 客户端。'),
    dict(name='Aidoku', bid='app.aidoku.Aidoku', ver='0.9', repo='Aidoku/Aidoku',
         dev='Skitty', cat='影音下载', desc='免费开源的 iOS/iPadOS 漫画阅读器，支持多源。'),
    dict(name='iTorrent', bid='com.xitrix.iTorrent2', ver='2.2.0', repo='XITRIX/iTorrent',
         dev='XITRIX', cat='影音下载', desc='iOS 端全功能 BitTorrent 客户端，支持后台下载。'),
    dict(name='Kumone', bid='sb.moe.kumone-ios', ver='0.3.28', repo='missuo/kumone',
         dev='missuo', cat='影音下载', desc='使用 SwiftUI 构建的跨平台原生音乐播放器。'),
    dict(name='Mori', bid='com.mori.downloader', ver='4.5.1', repo='coflyn/Mori',
         dev='coflyn', cat='影音下载', desc='客户端侧媒体下载器 App 与 CLI。'),
    dict(name='Pixiv-SwiftUI', bid='org.eu.eslzzyl.Pixiv-SwiftUI', ver='0.16.3', repo='Eslzzyl/Pixiv-SwiftUI',
         dev='Eslzzyl', cat='影音下载', desc='为现代 Apple 平台设计的第三方 Pixiv 客户端。'),
    dict(name='Simple Live', bid='com.xycz.simple-live', ver='1.13.2', repo='xiaoyaocz/dart_simple_live',
         dev='xiaoyaocz', cat='影音下载', desc='简简单单的看直播，聚合多平台直播源。'),
    dict(name='Pure Live', bid='com.mystyle.purelive.liu', ver='3.1.19', repo=None,
         dev='mystyle', cat='影音下载', desc='简洁的直播聚合客户端（闭源分发）。'),
    # ── 浏览电视 ──
    dict(name='亚瑟浏览器', bid='com.lxm.ysbrowser', ver='25.6', repo=None,
         dev='lxm', cat='浏览电视', desc='内置书签与影视源的浏览器（闭源）。'),
    dict(name='iBox', bid='com.super.tvbox', ver='2.5.0', repo=None,
         dev='super', cat='浏览电视', desc='影视聚合盒子，支持自定义接口（闭源）。'),
    dict(name='Rex', bid='tv.rexnow.app', ver='1.0.1', repo=None,
         dev='rexnow', cat='浏览电视', desc='影视资源聚合客户端（闭源）。'),
    dict(name='知乎--', bid='com.huamu013.ZhihuMinusMinus', ver='0.9.5', repo=None,
         dev='huamu013', cat='浏览电视', desc='轻量知乎客户端（去广告精简版）。'),
    # ── 摄影工具 ──
    dict(name='飓风相机', bid='com.ysjf.lutcamera', ver='1.8.7', repo=None,
         dev='ysjf', cat='摄影工具', desc='支持 LUT 的专业相机应用（闭源）。'),
    dict(name='扫描全能王', bid='com.intsig.CamScannerLite', ver='7.26.6', repo=None,
         dev='IntSig', cat='摄影工具', desc='文档扫描与 OCR 识别工具。'),
    dict(name='Trace', bid='com.morpholioapps.trace', ver='6.86', repo=None,
         dev='Morpholio', cat='摄影工具', desc='设计草图与速写应用。'),
]

CAT_ICONS = {
    '签名工具': 'sign', '系统调试': 'debug', '影音下载': 'media',
    '浏览电视': 'tv', '摄影工具': 'photo',
}


def api(url, tries=4):
    last = None
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={
                'Authorization': 'Bearer ' + TOKEN,
                'Accept': 'application/vnd.github+json',
                'User-Agent': 'minis-lcsign-source'})
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:
            last = e
            time.sleep(3 * (i + 1))
    raise last


def fetch_releases(repo):
    rels = api(f'https://api.github.com/repos/{repo}/releases?per_page=30')
    out = []
    for r in rels:
        if r.get('draft'):
            continue
        ipas = [a for a in r.get('assets', []) if a['name'].lower().endswith(('.ipa', '.tipa'))]
        if not ipas:
            continue
        ipa = max(ipas, key=lambda a: a['size'])
        tag = r['tag_name']
        ver = re.sub(r'^v', '', tag)
        out.append(dict(
            version=ver, tag=tag, date=(r['published_at'] or '')[:10],
            url=ipa['browser_download_url'], size=ipa['size'],
            notes=(r.get('body') or '').strip()[:1200],
            prerelease=r.get('prerelease', False)))
    return out


def main():
    apps = []
    for a in APPS:
        entry = dict(
            name=a['name'], bundleIdentifier=a['bid'], developerName=a['dev'],
            subtitle=a['cat'], localizedDescription=a['desc'],
            category=a['cat'], versions=[])
        if a.get('repo'):
            try:
                rels = fetch_releases(a['repo'])
                stable = [r for r in rels if not r['prerelease']]
                ordered = stable + [r for r in rels if r['prerelease']]
                for r in ordered:
                    entry['versions'].append(dict(
                        version=r['version'], date=r['date'],
                        localizedDescription=r['notes'] or f"{a['name']} {r['version']}",
                        downloadURL=r['url'], size=r['size'],
                        minOSVersion='15.0'))
                print(f"  {a['name']:16} {len(entry['versions'])} 个版本 (最新 {ordered[0]['version'] if ordered else '-'})")
            except Exception as e:
                print(f"  {a['name']:16} 拉取失败: {str(e)[:60]}")
        else:
            if a.get('extra_url'):
                entry['versions'].append(dict(
                    version=a['ver'], date='2026-11-05', minOSVersion='15.0',
                    localizedDescription=f"{a['name']} {a['ver']}（官方离线安装包）",
                    downloadURL=a['extra_url'], size=0))
            print(f"  {a['name']:16} 闭源 / 无公开源")
        entry['_installedVersion'] = a['ver']
        apps.append(entry)

    # 按分类排序
    order = list(CAT_ICONS.keys())
    apps.sort(key=lambda x: (order.index(x['subtitle']) if x['subtitle'] in order else 99, x['name']))

    source = dict(
        name='Cacads 自用源',
        subtitle='我手机上装的自签 / 侧载应用',
        description='本机实际安装的第三方应用集合，多来自 GitHub Releases，'
                    '闭源应用仅作索引记录。此源按 LCSign / AltStore 格式生成。',
        iconURL=f'{RAW}/App_icons/icon.png',
        headerURL=f'{RAW}/App_icons/header.png',
        website=f'https://github.com/{REPO}',
        tintColor='#1F5E4B',
        featuredApps=[],
        apps=apps,
        news=[])
    cmap = {'签名工具': 'sign', '系统调试': 'debug', '影音下载': 'media',
            '浏览电视': 'tv', '摄影工具': 'photo'}
    for a in apps:
        a['iconURL'] = f"{RAW}/App_icons/cat_{cmap.get(a.get('category'), 'sign')}.png"

    out = os.environ.get('OUT_PATH', os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'apps', 'source.json'))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w', encoding='utf-8') as f:
        json.dump(source, f, ensure_ascii=False, indent=2)
    print(f"\n共 {len(apps)} 个应用，"
          f"{sum(1 for a in apps if a['versions'])} 个有可下载版本")


if __name__ == '__main__':
    main()
