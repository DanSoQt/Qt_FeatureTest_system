import html


# dict repo -> list(tuple(feature, text))

_repos = set()

_errors_by_repo = {}

_warnings_by_repo = {}


_html_start = '''<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
  <title>Qt feature test result</title>
  <meta charset="UTF-8">
  <style type="text/css">
  address {
    margin-top: 1em;
    padding-top: 1em;
    border-top: thin dotted }
  </style>
</head>


<body>
'''


_html_end = '''
<address> Copyright 2017 The Qt Company</address>
</body>
</html>
'''

def registerError(repo, feature, errmsg):
    _repos.add(repo)
    errlist = _errors_by_repo.setdefault(repo, [])
    errlist.append((feature, errmsg))

def registerWarning(repo, feature, count, message):
    _repos.add(repo)
    warnlist = _warnings_by_repo.setdefault(repo, [])
    warnlist.append((feature, count, message))


def writeHtml(outfile):
    print(_html_start, file=outfile)
    print('<h1>Qt feature test results</h1>', file=outfile)
    for repo in _repos:
        errlist = _errors_by_repo.get(repo, [])
        errcount = len(errlist)
        warnlist = _warnings_by_repo.get(repo, [])
        warncount = len(warnlist)
        print('<details><summary>Repository {}:'.format(repo), file=outfile)
        print(errcount, ['errors', 'error'][errcount==1], warncount, ['warnings', 'warning'][warncount==1], file=outfile)
        print('</summary>', '<ul style="list-style: none;">',  file=outfile)
        for err in errlist:
            print('<li>', '<details>', '<summary>Build error <strong>{}</strong></summary>'.format(err[0]), '<pre>', file=outfile)
            print(html.escape(err[1]), file=outfile)
            print('</pre>', '</details>', file=outfile)
        for warn in warnlist:
            print('<li>', '<details>', '<summary>{} warnings for <strong>{}</strong></summary>'.format(warn[1], warn[0]), '<pre>', file=outfile)
            print(html.escape(warn[2]), file=outfile)
            print('</pre>', '</details>', file=outfile)
        print('</ul>', '</details>', file=outfile)
    print(_html_end, file=outfile)
