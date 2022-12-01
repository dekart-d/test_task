from __future__ import annotations
import requests

#  =============== API_URL ===============
API_PATH = "https://nominatim.openstreetmap.org/search.php?q="
API_PATH_RESULT_FORMAT = "&format=jsonv2"


# =========================================


#  =============== PREPARE_DATA ===============
def send_request_to_openstreetmap(
        request_data: str,
        get_json: bool = False):
    if get_json:
        return requests.get(f"{API_PATH}{request_data}{API_PATH_RESULT_FORMAT}").json()
    return requests.get(f"{API_PATH}{request_data}{API_PATH_RESULT_FORMAT}")


class ExpectedData:
    def __init__(
            self,
            request_address: str,
            boundingbox: list[str],
            category: str,
            type: str,
            importance: float,
            display_name: str,
            osm_id: int,
    ):
        self.request_address = request_address
        self.boundingbox = boundingbox
        self.category = category
        self.type = type
        self.importance = importance
        self.display_name = display_name
        self.osm_id = osm_id

    def compare_json_with_expected_data(self, json_response):
        try:
            return json_response['boundingbox'] == self.boundingbox and \
                   json_response['category'] == self.category and \
                   json_response['type'] == self.type and \
                   json_response['importance'] == self.importance and \
                   json_response['display_name'] == self.display_name and \
                   json_response['osm_id'] == self.osm_id
        except Exception:
            return False


# =========================================


#  =============== DATA ===============
requests_addresses = [
    "Санкт-Петербург Коммуны 26к2",
    "Воронцовский бульвар 18",
    "53.9075928 27.512981131131617",
]

expected_data = {
    requests_addresses[0]: ExpectedData(
        request_address="Санкт-Петербург Коммуны 26к2",
        boundingbox=['59.827664', '59.8279379', '30.1845685', '30.1851256'],
        category='building',
        type='apartments',
        importance=0.2001,
        display_name='26 к2, Авангардная улица, Лигово, округ Урицк, '
                     'Санкт-Петербург, Северо-Западный федеральный округ, 198205, Россия',
        osm_id=129921125
    ),
    requests_addresses[1]: ExpectedData(
        request_address="Воронцовский бульвар 18",
        boundingbox=['60.0639034', '60.0652862', '30.426555', '30.4277942'],
        category='building',
        type='apartments',
        importance=0.31010000000000004,
        display_name='18, Воронцовский бульвар, Западный микрорайон, Западное Мурино, Мурино, '
                     'Муринское городское поселение, Всеволожский район, Ленинградская область, '
                     'Северо-Западный федеральный округ, 188677, Россия',
        osm_id=445242146
    ),
    requests_addresses[2]: ExpectedData(
        request_address="53.9075928 27.512981131131617",
        boundingbox=['53.9074816', '53.9077876', '27.5126543', '27.5133284'],
        category='building',
        type='government',
        importance=0.001,
        display_name='Военкомат Фрунзенского района, 35, Кальварыйская вуліца, Кальварыя, Тучынка, '
                     'Фрунзенскі раён, Мінск, 220073, Беларусь',
        osm_id=25391022
    ),
}


# ====================================


#  =============== TESTS ===============
def test_status_ok():
    assert send_request_to_openstreetmap('Воронцовский бульвар 10').status_code == 200


def test_expected_data_address_request():
    test_request = requests_addresses[0]
    test_case_expected_data = expected_data[test_request]
    json_response = send_request_to_openstreetmap(test_request, get_json=True)[0]
    assert test_case_expected_data.compare_json_with_expected_data(json_response=json_response)


def test_expected_data_adress_1_request():
    test_request = requests_addresses[1]
    test_case_expected_data = expected_data[test_request]
    json_response = send_request_to_openstreetmap(test_request, get_json=True)[0]
    assert test_case_expected_data.compare_json_with_expected_data(json_response=json_response)


def test_expected_data_lat_lon():
    test_request = requests_addresses[2]
    json_response = send_request_to_openstreetmap(test_request, get_json=True)[0]
    test_case_expected_data = expected_data[test_request]
    assert test_case_expected_data.compare_json_with_expected_data(json_response=json_response)

# ====================================
