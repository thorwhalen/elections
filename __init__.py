from functools import partial

import requests
import pandas as pd

from py2store.utils.explicit import ExplicitKeysSource
from py2store import add_ipython_key_completions, KvReader, Store, wrap_kvs

state_stubs = ['alabama', 'alaska', 'arizona', 'arkansas', 'california', 'colorado',
               'connecticut', 'delaware', 'district-of-columbia', 'florida', 'georgia',
               'hawaii', 'idaho', 'illinois', 'indiana', 'iowa', 'kansas', 'kentucky',
               'louisiana', 'maine', 'maryland', 'massachusetts', 'michigan', 'minnesota',
               'mississippi', 'missouri', 'montana', 'nebraska', 'nevada', 'new-hampshire',
               'new-jersey', 'new-mexico', 'new-york', 'north-carolina', 'north-dakota', 'ohio',
               'oklahoma', 'oregon', 'pennsylvania', 'rhode-island', 'south-carolina', 'south-dakota',
               'tennessee', 'texas', 'utah', 'vermont', 'virginia', 'washington', 'west-virginia',
               'wisconsin', 'wyoming']


def get_json_for_state(state):

    url = f'https://static01.nyt.com/elections-assets/2020/data/api/2020-11-03/state-page/{state}.json'
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        print(
            f"Something went wrong with state {state}. I'm outputing the raw response")
        return r


@add_ipython_key_completions
@Store.wrap
class Election2020RawJson(ExplicitKeysSource):

    def __init__(self):
        super().__init__(key_collection=state_stubs,
                         _obj_of_key=get_json_for_state)


class Races2020(Election2020RawJson):
    def _obj_of_data(self, data):
        state_slug = data['data']['races'][0]['state_id'].lower()
        races = Store({x['race_slug'][3:]: x for x in data['data']['races']})
        return add_ipython_key_completions(races)


def post_process_timeseries(data):
    df = pd.DataFrame(data['president-general-2020-11-03']['timeseries'])
    df = pd.concat(
        (df, pd.DataFrame(df['vote_shares'].values.tolist())), axis=1)
    del df['vote_shares']
    df = df.set_index('timestamp')
    return df


President2020TimeSeries = wrap_kvs(
    Races2020, obj_of_data=post_process_timeseries)
    
