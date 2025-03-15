import datetime
import pytest
import mongomock
from pymongo import MongoClient
from ..url_shortener import minifyUrl, expandUrl, UrlMapping

@pytest.fixture(scope='function')
#@pytest.fixture(autouse=True)
def test_db():
    client = mongomock.MongoClient()
    test_db = client["url_shortener"]
    return test_db

@pytest.fixture
def expected():
    return UrlMapping("https://www.example.com/path?q=search","3",'',5)


def test_minify(test_db, expected):
    inputUrl = expected.long_url

    response = minifyUrl(test_db, inputUrl, 5)
    dbRecord =  test_db.urls.find_one({"long_url": inputUrl})

    assert response.url.short_code == expected.short_code
    assert response.message == "Shortened URL: https://myurlshortener.com/3"
    # db assertions
    assert test_db.urls.count_documents({}) == 1
    assert dbRecord["short_code"] == response.url.short_code

def test_expand():
    assert False

def test_minify_and_expand():
    assert False

def test_expand_not_found():
    assert False

def test_expand_already_expanded():
    assert False

def test_minify_already_exist():
    assert False

def test_minify_already_exist_but_expired():
    assert False

def test_minify_multiple(expected):
    #mapping = {
    #    "long_url": '',
    #    "short_code": 'aaa',
    #    "created_at": '',
    #    "expiration_seconds": 5
    #}
    #test_db.urls.results.insert_one(mapping)
    assert False

def test_expired_url():
    assert False