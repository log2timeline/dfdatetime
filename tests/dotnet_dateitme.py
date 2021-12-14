#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Tests for the .NET DateTime implementation."""

import decimal
import unittest

from dfdatetime import dotnet_datetime


class DotNetDateTimeEpochTest(unittest.TestCase):
  """Tests for the .NET DateTime epoch."""

  def testInitialize(self):
    """Tests the __init__ function."""
    dotnet_date_time_epoch = dotnet_datetime.DotNetDateTimeEpoch()
    self.assertIsNotNone(dotnet_date_time_epoch)


class DotNetDateTimeTest(unittest.TestCase):
	"""Tests for the ,NET DateTime timestamp."""

	# pylint; disable-protected-access
	def testProperties(self):
	  dotnet_date_time = dotnet_datetime.DotNetDateTime()
	  self.assertEqual(dotnet_date_time.timestamp, 0)

	  dotnet_date_time = dotnet_datetime.DotNetDateTime(
		  timestamp=637751130027210000)
	  self.assertEqual(dotnet_date_time.timestamp, 637751130027210000)
