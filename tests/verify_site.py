from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from urllib.parse import urlsplit
import unittest


SITE_ROOT = Path(__file__).resolve().parents[1]
LEGAL_PAGES = (
    "privacy.html",
    "support.html",
    "terms.html",
    "data-deletion.html",
    "membership.html",
    "automatic-renewal.html",
    "open-source.html",
)


class PageParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.hrefs: List[str] = []
        self.anchors: List[Dict[str, str]] = []
        self._anchor: Optional[Dict[str, str]] = None

    def handle_starttag(
        self, tag: str, attrs: List[Tuple[str, Optional[str]]]
    ) -> None:
        attributes = {key: value or "" for key, value in attrs}
        if tag == "a":
            href = attributes.get("href", "")
            self.hrefs.append(href)
            self._anchor = {
                "href": href,
                "class": attributes.get("class", ""),
                "text": "",
            }

    def handle_data(self, data: str) -> None:
        if self._anchor is not None:
            self._anchor["text"] += data

    def handle_endtag(self, tag: str) -> None:
        if tag == "a" and self._anchor is not None:
            self._anchor["text"] = " ".join(self._anchor["text"].split())
            self.anchors.append(self._anchor)
            self._anchor = None


def parse_page(path: Path) -> Tuple[str, PageParser]:
    source = path.read_text(encoding="utf-8")
    parser = PageParser()
    parser.feed(source)
    return source, parser


class SiteContractTests(unittest.TestCase):
    def test_required_assets_exist(self) -> None:
        for relative_path in (
            "site.css",
            "assets/focusabit-logo.svg",
            "assets/apple-touch-icon.png",
        ):
            with self.subTest(relative_path=relative_path):
                self.assertTrue((SITE_ROOT / relative_path).is_file())

    def test_homepage_contract(self) -> None:
        source, parser = parse_page(SITE_ROOT / "index.html")

        required_content = (
            "开启一次专注，如此简单。",
            "轻松开始",
            "安静专注",
            "片刻冥想",
            "看见节律",
            'id="features"',
            'id="product"',
            'href="site.css?v=20260826"',
            'src="assets/focusabit-logo.svg"',
            "Focusabit for iPhone · 敬请期待",
        )
        for content in required_content:
            with self.subTest(content=content):
                self.assertIn(content, source)

        homepage_hrefs = set(parser.hrefs)
        for page in (*LEGAL_PAGES, "legal.html"):
            with self.subTest(footer_link=page):
                self.assertIn(page, homepage_hrefs)

        clickable_launch_labels = {
            anchor["text"]
            for anchor in parser.anchors
            if "App Store" in anchor["text"] or "敬请期待" in anchor["text"]
        }
        self.assertEqual(set(), clickable_launch_labels)

    def test_homepage_links_to_official_icp_record(self) -> None:
        _, parser = parse_page(SITE_ROOT / "index.html")
        icp_links = [
            anchor
            for anchor in parser.anchors
            if anchor["text"] == "蜀ICP备2026047538号"
        ]

        self.assertEqual(1, len(icp_links))
        self.assertEqual("https://beian.miit.gov.cn/", icp_links[0]["href"])

    def test_legal_overview_links_to_every_legal_page(self) -> None:
        overview = SITE_ROOT / "legal.html"
        self.assertTrue(overview.is_file())
        _, parser = parse_page(overview)
        for page in LEGAL_PAGES:
            with self.subTest(page=page):
                self.assertIn(page, parser.hrefs)

    def test_legal_page_shells_link_home_and_overview(self) -> None:
        for page in LEGAL_PAGES:
            with self.subTest(page=page):
                _, parser = parse_page(SITE_ROOT / page)
                brands = [
                    anchor
                    for anchor in parser.anchors
                    if "brand" in anchor["class"].split()
                ]
                self.assertEqual(1, len(brands))
                self.assertEqual("index.html", brands[0]["href"])
                self.assertIn("legal.html", parser.hrefs)

    def test_existing_legal_body_markers_remain(self) -> None:
        markers = {
            "privacy.html": "当前版本不请求通讯录、精确位置、麦克风或健康数据权限。",
            "support.html": "请勿通过普通邮件发送密码、验证码、完整交易凭证或完整支付信息。",
            "terms.html": "微专注是自我管理工具，不构成医疗、心理、健康或其他专业建议",
            "data-deletion.html": "删除账号与取消会员订阅是两个独立操作。",
            "membership.html": "基础计时能力不因未开通会员而关闭。",
            "automatic-renewal.html": "终身会员为一次性购买，不自动续费。",
            "open-source.html": "当前版本未引入第三方 UI 框架。",
        }
        for page, marker in markers.items():
            with self.subTest(page=page):
                source = (SITE_ROOT / page).read_text(encoding="utf-8")
                self.assertIn(marker, source)

    def test_all_local_links_resolve(self) -> None:
        for html_path in SITE_ROOT.glob("*.html"):
            _, parser = parse_page(html_path)
            for href in parser.hrefs:
                parts = urlsplit(href)
                if parts.scheme or href.startswith(("#", "mailto:")) or not parts.path:
                    continue
                target = (html_path.parent / parts.path).resolve()
                with self.subTest(page=html_path.name, href=href):
                    self.assertTrue(target.exists())

    def test_no_placeholder_or_empty_links(self) -> None:
        forbidden = ('href="#"', ".example", "【请替换")
        for html_path in SITE_ROOT.glob("*.html"):
            source = html_path.read_text(encoding="utf-8")
            for value in forbidden:
                with self.subTest(page=html_path.name, value=value):
                    self.assertNotIn(value, source)


if __name__ == "__main__":
    unittest.main()
