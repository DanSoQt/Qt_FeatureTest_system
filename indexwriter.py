import yaml
import os

_html_header = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN">
<html>
<head>
  <title>Qt feature test builds</title>
  <meta charset="UTF-8">
  <style type="text/css">
    address {
    margin-top: 1em;
    padding-top: 1em;
    border-top: thin dotted }
    table td{

 padding:0px 10px 0px 10px; /* top right bottom left */

 }
  </style>
</head>


<body>

<h1>Qt feature test builds</h1>

<table>
  <tr>
    <th> Test run </th>
    <th> Errors </th>
    <th> Warnings </th>
  </tr>'''

_html_footer = '''
</table>
<address> Copyright 2018 The Qt Company</address>
</body>
</html>
'''


_table_row = '''
  <tr>
    <td><a href="{url}">{date}</a></td>
    <td><strong>{errcount} build errors</strong> in {buildcount} builds</td>
    <td>{total_warncount} warnings from {build_warncount} builds</td>
  </tr>'''

__example = '''
  <tr>
    <td><a href="featuretest_2017-04-18T17:19.html">2017-04-18 17:19</a></td>
    <td><strong>32 build errors</strong> in 5738 builds</td>
    <td>138 warnings from 35 builds</td>
  </tr>
  <tr>
    <td><a href="featuretest_2017-04-20T16:00.html">2017-04-20 16:00</a></td>
    <td><strong>31 build errors</strong> in 5836 builds</td>
    <td>130 warnings from 29 builds</td>
  </tr>
  <tr>
    <td><a href="featuretest_2017-04-23T00:00.html">2017-04-23 00:00</a></td>
    <td><strong>29 build errors</strong> in 5826 builds</td>
    <td>131 warnings from 32 builds</td>
  </tr>
  <tr>
    <td><a href="featuretest_2017-04-25T16:00.html">2017-04-25 16:00</a></td>
    <td><strong>27 build errors</strong> in 5826 builds</td>
    <td>125 warnings from 28 builds</td>
  </tr>
'''


_outdir = '.'

#with open('yamltest.txt', 'r') as yf:
#    print(yaml.dump(yaml.load(yf.read()),  default_flow_style=False))
def writeIndex():
    with open(os.path.join(_outdir,'index.html'), 'w') as htmlFile:
        print(_html_header, file=htmlFile)
        with open(os.path.join(_outdir,'buildstats.yaml'), 'r') as yf:
            run_list=yaml.load(yf.read())
        #print(run_list)
        for run in reversed(run_list):
            print(_table_row.format(url=os.path.basename(run['file']), date=run['date'], errcount=run['errcount'],
                                    build_warncount=run['build_warncount'], total_warncount=run['total_warncount'],
                                    buildcount=run['buildcount']), file=htmlFile)
        print(_html_footer, file=htmlFile)


def addTestrun(file, date, buildcount, errcount, build_warncount, total_warncount):
    global _outdir
    _outdir = os.path.dirname(file)
    runlist = [{'file':file, 'date':date, 'buildcount':buildcount, 'errcount':errcount,
                'build_warncount':build_warncount, 'total_warncount':total_warncount}]
    with open(os.path.join(_outdir,'buildstats.yaml'), 'a') as yf2:
        print(yaml.dump(runlist,  default_flow_style=False), file=yf2)
