"""Constants."""

import datetime

# full data not collected before this date
COLLECTION_STARTED = datetime.date(2019, 5, 1)

LADDERS = {
    'voobly': {
        131: 'RM - 1v1',
        132: 'RM - Team Games',
        163: 'DM - 1v1'
    },
    'vooblycn': {
        131: 'RM - 1v1',
        132: 'RM - Team Games',
        163: 'DM - 1v1'
    },
    'qq': {
        1: 'W'
    }
}
