from app.model import Contest
from app import db


def get_active_contests():
    result_string = ""
    for contest in db.session.query(Contest):
        short_name = contest.name.replace(" ", "").upper()
        long_name = contest.name
        result_string += "{{contestname}}{0}{{/contestname}}".format(short_name)
        result_string += "{{contestdisplayname}}{0}{{/contestdisplayname}}".format(long_name)

        result_string += "{{datadelay}}{0}{{/datadelay}}".format(15)
        result_string += "{{utcoffset}}{0}{{/utcoffset}}".format("+01:00")
        result_string += "{{countrycode}}{0}{{/countrycode}}".format(contest.country)
        result_string += "{{site}}{0}{{/site}}".format("St. Auban")
        result_string += "{{fromdate}}{0}{{/fromdate}}".format(contest.start_date.strftime("%Y%m%d"))
        result_string += "{{todate}}{0}{{/todate}}".format(contest.end_date.strftime("%Y%m%d"))
        result_string += "{{lat}}{0}{{/lat}}".format(44.1959)
        result_string += "{{lon}}{0}{{/lon}}".format(5.98849)
        result_string += "{{alt}}{0}{{/alt}}".format("")

    return result_string
