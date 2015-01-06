from __future__ import absolute_import, print_function, division
# N.B., do not import unicode_literals in tests


import zipfile
from petl.compat import PY2


from petl.testutils import ieq, eq_
from petl.io.csv import fromcsv, tocsv, appendcsv, fromtsv, totsv
from petl.io.sources import StringSource, PopenSource, ZipSource


def test_stringsource():

    table1 = (('foo', 'bar'),
              ('a', '1'),
              ('b', '2'),
              ('c', '2'))

    # test writing to a string buffer
    ss = StringSource()
    tocsv(table1, ss)
    expect = "foo,bar\r\na,1\r\nb,2\r\nc,2\r\n"
    if not PY2:
        expect = expect.encode('ascii')
    actual = ss.getvalue()
    eq_(expect, actual)

    # test reading from a string buffer
    table2 = fromcsv(StringSource(actual))
    ieq(table1, table2)
    ieq(table1, table2)

    # test appending
    appendcsv(table1, ss)
    actual = ss.getvalue()
    expect = "foo,bar\r\na,1\r\nb,2\r\nc,2\r\na,1\r\nb,2\r\nc,2\r\n"
    if not PY2:
        expect = expect.encode('ascii')
    eq_(expect, actual)


def test_popensource():

    expect = (('foo', 'bar'),
              ('a', '1'))
    delimiter = ' '
    actual = fromcsv(PopenSource(r'echo -e foo bar\\na 1',
                                 shell=True,
                                 executable='/bin/bash'),
                     delimiter=delimiter)
    ieq(expect, actual)


def test_zipsource():

    # setup
    table = [('foo', 'bar'), ('a', '1'), ('b', '2')]
    totsv(table, 'tmp/issue_241.tsv')
    z = zipfile.ZipFile('tmp/issue_241.zip', mode='w')
    z.write('tmp/issue_241.tsv', 'data.tsv')
    z.close()

    # test
    actual = fromtsv(ZipSource('tmp/issue_241.zip', 'data.tsv'))
    ieq(table, actual)