# Date and time values
## Terminology

**Calendar**: a system of organising days.

**Epoch**: a reference point from which time is measured.

**Leap second**: a leap second is a one-second adjustment that is occasionally
applied to Coordinated Universal Time (UTC) in order to keep its time of day
close to the mean solar time.

### Also see

* [Wikipedia: Calendar](https://en.wikipedia.org/wiki/Calendar)
* [Wikipedia: Epoch](https://en.wikipedia.org/wiki/Epoch_(reference_date))
* [Wikipedia: Leap second](https://en.wikipedia.org/wiki/Leap_second)

## Accuracy and precision

* **accuracy** is used to describe the closeness of a measurement to the true
value;
* **precision** is the closeness of agreement among a set of results.

In NTFS data and time values are stored using a [FILETIME structure](https://docs.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-filetime).
The FILETIME structure stores a date and time value as a 64-bit integer that
represents the number of 100-nanosecond intervals since "January 1, 1601
00:00:00.0000000 UTC". This provides an upper bound of a 100-nanosecond
interval **data granularity**. For disambiguation we'll refer to this as
**datetime storage granularity**.

However this does not have to mean that the actual value stored within the
FILETIME structure has a 100-nanosecond interval data granularity. E.g. the
FILETIME MSDN article also mentions that on NTFS, the access time has a
**resolution** of 1 hour. For disambiguation the term resolution is comparable
with that of [Display resolution](https://en.wikipedia.org/wiki/Display_resolution)
or [Audio resolution](https://en.wikipedia.org/wiki/Audio_bit_depth), we'll
refer to this as **datetime value granularity**.

The FILETIME MSDN article also mentions that some values should be interpreted
not as date and time values e.g. 0xFFFFFFFF can be used to specify that a
file's previous access time should be preserved, or 0 to specify that the date
and time value is not set. For disambiguation we'll refer to this as **datetime
value semantics** (in other words meaning or representation).

### Digital forensics significance

A large part of digital forensic analysis is about the interpretation of
computer data. If date and time values are converted from a storage format to
another storage format or a string representation we are likely to change
granularity and semantics in the process. If the analyst is aware of this the
impact should be minimal, however if we wish to have automation assisted
analysis we'll have to preserve concepts of granularity and semantics and
represent them in a machine process-able manner. So that the automation can
distinguish between a FILETIME date and time value that is not set versus a
FILETIME date and time value that represents "January 1, 1601 00:00:00.0000000
UTC".

Another aspect relevant to digital forensic analysis is how to represent a
datetime value with a value granularity of 1 day (e.g. FAT access time) in a
timeline of microseconds, where the analyst is only interested in the events
that occurred within a specific hour on that day. Technically the access time
should be included in the resulting timeline since the access could have
occurred during that specific hour.

### References

* [Wikipedia: Accuracy and precision](https://en.wikipedia.org/wiki/Accuracy_and_precision)
* [Wikipedia: Computer forensics](https://en.wikipedia.org/wiki/Computer_forensics)
* [Wikipedia: Granularity - Data Granularity](https://en.wikipedia.org/wiki/Granularity#Data_granularity)
* [Wikipedia: Semantics](https://en.wikipedia.org/wiki/Semantics)
* [FILETIME structure](https://docs.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-filetime)
* [File Times](https://docs.microsoft.com/en-us/windows/win32/sysinfo/file-times)
* [Precision and accuracy of DateTime](https://docs.microsoft.com/en-us/archive/blogs/ericlippert/precision-and-accuracy-of-datetime), by Eric Lippert, April 8, 2010

## .NET DateTime
### Characteristics

Attribute | Description
--- | ---
Supported date range | 0001-01-01 00:00:00 through 9999-12-31 23:59:59
Storage granularity | 100 nanoseconds
Time zone | externally represented, typically UTC

### Format

Offset | Size | Description
0 | 4 or 8 | timestamp, little endian integer value containing the number of 100 nanosecond intervals since January 1, 0001 00:00:00.0000000

### Also see

* [Microsoft: DateTime struct](https://docs.microsoft.com/en-us/dotnet/api/system.datetime?view=net-6.0)
* [Microsoft: DateTime.Ticks](https://docs.microsoft.com/en-us/dotnet/api/system.datetime.ticks)

## APFS timestamp
### Characteristics

Attribute | Description
--- | ---
Supported date range | 1677-09-21 00:12:43.145224192 through 2262-04-11 23:47:16.854775807
Storage granularity | 1 nanosecond
Time zone | externally represented, typically UTC

### Format

Offset | Size | Description
--- | --- | ---
0 | 8 | timestamp, integer value containing the number of nanoseconds before (when negative) or after (when positive) 1970-01-01 00:00:00.000 (or POSIX or Unix epoch)

## Cocoa timestamp
### Characteristics

Attribute | Description
--- | ---
Supported date range | ...
Storage granularity | 1 second with higher granularity in fractional part
Time zone | externally represented, typically UTC

### Format

Offset | Size | Description
--- | --- | ---
0 | 4 or 8 | timestamp, floating point value containing the number of seconds since 2001-01-01 00:00:00

### Also see

* [Apple Developer: Dates](https://developer.apple.com/library/archive/documentation/Cocoa/Conceptual/DatesAndTimes/Articles/dtDates.html)
* [Apple Developer: NSDate](https://developer.apple.com/documentation/foundation/nsdate)

## Delphi TDateTime
### Characteristics

Attribute | Description
--- | ---
Supported date range | ... through 9999-12-31 23:59:59.999
Storage granularity | 1 day with higher granularity in fractional part
Time zone | externally represented, typically UTC

### Format

Offset | Size | Description
--- | --- | ---
0 | 4 | timestamp, floating point value containing the number of days since 1899-12-30 00:00:00

### Also see

* [Embarcadero: System.TDateTime](https://docwiki.embarcadero.com/Libraries/XE3/en/System.TDateTime)

## FAT date and time
### Characteristics

Attribute | Description
--- | ---
Supported date range | 1980-01-01 00:00:00 through 2107-12-31 23:59:58
Storage granularity | 2-second intervals
Time zone | externally represented, typically local time

Sometimes 2099-12-31 23:59:58 is defined as the upper bound of DOS date and
time. Also see: [Time formatting and storage bugs - Year 2100](https://en.wikipedia.org/wiki/Time_formatting_and_storage_bugs#Year_2100)

### Format

The FAT (or DOS) date is a 16-bit value that consists of:

Offset | Size | Description
--- | --- | ---
0.0 | 5 bits | day of month, where 1 is the first day of the month
0.5 | 4 bits | month, where January is represented by 1
1.1 | 7 bits | year, ranging from 1980 through

The FAT (or DOS) time is a 16-bit value that consists of:

Offset | Size | Description
--- | --- | ---
0.0 | 5 bits | number of 2-second intervals, ranging from 0 through 29
0.5 | 6 bits | minutes, ranging from 0 through 59
1.2 | 5 bits | hours, ranging from 0 through 23

### Also see

* [Wikipedia: File Allocation Table](https://en.wikipedia.org/wiki/File_Allocation_Table)
* [DosDateTimeToFileTime function](https://docs.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-dosdatetimetofiletime)

## FAT timestamp
### Characteristics

Attribute | Description
--- | ---
Supported date range | 1980-01-01 00:00:00.00 through 2107-12-31 23:59:58.99
Storage granularity | 10 milliseconds
Time zone | externally represented

### Format

Offset | Size | Description
--- | --- | ---
0 | 8 | timestamp, integer value containing the number of 10 milliseconds intervals after 1980-01-01 00:00:00.00 (or FAT date time epoch)

## FILETIME
### Characteristics

Attribute | Description
--- | ---
Supported date range | 1601-01-01 00:00:00.0000000 through ...
Storage granularity | 100-nanosecond intervals
Time zone | externally represented, typically UTC

The actual upper bound of the supported date range is unclear. Also see:
[Latest possible FILETIME](https://stackoverflow.com/questions/9999393/latest-possible-filetime)

### Format

The FILETIME structure is 8 bytes of size and consists of:

Offset | Size | Description
--- | --- | ---
0 | 4 | lower 32-bit of the 64-bit timestamp
4 | 4 | upper 32-bit of the 64-bit timestamp

The FILETIME should be treated as a structure when stored and passed to Windows
API functions. However it can be combined into a 64-bit integer, which will be
indicated as a FILETIME timestamp, containing the number of seconds since
1601-01-01 00:00:00.0000000.

An empty (or unset) FILETIME timestamp can be represented by 0, however the
meaning can differ depending on the context in which the timestamp is used.

Certain values of FILETIME such as { 0xffffffff, 0xffffffff } for the
SetFileTime Windows API function are overloaded with a special meaning.

### Also see

* [MSDN: FILETIME](https://docs.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-filetime)

## Golang time.Time timestamp

### Characteristics

Attribute | Description
--- | ---
Supported date range | 0001-01-01 00:00:00.0000000 through ...
Storage granularity | 1 nanosecond
Time zone | internally represented.

The granularity of the time zone value depends on the version of the timestamp.
Version 1 timestamps are stored in minutes and version 2 timestamps add a
seconds component.  *Note: Version 2 is currently not supported.*

### Format

Offset | Size | Description
--- | --- | ---
0 | 1 | version (known values are 1 or 2)
1 | 8 | seconds since January, 1, 1 stored as a 64-bit big-endian signed integer
9 | 4 | fraction of second, in nanoseconds stored as a 32-bit big-endian signed integer
13 | 2 | time zone offset in minutes as a 16-bit big-endian signed integer.
15 | 1 | time zone offset in seconds (only for version 2)

A value of -1 is a special value when the Time instance is initialised as UTC
(e.g. ```time.Date(1970, time.January, 1, 0, 0, 0, 0, time.UTC)```).

### Also see

* [Golang time.go](https://cs.opensource.google/go/go/+/master:src/time/time.go)

## HFS timestamp

Sometimes a distinction is made between HFS and HFS+ timestamps is that the
former is stored in local time and the latter in UTC. Note that this behavior
is highly depending on the context in which the timestamp is used.

### Characteristics

Attribute | Description
--- | ---
Supported date range | 1904-01-01 00:00:00 through 2040-02-06 06:28:15
Storage granularity | 1 second
Time zone | externally represented

### Format

Offset | Size | Description
--- | --- | ---
0 | 4 | timestamp, integer value containing the number of seconds since 1904-01-01 00:00:00

An empty (or unset) HFS timestamp can be represented by 0, however the meaning
can differ depending on the context in which the timestamp is used.

### Also see

* [Wikipedia: HFS Plus](https://en.wikipedia.org/wiki/HFS_Plus)
* [Technical Note TN1150 - HFS Plus Volume Format](http://dubeiko.com/development/FileSystems/HFSPLUS/tn1150.html#HFSPlusDates)

## Java timestamp
### Characteristics

Attribute | Description
--- | ---
Supported date range | ...
Storage granularity | 1 millisecond
Time zone | externally represented

### Format

Offset | Size | Description
--- | --- | ---
0 | 8 | timestamp, integer value containing the number of milliseconds before (when negative) or after (when positive) 1970-01-01 00:00:00.000 (or POSIX or Unix epoch)

### Also see

* [Class java.util.Date](https://docs.oracle.com/javase/8/docs/api/java/util/Date.html)

## OLE Automated date

The OLE Automated date is also known as Floatingtime or Application time.

### Characteristics

Attribute | Description
--- | ---
Supported date range | ...
Storage granularity | 1 day with fragment
Time zone | externally represented

### Format

Offset | Size | Description
--- | --- | ---
0 | 8 | timestamp, floating-point value containing the number of days before (when negative) or after (when positive) 1889-12-30. The fractional part represents the fraction of a day since midnight.

## POSIX timestamp

There multiple variants of the POSIX timestamp:

* the `time_t` has different sizes and signs on different platforms
* variants exist that store the timestamp in milliseconds (Java), microsecond and nanoseconds (APFS) precision instead of second precision

### Characteristics

Attribute | Description
--- | ---
Supported date range | 1901-12-13 20:45:52 through 2038-01-19 03:14:07 (32-bit)
Storage granularity | 1 second
Time zone | externally represented

### Format

Offset | Size | Description
--- | --- | ---
0 | 4 or 8 | timestamp, integer value containing the number of seconds before (when negative) or after (when positive) 1970-01-01 00:00:00 (or POSIX or Unix epoch)

An empty (or unset) POSIX timestamp can be represented by 0, however the
meaning can differ depending on the context in which the timestamp is used.

### Also see

* [Wikipedia: UNIX time](https://en.wikipedia.org/wiki/Unix_time)

## RFC2579 date-time
### Characteristics

Attribute | Description
--- | ---
Supported date range | 0-01-01 00:00:00.0 through 65536-12-31 23:59:59.9
Storage granularity | 1 decisecond (100 milliseconds)
Time zone | internally represented as [+-]hh:mm from UTC

### Format

The RFC2579 date-time structure is 11 bytes of size and consists of:

Offset | Size | Description
--- | --- | ---
0 | 2 | year, ranging from 0 through 65536
2 | 1 | month, where January is represented by 1
3 | 1 | day of month, where 1 is the first day of the month
4 | 1 | hours, ranging from 0 through 23
5 | 1 | minutes, ranging from 0 through 59
6 | 1 | seconds, ranging from 0 through 59
7 | 1 | deciseconds, ranging from 0 through 9
8 | 1 | direction from UTC, "+" or "-"
9 | 1 | hours from UTC, ranging from 0 through 13
10 | 1 | minutes from UTC, ranging from 0 through 59

### Also see

* [RFC2579](https://datatracker.ietf.org/doc/html/rfc2579)

## SYSTEMTIME
### Characteristics

Attribute | Description
--- | ---
Supported date range | 1601-01-01 00:00:00.000 through 30827-12-31 23:59:59.999
Storage granularity | 1 millisecond
Time zone | externally represented

### Format

The SYSTEMTIME structure is 16 bytes of size and consists of:

Offset | Size | Description
--- | --- | ---
0 | 2 | year, ranging from 1601 through 30827
2 | 2 | month, where January is represented by 1
4 | 2 | day of week, staring with Sunday represented by 0
6 | 2 | day of month, where 1 is the first day of the month
8 | 2 | hours, ranging from 0 through 23
10 | 2 | minutes, ranging from 0 through 59
12 | 2 | seconds, ranging from 0 through 59
14 | 2 | milliseconds, ranging from 0 through 999

An empty (or unset) SYSTEMTIME can be represented by 16x 0-byte values.

### Also see

* [MSDN: SYSTEMTIME](https://docs.microsoft.com/en-us/windows/win32/api/minwinbase/ns-minwinbase-systemtime)

## Time element strings

### ISO 8601 / RFC 3339

Example `2020-05-31T00:00:47.044800+00:00`

### RFC 822

Example `Tue, 15 Nov 94 08:12:31 GMT`

### RFC 1123

Example `Tue, 15 Nov 1994 08:12:31 GMT`

### RFC 2822

### Also see

* [RFC 822 - Date and time specification](https://datatracker.ietf.org/doc/html/rfc822#section-5)
* [RFC 1123 - RFC-822 date and time specification](https://datatracker.ietf.org/doc/html/rfc1123#section-5)
* [RFC 2822 - Date and time specification](https://datatracker.ietf.org/doc/html/rfc2822#section-3.3)
* [RFC 3339 - Internet date/time format](https://datatracker.ietf.org/doc/html/rfc3339#section-5.6)

## UUID version 1 time
### Characteristics

Attribute | Description
--- | ---
Supported date range | 1582-10-15 00:00:00.0000000 through ...
Storage granularity | 100-nanosecond intervals
Time zone | externally represented, typically UTC

### Format

Offset | Size | Description
--- | --- | ---
0 | 60-bits | integer value, containing the number of 100-nanosecond intervals since 1582-10-15 00:00:00
7.4 | 4-bits | version
8.0 | 16-bits | UUID version (variant) and clock sequence
10.0 | 48-bits | node identifier (typically a MAC address in UUID version 1)

### Also see

* [Wikipedia: Universally unique identifier](https://en.wikipedia.org/wiki/Universally_unique_identifier)

## WebKit timestamp
### Characteristics

Attribute | Description
--- | ---
Supported date range | ...
Storage granularity | 1 microsecond
Time zone | externally represented, typically UTC

### Format

Offset | Size | Description
--- | --- | ---
0 | 8 | timestamp, signed integer value containing the number of microseconds before (when negative) or after (when positive) 1601-01-01 00:00:00.000000

### Also see

* [Chromium source: time.h](https://chromium.googlesource.com/chromium/src/base/+/refs/heads/main/time/time.h#5)
