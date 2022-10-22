# -*- coding: utf-8 -*-
"""The date and time definitions.

Also see:
  https://en.wikipedia.org/wiki/Day
  https://en.wikipedia.org/wiki/Hour
  https://en.wikipedia.org/wiki/Minute
"""

DAYS_PER_MONTH = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

SECONDS_PER_DAY = 24 * 60 * 60

DECISECONDS_PER_SECOND = 10

MILLISECONDS_PER_SECOND = 1000

MICROSECONDS_PER_DAY = 86400000000
MICROSECONDS_PER_SECOND = 1000000
MICROSECONDS_PER_DECISECOND = 100000
MICROSECONDS_PER_MILLISECOND = 1000

NANOSECONDS_PER_MICROSECOND = 1000
NANOSECONDS_PER_SECOND = 1000000000

PRECISION_1_DAY = '1d'
PRECISION_1_HOUR = '1h'
PRECISION_1_NANOSECOND = '1ns'
PRECISION_10_NANOSECONDS = '10s'
PRECISION_100_NANOSECONDS = '100ns'
PRECISION_1_MICROSECOND = '1us'
PRECISION_10_MICROSECONDS = '10us'
PRECISION_100_MICROSECONDS = '100us'
PRECISION_1_MILLISECOND = '1ms'
PRECISION_10_MILLISECONDS = '10ms'
PRECISION_100_MILLISECONDS = '100ms'
PRECISION_1_MINUTE = '1min'
PRECISION_1_SECOND = '1s'
PRECISION_2_SECONDS = '2s'

PRECISION_VALUES = frozenset([
    PRECISION_1_DAY,
    PRECISION_1_HOUR,
    PRECISION_1_NANOSECOND,
    PRECISION_10_NANOSECONDS,
    PRECISION_100_NANOSECONDS,
    PRECISION_1_MICROSECOND,
    PRECISION_10_MICROSECONDS,
    PRECISION_100_MICROSECONDS,
    PRECISION_1_MILLISECOND,
    PRECISION_10_MILLISECONDS,
    PRECISION_100_MILLISECONDS,
    PRECISION_1_MINUTE,
    PRECISION_1_SECOND,
    PRECISION_2_SECONDS])

# Create a days per century lookup table.
DAYS_PER_CENTURY = {}
for year in range(-10000, 10000, 100):
  if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
    number_of_days = 36525
  else:
    number_of_days = 36524
  DAYS_PER_CENTURY[year] = number_of_days

# Create a days per year lookup table.
DAYS_PER_YEAR = {}
for year in range(-10000, 10000, 1):
  if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0:
    number_of_days = 366
  else:
    number_of_days = 365
  DAYS_PER_YEAR[year] = number_of_days

# Create a days per year in POSIX epoch lookup table.
DAYS_PER_YEAR_IN_POSIX_EPOCH = {}

number_of_days = 0
for year in range(1969, -10000, -1):
  number_of_days -= DAYS_PER_YEAR[year]
  DAYS_PER_YEAR_IN_POSIX_EPOCH[year] = number_of_days

number_of_days = 0
for year in range(1970, 10000, 1):
  DAYS_PER_YEAR_IN_POSIX_EPOCH[year] = number_of_days
  number_of_days += DAYS_PER_YEAR[year]
