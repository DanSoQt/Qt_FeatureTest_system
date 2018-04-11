import html
import datetime
import indexwriter
# dict repo -> list(tuple(feature, text))

_repos = {}

_errors_by_repo = {}

_warnings_by_repo = {}


_html_start = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
  <title>Feature build test {}</title>
  <meta charset="UTF-8">
  <style type="text/css">
  address {{
    margin-top: 1em;
    padding-top: 1em;
    border-top: thin dotted }}
  </style>
</head>


<body>
'''


_html_end = '''
<address> Copyright 2018 The Qt Company</address>
</body>
</html>
'''

_top_text ='''<h1>Qt feature build test results for {datestring}</h1>
<table>
  <tr>
    <td style="text-align:right"><strong>{errcount}</strong></td>
    <td>builds with errors.</td>
  </tr>
  <tr>
    <td style="text-align:right"><strong>{warncount}</strong></td>
    <td>builds with warnings ({totalwarncount} warnings in total).</td>
  </tr>
    <td style="text-align:right"><strong>{buildcount}</strong></td>
    <td>total builds.</td>
</table>
<p>
'''


_build_count = -1
_warn_count = 0
_total_warn_count = 0
_error_count = 0
_date_datetime = datetime.datetime.now()

def registerError(repo, feature, errmsg):
    global _error_count
    errlist = _errors_by_repo.setdefault(repo, [])
    errlist.append((feature, errmsg))
    _error_count += 1

def registerWarning(repo, feature, count, message):
    global _warn_count, _total_warn_count
    warnlist = _warnings_by_repo.setdefault(repo, [])
    warnlist.append((feature, count, message))
    _warn_count += 1
    _total_warn_count += count

def registerStats(buildcount):
    global _build_count
    _build_count = buildcount


def registerRepo(repo, sha1):
    _repos[repo] = sha1
    _errors_by_repo[repo] = []
    _warnings_by_repo[repo] = []


def setDateTime(datetime):
    global _date_datetime
    _date_datetime = datetime

def writeHtml(outfile):
    date_string = _date_datetime.strftime("%d %B %Y %H:%M")
    print(_html_start.format(date_string), file=outfile)
    print(_top_text.format(datestring=date_string, errcount=_error_count, warncount=_warn_count, totalwarncount = _total_warn_count, buildcount=_build_count if _build_count > 0 else '?'), file=outfile)
    for rs in sorted([(r, len(_errors_by_repo[r]), len(_warnings_by_repo[r])) for r in _repos], key=lambda r:(-r[1],-r[2], r[0])):
        repo = rs[0]
        errcount = rs[1]
        warncount = rs[2]
        errlist = _errors_by_repo.get(repo, [])
        errcount = len(errlist)
        warnlist = _warnings_by_repo.get(repo, [])
        warncount = len(warnlist)
        if errcount or warncount:
            print('<details><summary>Repository <strong>{}</strong> (<em>{}</em>):'.format(repo, _repos[repo]), file=outfile)
            if (errcount > 0):
                print('<strong>', file=outfile)
            print(errcount, ['errors', 'error'][errcount==1], file=outfile)
            if (errcount > 0):
                print('</strong>', file=outfile)
            print(warncount, ['warnings', 'warning'][warncount==1], file=outfile)
            print('</summary>', '<ul style="list-style: none;">',  file=outfile)
            for err in errlist:
                print('<li>', '<details>', '<summary>Build error <strong>{}</strong></summary>'.format(err[0]), '<pre>', file=outfile)
                print(html.escape(err[1]), file=outfile)
                print('</pre>', '</details>', file=outfile)
            for warn in warnlist:
                c = warn[1]
                f = warn[0]
                suffix = '' if c == 1 else 's'
                print('<li>', '<details>', '<summary>{} warning{} for <strong>{}</strong></summary>'.format(c, suffix, f), '<pre>', file=outfile)
                print(html.escape(warn[2]), file=outfile)
                print('</pre>', '</details>', file=outfile)
            print('</ul>', '</details>', file=outfile)
        else:
            print('<br>Repository <strong>{}</strong> (<em>{}</em>): no errors, no warnings'.format(repo, _repos[repo]), file=outfile)
    print(_html_end, file=outfile)
    indexwriter.addTestrun(file=outfile.name, date=_date_datetime.strftime('%Y-%m-%d %H:%M'), buildcount = _build_count,
                           errcount = _error_count, build_warncount = _warn_count, total_warncount = _total_warn_count)
    indexwriter.writeIndex()

#indexwriter: def addTestrun(file, date, buildcount, errcount, build_warncount, total_warncount):

