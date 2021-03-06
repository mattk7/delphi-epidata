"""Integration tests for the `fluview` endpoint."""

# standard library
import unittest

# third party
import mysql.connector

# first party
from delphi.epidata.client.delphi_epidata import Epidata


class FluviewTests(unittest.TestCase):
  """Tests the `fluview` endpoint."""

  @classmethod
  def setUpClass(cls):
    """Perform one-time setup."""

    # use the local instance of the Epidata API
    Epidata.BASE_URL = 'http://delphi_web_epidata/epidata/api.php'

  def setUp(self):
    """Perform per-test setup."""

    # connect to the `epidata` database and clear the `fluview` table
    cnx = mysql.connector.connect(
        user='user',
        password='pass',
        host='delphi_database_epidata',
        database='epidata')
    cur = cnx.cursor()
    cur.execute('truncate table fluview')
    cnx.commit()
    cur.close()

    # make connection and cursor available to test cases
    self.cnx = cnx
    self.cur = cnx.cursor()

  def tearDown(self):
    """Perform per-test teardown."""
    self.cur.close()
    self.cnx.close()

  def test_round_trip(self):
    """Make a simple round-trip with some sample data."""

    # insert dummy data
    self.cur.execute('''
      insert into fluview values
        (0, "2020-04-07", 202021, 202020, "nat", 1, 2, 3, 4, 3.14159, 1.41421,
        10, 11, 12, 13, 14, 15)
    ''')
    self.cnx.commit()

    # make the request
    response = Epidata.fluview('nat', 202020)

    # assert that the right data came back
    self.assertEqual(response, {
      'result': 1,
      'epidata': [{
         'release_date': '2020-04-07',
         'region': 'nat',
         'issue': 202021,
         'epiweek': 202020,
         'lag': 1,
         'num_ili': 2,
         'num_patients': 3,
         'num_providers': 4,
         'num_age_0': 10,
         'num_age_1': 11,
         'num_age_2': 12,
         'num_age_3': 13,
         'num_age_4': 14,
         'num_age_5': 15,
         'wili': 3.14159,
         'ili': 1.41421,
       }],
      'message': 'success',
    })
