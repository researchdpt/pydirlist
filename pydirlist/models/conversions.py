import pydirlist

intervals = (
    ('weeks', 604800),  # 60 * 60 * 24 * 7
    ('days', 86400),    # 60 * 60 * 24
    ('hours', 3600),    # 60 * 60
    ('minutes', 60),
    ('seconds', 1),
    )

def display_time(seconds, granularity=2):
    result = []

    for name, count in intervals:
        value = seconds // count
        if value:
            seconds -= value * count
            if value == 1:
                name = name.rstrip('s')
            result.append("{} {}".format(value, name))
    return ', '.join(result[:granularity])

#Code for the "page generation took x seconds" thing.
@pydirlist.app.before_request
def before_request():
    pydirlist.g.request_start_time = pydirlist.time.time()
    pydirlist.g.request_time = lambda: "%.5f" % (pydirlist.time.time() - pydirlist.g.request_start_time)

#Current time as a part of the code
@pydirlist.app.context_processor
def inject_now():
    return {'now': pydirlist.datetime.utcnow()}

#Current time in UNIX format
def unix_time_current():
    return int(pydirlist.time.time())
pydirlist.app.jinja_env.globals.update(unix_time_current=unix_time_current)

#Display how long ago something happened in a readable format
@pydirlist.app.template_filter('time_ago')
def time_ago(unixtime):
    return pydirlist.humanize.naturaltime(pydirlist.datetime.now() - pydirlist.timedelta(seconds=unix_time_current() - int(unixtime)))
pydirlist.app.jinja_env.globals.update(time_ago=time_ago)

#Display a somewhat normal date
@pydirlist.app.template_filter('human_date')
def human_date(unixtime):
    return pydirlist.datetime.fromtimestamp(int(unixtime)).strftime('%Y-%m-%d %H:%M:%S')
pydirlist.app.jinja_env.globals.update(human_date=human_date)

#Display a somewhat normal size
@pydirlist.app.template_filter('human_size')
def human_size(filesize):
    return pydirlist.humanize.naturalsize(filesize)
pydirlist.app.jinja_env.globals.update(human_size=human_size)
