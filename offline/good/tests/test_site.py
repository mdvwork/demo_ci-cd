from html.parser import HTMLParser
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"


class Page(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.titles = []
        self.headings = []
        self.stylesheets = []
        self.active_tag = None
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("title", "h1"):
            self.active_tag = tag
        if tag == "link" and attrs.get("rel") == "stylesheet":
            self.stylesheets.append(attrs.get("href", ""))

    def handle_endtag(self, tag):
        if tag == self.active_tag:
            self.active_tag = None

    def handle_data(self, data):
        if self.active_tag == "title":
            self.titles.append(data.strip())
        elif self.active_tag == "h1":
            self.headings.append(data.strip())


class SiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.text = (SITE / "index.html").read_text(encoding="utf-8")
        cls.page = Page(cls.text)

    def test_title(self):
        self.assertEqual("".join(self.page.titles), "Расписание DevOps",
                         "Заголовок вкладки должен быть Расписание DevOps")

    def test_heading(self):
        self.assertEqual(self.page.headings, ["Расписание DevOps"],
                         "Нужен один заголовок h1 Расписание DevOps")

    def test_stylesheet_exists(self):
        self.assertTrue(self.page.stylesheets, "Не подключен файл стилей")
        for href in self.page.stylesheets:
            with self.subTest(href=href):
                self.assertTrue(bool(href) and (SITE / href).is_file(),
                                f"Missing stylesheet: {href}")

    def test_lesson_topic(self):
        self.assertIn("Тема занятия: CI/CD", self.text,
                      "На странице должна быть указана тема занятия")


if __name__ == "__main__":
    unittest.main()
