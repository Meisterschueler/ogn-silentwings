# flake8: noqa
from app import app
from flask import request,jsonify, send_file

from io import StringIO

import logging
from logging.handlers import RotatingFileHandler



#########################
# Following Sections provides the Silent Wings Viewer interface
#########################

# getcontestinfo.php
@app.route("/getcontestinfo.php")
@app.route("/getcontestinfo")
def getcontestinfo():
    username = request.args.get('username', type = str)
    cpassword = request.args.get('cpassword', type = str)
    contestname = request.args.get('contestname', type = str)
    date = request.args.get('date', type = str)
    app.logger.error('getcontestinfo.php was called: usernmae = %s contestname = %s date = %s',username,contestname,date)

    if 'username' in request.args:
        app.logger.error('Username was provided in URL')
        pass # do something


    if 'date' in request.args:
        app.logger.error('Date was provided in URL; Should return CUC file')
        # return CUC file
        # Call function, which creates CUC file here
        # pass 
        return send_file(gencuc(), attachment_filename='CUC_temp.cuc')


    return "{date}20050903{/date}{task}1{/task}{validday}0{/validday}{date}20050904{/date}{task}1{/task}{validday}0{/validday}\
    {date}20050907{/date}{task}1{/task}{validday}0{/validday}{date}20050909{/date}{task}1{/task}{validday}1{/validday}\
    {date}20050910{/date}{task}1{/task}{validday}1{/validday}{date}20050911{/date}{task}1{/task}{validday}1{/validday}"


  # Parameters
  # username=<user name>
  # cpassword=<encrypted password>
  # contestname=<contest name>
  # date=<YYYYMMDD>

  # Example get to server:
  # GET /getcontestinfo.php?username=ogn&cpassword=ecbad38d0b5a3cf6482e661028b2c60c&contestname=FAIGP2005 HTTP/1.1
  # This should return a list of days and tasks as follows

  # Expected return
  # {date}20050903{/date}{task}1{/task}{validday}0{/validday}
  # {date}20050904{/date}{task}1{/task}{validday}0{/validday}
  # {date}20050907{/date}{task}1{/task}{validday}0{/validday}
  # {date}20050909{/date}{task}1{/task}{validday}1{/validday}
  # {date}20050910{/date}{task}1{/task}{validday}1{/validday}
  # {date}20050911{/date}{task}1{/task}{validday}1{/validday}

  # GET /getcontestinfo?contestname=LIVE&date=20171104&username=ogn&cpassword=ecbad38d0b5a3cf6482e661028b2c60c HTTP/1.1
  # This should return a CUC file of the selected day


# GetBannerInfo
@app.route("/getbannerinfo.php")
def getbannerinfo():
    # Example call 
    # GET /getbannerinfo.php HTTP/1.0
    return # do something

# gettrackerdata.php
@app.route("/gettrackerdata.php")
def gettrackerdata():
    querytype = request.args.get('querytype', type = str)
    contestname = request.args.get('contestname', type = str)
    trackerid = request.args.get('trackerid', type = str)
    username = request.args.get('username', type = str)
    cpassword = request.args.get('cpassword', type = str)
    starttime = request.args.get('starttime', type = str)
    endtime = request.args.get('endtime', type = str)
    compression = request.args.get('compression', type = str)

  # GET /gettrackerdata.php?querytype=getintfixes&contestname=FAIGP2005&trackerid=FLRDDA646&username=ogn&cpassword=ecbad38d0b5a3cf6482e661028b2c60c&starttime=20050911000001&endtime=20050911235959&compression=gzip HTTP/1.0

  app.logger.error('gettrackerdata.php was called: username = %s contestname = %s trackerid = %s starttime = %s',username,contestname,trackerid,starttime)

  if 'username' in request.args:
    app.logger.error('Username was provided in URL')
    pass # do something

  # TODO: This needs to be gzipped.
  return """{datadelay}0{/datadelay}\
	1052,20061230045824,-34.60305,138.72063,49.0,0\
	1052,20061230045828,-34.60306,138.72067,48.0,0\
	1052,20061230045832,-34.60306,138.72071,48.0,0\
	1052,20061230045836,-34.60306,138.72075,47.0,0\
	1052,20061230045840,-34.60306,138.72079,46.0,0\
	1052,20061230045844,-34.60307,138.72083,45.0,0"""

  # Expected return pattern:
  # <tracker id>,<timestamp>,<latitude>,<longitude>,<altitude>,<status>


  # Example request
  # GET /gettrackerdata.php?querytype=getintfixes&contestname=FAIGP2005&trackerid=FLRDDA646&username=ogn&cpassword=ecbad38d0b5a3cf6482e661028b2c60c&starttime=20050911000001&endtime=20050911235959&compression=gzip HTTP/1.0

def gencuc():
  # Generate temporary CUC file using StringIO.StringIO()
  CUC_temp = StringIO()

  # write CUC header
  CUC_temp.write("""[Options]
  Title=Angel Casado OGN-SGP test
  PeriodFrom=0
  PeriodTo=401521
  AvtoSaveFlight=True
  AvtoSaveTime=60
  AvtoPublishTime=-300
  TakeoffAlt=0m
  TaskPicWidth=600
  TaskPicHeight=400
  TaskPicCompression=90
  TaskPicBorder=12
  UtcOffset=1
  NeedLegs=False
  StrictName=False
  UseBinFiles=True
  CommentPrefix=1

  [Warnings]
  HighEnl=300
  AsViolate=True
  MinFinAlt=0m
  MaxFinAlt=10000m
  MaxStartAlt=0m
  MaxAlt=0m
  MaxAltCorr=50.0m
  AltTimeout=0
  StartGsp=0km/h
  FixRate=10
  ValFailed=True

  [SearchPath]
  \\psf\Home\Desktop\Flights\

  [Pilots] """)

  # write pilot list here
  CUC_temp.write("""\"John\", \"Doe\", 26356, \"CAIXX00,1052\"""")

  # write tail of CUC file
  CUC_temp.write("""V,HighEnl=300,AsViolate=True,MinFinAlt=0m,MaxFinAlt=10000m,MaxStartAlt=0m,MaxAlt=0m,MaxAltCorr=50.0m,AltTimeout=0,StartGsp=0km/h,FixRate=10,ValFailed=True
  C301299000000301299000003
  C4223150N00151500ELa Cerdanya - LECD
  C4223150N00151500ELa Cerdanya - LECD
  C4234110N00044360WSanta Cilia - LECI
  C4206290N00028590EBenabarre
  C4203020N00117320EOliana
  C4223150N00151500ELa Cerdanya - LECD
  C4223150N00151500ELa Cerdanya - LECD
  TSK,WpDis=True,MinDis=True,NearDis=0.5km,NearAlt=200.0m,MinFinAlt=0.0km
  XTest day
  E000,0,,,0,0,-1,-1,-1,-1,0,0,-1,-1,0,0,-1,-1,0,0,"",-1,-1,"",-1,,,,,,
  E001,0,,,0,0,-1,-1,-1,-1,0,0,-1,-1,0,0,-1,-1,0,0,"",-1,-1,"",-1,,,,,,
  E002,0,,,0,0,-1,-1,-1,-1,0,0,-1,-1,0,0,-1,-1,0,0,"",-1,-1,"",-1,,,,,,
  E003,0,,,0,0,-1,-1,-1,-1,0,0,-1,-1,0,0,-1,-1,0,0,"",-1,-1,"",-1,,,,,,
  E004,0,,,0,0,-1,-1,-1,-1,0,0,-1,-1,0,0,-1,-1,0,0,"",-1,-1,"",-1,,,,,,
  E005,0,,,0,0,-1,-1,-1,-1,0,0,-1,-1,0,0,-1,-1,0,0,"",-1,-1,"",-1,,,,,,
  """)

  # Reset postion in file to beginning
  CUC_temp.seek(0)
  return CUC_temp


#########################
# Following Sections provides the Silent Wings Studio interface
#########################

# eventgroups - DRAFT
@app.route('/eventgroups')
def eventgroups():
  # Define input, which we don't have yet
  vname = ['WM2020 Club','WM2020 18m']
  vdescription = ['Description of WM2020 Club','Description of WM2020 18m']
  vbannerUrl = ['www.xyz.de','www.123.de']
  return jsonify(
	name=vname,
	description=vdescription,
	bannerUrl=vbannerUrl
	)

