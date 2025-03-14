import datetime
import pytest
import mongomock
from pymongo import MongoClient
from ..url_shortener import minifyUrl, expandUrl, UrlMapping

@pytest.fixture(autouse=True)
def test_db():
    test_db = mongomock.MongoClient()
    #test_db.drop_database('url_shortener_test')
    return test_db

@pytest.fixture
def expected():
    return UrlMapping("https://www.example.com/path?q=search","https://myurlshortener.com/fstp4",'',5)


def test_minify(test_db, expected):
    inputUrl = expected.long_url

    response = minifyUrl(test_db, inputUrl, 5)

    dbCollection = test_db.urls.results
    dbRecord = dbCollection.find_one({"long_url": inputUrl})

    assert response.url.short_code == expected.short_code
    assert response.message == "Shortened URL: https://myurlshortener.com/fstp4"
    # db assertions
    assert dbCollection.count_documents({}) == 1
    assert dbRecord["short_code"] == response.url.short_code

def test_expand():
    assert False

def test_minify_and_expand():
    assert False

def test_expande_not_found():
    assert False

def test_expand_already_expanded():
    assert False

def test_minify_already_exist():
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