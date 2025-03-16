from datetime import datetime
import pytest
import mongomock
from pymongo import MongoClient
from freezegun import freeze_time
from ..url_shortener import main, minifyUrl, expandUrl, UrlMapping, SHORTENED_URL_PREFIX

TESTING_LONG_URL = "https://www.example.com/path?q=search"
TESTING_SHORT_URL = f"{SHORTENED_URL_PREFIX}3"

@pytest.fixture
def expectedMapping():
    return UrlMapping(TESTING_LONG_URL,'3',datetime(2025, 3, 14, 12, 30),5)

@pytest.fixture(scope='function')
def test_db():
    client = mongomock.MongoClient()
    test_db = client["url_shortener"]
    return test_db

def test_message_no_args():
    inputUrl = TESTING_LONG_URL

    response = main()
    assert response.message == "Please provide either --minify or --expand parameter."
    
def test_minify(test_db, expectedMapping):
    inputUrl = TESTING_LONG_URL

    response = minifyUrl(test_db, inputUrl, 5)
    dbRecord = test_db.urls.find_one({"short_code": response.mapping.short_code})

    assert response.url == TESTING_SHORT_URL
    assert response.message == f"Shortened URL: {TESTING_SHORT_URL}"
    assert response.mapping.short_code == expectedMapping.short_code
    # db assertions
    assert test_db.urls.count_documents({}) == 1
    assert dbRecord["long_url"] == response.mapping.long_url

def test_minify_multiple_differents_urls_gives_different_codes(test_db):
    inputUrl1 = TESTING_LONG_URL
    inputUrl2 = f"{TESTING_LONG_URL}2"

    response1 = minifyUrl(test_db, inputUrl1, 5)
    response2 = minifyUrl(test_db, inputUrl2, 5)
    dbRecord1 = test_db.urls.find_one({"long_url": inputUrl1})
    dbRecord2 = test_db.urls.find_one({"long_url": inputUrl2})

    assert response1.url == TESTING_SHORT_URL
    assert response1.message == f"Shortened URL: {TESTING_SHORT_URL}"
    assert response2.url == f"{SHORTENED_URL_PREFIX}4"
    assert response2.message == f"Shortened URL: {SHORTENED_URL_PREFIX}4"
    # db assertions
    assert test_db.urls.count_documents({}) == 2
    assert dbRecord1["short_code"] == response1.mapping.short_code
    assert dbRecord2["short_code"] == response2.mapping.short_code

def test_minify_already_exist(test_db):
    inputUrl = TESTING_LONG_URL
    
    first_response = minifyUrl(test_db, inputUrl, 5)
    second_response = minifyUrl(test_db, inputUrl, 5)
    dbRecord =  test_db.urls.find_one({"short_code": second_response.mapping.short_code})

    assert second_response.url == TESTING_SHORT_URL
    assert second_response.message == f"Shortened URL: {TESTING_SHORT_URL}"
    # db assertions
    assert test_db.urls.count_documents({}) == 1
    assert dbRecord["long_url"] == second_response.mapping.long_url

@freeze_time("2025-03-14 12:30:01")
def test_expand(test_db, expectedMapping):
    test_db.urls.insert_one(expectedMapping.to_dict())
    inputUrl = TESTING_SHORT_URL

    response = expandUrl(test_db, inputUrl)
    
    assert response.url == TESTING_LONG_URL
    assert response.message == f"Original URL: {TESTING_LONG_URL}"
    assert response.mapping.long_url == TESTING_LONG_URL

def test_expand_not_found(test_db):
    inputUrl = TESTING_SHORT_URL

    response = expandUrl(test_db, inputUrl)
    
    assert response.url == ""
    assert response.message == "Error: Shortened URL does not exist or has expired."
    assert response.mapping == None

def test_minify_and_expand(test_db):
    inputUrl = TESTING_LONG_URL

    minifyResponse = minifyUrl(test_db, inputUrl, 5)
    short_url = minifyResponse.url

    expandResponse = expandUrl(test_db, short_url)
    long_url = expandResponse.url
    
    dbRecord = test_db.urls.find_one({"long_url": inputUrl})

    assert inputUrl == long_url
    # db assertions
    assert test_db.urls.count_documents({}) == 1
    assert dbRecord["long_url"] == inputUrl
    assert dbRecord["short_code"] == expandResponse.mapping.short_code

@freeze_time("2025-03-14 12:35:01")
def test_minify_already_exist_but_expired(test_db, expectedMapping):
    inputUrl = TESTING_LONG_URL
    test_db.urls.insert_one(expectedMapping.to_dict())
    test_db.counters.insert_one({"_id": "url_counter","count": 1})

    response = minifyUrl(test_db, inputUrl, 5)
    dbRecord =  test_db.urls.find_one({"short_code": response.mapping.short_code})

    assert response.url == f"{SHORTENED_URL_PREFIX}4"
    assert response.message == f"Shortened URL: {SHORTENED_URL_PREFIX}4"
    # db assertions
    assert test_db.urls.count_documents({}) == 2
    assert dbRecord["long_url"] == response.mapping.long_url

@freeze_time("2025-03-14 12:40:01")
def test_expired_url(test_db, expectedMapping):
    test_db.urls.insert_one(expectedMapping.to_dict())
    inputUrl = TESTING_SHORT_URL

    response = expandUrl(test_db, inputUrl)

    assert response.url == ""
    assert response.message == "Error: Shortened URL does not exist or has expired."
    assert response.mapping == None