from bot import crud


def help_text(chat_id):
    user = crud.get_user(chat_id)
    return """Helping text:
/run - launch notification
/stop - stop notification
/current - show current value    
    
/interval <seconds> - change interval. Current: {interval}
/overweight <integer> - change overweight rate to notify. Current: {overweight}
/min_value <integer> - change min border. Current: {min_value}
/max_value <integer> - change max border. Current: {max_value}
""".format(interval=user.interval,
           overweight=user.overweight,
           diff=user.diff,
           min_value=user.min_value,
           max_value=user.max_value)

overweight_text = """Overweight:
/overweight <integer> - change overweight rate to notify
"""

interval_text = """Interval:
/interval <seconds> - change interval
"""
#
# diff_text = """Diff:
# /diff <integer> - change different, this value update min and max borders
# """

min_value_text = """Min value:
/min_value <integer> - change min border
"""

max_value_text = """Max value:
/max_value <integer> - change max border
"""

current_text = """Current:
/current - show current coin value
"""