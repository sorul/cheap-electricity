import sys
import types

# Stub for pandas with minimal functionality required by the project
class FakeDataFrame:
    def __init__(self, data):
        # store columns as simple dict of lists
        self.data = {}
        if isinstance(data, list) and data:
            for key in data[0].keys():
                self.data[key] = [row.get(key) for row in data]

    def __getitem__(self, key):
        return self.data.get(key, [])

    def __setitem__(self, key, value):
        self.data[key] = value

    def set_index(self, *args, **kwargs):
        return self

    def drop(self, *args, **kwargs):
        return self

    def __repr__(self):  # pragma: no cover - debugging representation
        return "FakeDataFrame()"

class FakeSeries(list):
    def quantile(self, q):
        sorted_vals = sorted(self)
        if not sorted_vals:
            return None
        index = (len(sorted_vals) - 1) * q
        lower = int(index)
        upper = min(lower + 1, len(sorted_vals) - 1)
        fraction = index - lower
        return sorted_vals[lower] + (sorted_vals[upper] - sorted_vals[lower]) * fraction

def to_datetime(values):
    return values

fake_pandas = types.ModuleType("pandas")
fake_pandas.DataFrame = FakeDataFrame
fake_pandas.Series = FakeSeries
fake_pandas.to_datetime = to_datetime
sys.modules.setdefault("pandas", fake_pandas)

# Stub for telegram.Bot
class FakeBot:
    def __init__(self, token):
        self.token = token

    async def send_message(self, chat_id, text):
        pass

fake_telegram = types.ModuleType("telegram")
fake_telegram.Bot = FakeBot
sys.modules.setdefault("telegram", fake_telegram)

# Stub for dotenv.load_dotenv
fake_dotenv = types.ModuleType("dotenv")
def load_dotenv():
    return None
fake_dotenv.load_dotenv = load_dotenv
sys.modules.setdefault("dotenv", fake_dotenv)
# Stub for requests to avoid external HTTP calls
fake_requests = types.ModuleType("requests")
class RequestException(Exception):
    pass

fake_requests.RequestException = RequestException
fake_requests.exceptions = types.SimpleNamespace(RequestException=RequestException)

def get(*args, **kwargs):
    raise RequestException("HTTP calls are disabled in tests")

fake_requests.get = get
sys.modules.setdefault("requests", fake_requests)
