# This file is auto-magically utilized by "server" runner
# in conjunction with App Stats functionality.

# https://cloud.google.com/appengine/docs/python/tools/appstats#Python_Optional_configuration

# Presence of this function causes recording of the App Stats
def webapp_add_wsgi_middleware(app):
  from google.appengine.ext.appstats import recording
  app = recording.appstats_wsgi_middleware(app)
  return app

# Some of the more-interesting settings from original `sample_appengine_config.py`

# CALC_RPC_COSTS: True or False. This is an experimental flag
# and is not guaranteed to be supported or work the same way in the
# future. When True, the cost and billed operations for each RPC are
# recorded and displayed in the AppStats UI. Turning this option on
# may negatively impact application performance.
appstats_CALC_RPC_COSTS = False

# DATASTORE_DETAILS: True or False. This is an experimental flag
# and is not guaranteed to be supported or work the same way in the
# future. When True, information regarding keys of entities read or
# written during various datastore operations and other related details
# are recorded. Currently the information is logged for the following
# datastore calls: Get, Put, RunQuery and Next.
appstats_DATASTORE_DETAILS = False

# Fraction of requests to record.  Set this to a float between 0.0
# and 1.0 to record that fraction of all requests.
appstats_RECORD_FRACTION = 1.0
