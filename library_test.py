import unittest
import library

NUM_CORPUS = '''
On the 5th of May every year, Mexicans celebrate Cinco de Mayo. This tradition
began in 1845 (the twenty-second anniversary of the Mexican Revolution), and
is the 1st example of a national independence holiday becoming popular in the
Western Hemisphere. (The Fourth of July didn't see regular celebration in the
US until 15-20 years later.) It is celebrated by 77.9% of the population--
trending toward 80.                                                                
'''

class TestCase(unittest.TestCase):

    # Helper function
    def assert_extract(self, text, extractors, *expected):
        actual = [x[1].group(0) for x in library.scan(text, extractors)]
        self.assertEquals(str(actual), str([x for x in expected]))

    # First unit test; prove that if we scan NUM_CORPUS looking for mixed_ordinals,
    # we find "5th" and "1st".
    def test_mixed_ordinals(self):
        self.assert_extract(NUM_CORPUS, library.mixed_ordinals, '5th', '1st')

    # Second unit test; prove that if we look for integers, we find four of them.
    def test_integers(self):
        self.assert_extract(NUM_CORPUS, library.integers, '1845', '15', '20', '80')

    # Third unit test; prove that if we look for integers where there are none, we get no results.
    def test_no_integers(self):
        self.assert_extract("no integers", library.integers)

    def test_dates(self):
        self.assert_extract('I was born on 2015-12-31.', library.dates_iso8601, '2015-12-31')

    def test_dates_no_integers(self):
        self.assert_extract("I was born on 2015-12-31", library.dates_iso8601)

    def test_dates_fmt2(self):
        self.assert_extract('I was born on 25 Jan 2017.', library.dates_fmt2, '25 Jan 2017')
    
    # Checks for the iso date format with full Date 2018-06-21 15:54:14.87Z
    def test_dates_1(self):
        self.assert_extract(' 2018-06-21 15:54:14.876 ', library.dates_newiso8601, '2018-06-21 15:54:14.876')

    # Checks only for the date
    def test_dates_2(self):
        self.assert_extract(' 2018-06-21 ', library.dates_newiso8601, '2018-06-21')

    # Checks with hours and min
    def test_dates_3(self):
        self.assert_extract(' 2018-06-21 15:54', library.dates_newiso8601, '2018-06-21 15:54')

    # Checks with hours and min with seconds
    def test_dates_4(self):
        self.assert_extract(' 2018-06-21 15:54:00 ', library.dates_newiso8601, '2018-06-21 15:54:00')
    
    # Checks with hours and min with seconds with milliseconds
    def test_dates_5(self):
        self.assert_extract(' 2018-06-21 15:54:00.123 ', library.dates_newiso8601, '2018-06-21 15:54:00.123')

    # Checks with hours and min with seconds with milliseconds and timezone(Z)
    def test_dates_6(self):
        self.assert_extract(' 2018-06-21 15:54:00.123Z ', library.dates_newiso8601, '2018-06-21 15:54:00.123Z')
    
    # Checks with hours and min with seconds with milliseconds and timezone offset -0800
    def test_dates_7(self):
        self.assert_extract(' 2018-06-21 15:54:00.123-0800 ', library.dates_newiso8601, '2018-06-21 15:54:00.123-0800')

    # Checks with hours and min with seconds with milliseconds and timezone offset -0800
    def test_dates_8(self):
        self.assert_extract(' 2018-06-21 15:54:00.123-0800 ', library.dates_newiso8601, '2018-06-21 15:54:00.123-0800')

    # Checks for date format and , after the month
    def test_dates_fmt3(self):
        self.assert_extract(' 21 Jun, 2018 ', library.dates_fmt3, '21 Jun, 2018')

    # Checks for date format - regular
    def test_dates_fmt31(self):
        self.assert_extract(' 21 Jun 2018 ', library.dates_fmt3, '21 Jun 2018')

    # Support comma seperated grouping
    def test_numbers(self):
        self.assert_extract(' 123,456,789 ', library.comma_seperator, '123,456,789')

if __name__ == '__main__':
    unittest.main()
