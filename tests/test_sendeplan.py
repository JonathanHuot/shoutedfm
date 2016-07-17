import unittest
import sendeplan


def read_soup(html_path):
    from codecs import open
    from os import path
    from bs4 import BeautifulSoup

    here = path.abspath(path.dirname(__file__))
    with open(path.join(here, html_path)) as f:
        return BeautifulSoup(f.read(), 'html.parser')

    
class test_sendeplan(unittest.TestCase):
    def test_events(self):
        event = sendeplan.event_from_cell(read_soup('sendeplan_event_cell.html'))
        self.assertEqual(event["start_time"], "14:00")
        self.assertEqual(event["end_time"], "16:00")
        self.assertNotEqual(event["event_title"].find("Miami Sound Sets"), -1)
        self.assertNotEqual(event["event_title"].find("aleXsir"), -1)

    def test_empty_event(self):
        event = sendeplan.event_from_cell(read_soup('sendeplan_empty_cell.html'))
        self.assertFalse(event)

    def test_event(self):
        weekday = sendeplan.weekday_from_eventpage(read_soup('sendeplan_event.html'))
        self.assertEqual(weekday, 1)

    def test_events(self):
        events = sendeplan.events_from_sendeplan(read_soup('sendeplan.html'))
        self.assertEqual(len(events), 13)

    def test_main(self):
        return
        with patch('requests.get') as mock:
            import pdb; pdb.set_trace();
            #mock.side_effect = [{"status_code": 200..setattr]
            events = sendeplan.main()
            self.assertEqual(len(events), 13)
            for event in events:
                self.assertIn("start_time", event)
                self.assertIn("end_time", event)
                self.assertIn("event_title", event)
                self.assertIn("weekday", event)
                self.assertNotEqual(event["weekday"], -1)
