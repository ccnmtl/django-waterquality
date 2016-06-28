from django.core.urlresolvers import reverse
from django.test import TestCase
from django.test.client import Client
from waterquality.models import Site, Location, Series, Row
from datetime import datetime


class TestBoringPages(TestCase):
    def setUp(self):
        self.c = Client()

    def test_index(self):
        r = self.c.get(reverse("waterchemistry-index"))
        self.assertEqual(r.status_code, 200)

    def test_teaching(self):
        r = self.c.get(reverse("waterchemistry-teaching"))
        self.assertEqual(r.status_code, 200)


def series_factory():
    site = Site.objects.create(name="test")
    l = Location.objects.create(name="test", site=site)
    return Series.objects.create(name="test", location=l)


class TestSeriesViews(TestCase):
    def setUp(self):
        self.c = Client()
        self.s = series_factory()
        self.r1 = Row.objects.create(
            series=self.s, timestamp=datetime.now(), value=1.0)
        Row.objects.create(series=self.s, timestamp=datetime.now(), value=2.0)
        Row.objects.create(series=self.s, timestamp=datetime.now(), value=3.0)
        self.r2 = Row.objects.create(
            series=self.s, timestamp=datetime.now(), value=4.0)

    def test_browse(self):
        r = self.c.get(reverse("waterchemistry-browse"))
        self.assertEqual(r.status_code, 200)

    def test_series_all(self):
        r = self.c.get(reverse("waterchemistry-series-all", args=[self.s.id]))
        self.assertEqual(r.status_code, 200)

    def test_series(self):
        r = self.c.get(reverse("waterchemistry-series", args=[self.s.id]))
        self.assertEqual(r.status_code, 200)

    def test_series_with_endpoints(self):
        start = self.r1.timestamp
        end = self.r2.timestamp
        r = self.c.get(reverse("waterchemistry-series", args=[self.s.id]),
                       dict(start=start, end=end))
        self.assertEqual(r.status_code, 200)

    def test_verify(self):
        r = self.c.get(reverse("waterchemistry-series-verify",
                               args=[self.s.id]))
        self.assertEqual(r.status_code, 200)


class TestGraph(TestCase):
    def setUp(self):
        self.c = Client()
        self.s = series_factory()
        self.r1 = Row.objects.create(
            series=self.s, timestamp=datetime.now(), value=1.0)
        Row.objects.create(series=self.s, timestamp=datetime.now(), value=2.0)
        Row.objects.create(series=self.s, timestamp=datetime.now(), value=3.0)
        self.r2 = Row.objects.create(
            series=self.s, timestamp=datetime.now(), value=4.0)

        self.s2 = series_factory()
        Row.objects.create(series=self.s2, timestamp=datetime.now(), value=7.0)
        Row.objects.create(series=self.s2, timestamp=datetime.now(), value=8.0)
        Row.objects.create(series=self.s2, timestamp=datetime.now(), value=0.0)
        Row.objects.create(
            series=self.s2, timestamp=datetime.now(), value=10.0)

    def test_simple(self):
        r = self.c.get(reverse("waterchemistry-graphing-tool"))
        self.assertEqual(r.status_code, 200)

    def test_with_endpoints(self):
        start = "2000-01-01"
        end = "2100-01-01"
        r = self.c.get(reverse("waterchemistry-graphing-tool"),
                       dict(start=start, end=end))
        self.assertEqual(r.status_code, 200)

    def test_invalid_endpoints(self):
        r = self.c.get(reverse("waterchemistry-graphing-tool"),
                       dict(start="bad start", end="bad end"))
        self.assertEqual(r.status_code, 200)
        r = self.c.get(reverse("waterchemistry-graphing-tool"),
                       dict(start="2000-01-01", end="bad end"))
        self.assertEqual(r.status_code, 200)

    def test_time_series(self):
        r = self.c.get(
            reverse("waterchemistry-graphing-tool"),
            dict(
                type='time-series',
                series=self.s.id,
                line_value_1=1,
                line_label_1="a label"))
        self.assertEqual(r.status_code, 200)

    def test_scatter_plot(self):
        r = self.c.get(
            reverse("waterchemistry-graphing-tool"),
            dict(
                type='scatter-plot',
                independent=self.s.id,
                dependent=self.s2.id,
                end="2100-01-01",
            ))
        self.assertEqual(r.status_code, 200)

    def test_scatter_plot_skip_zeroes(self):
        r = self.c.get(
            reverse("waterchemistry-graphing-tool"),
            dict(
                type='scatter-plot',
                skip_zeroes="1",
                independent=self.s.id,
                dependent=self.s2.id,
                end="2100-01-01",
            ))
        self.assertEqual(r.status_code, 200)

    def test_box_plot(self):
        r = self.c.get(
            reverse("waterchemistry-graphing-tool"),
            dict(
                type='box-plot',
                series=self.s.id,
                end="2100-01-01",
            ))
        self.assertEqual(r.status_code, 200)
