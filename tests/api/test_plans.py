from datetime import date
from http import HTTPStatus

from httpx import AsyncClient

from plan.schemas import (
    PlanCreditPerformance,
    PlanPaymentPerformance,
    YearPerformance,
)


async def test_plans_performance_by_valid_date(client: AsyncClient):
    params = {
        "date": "2021-01-21",
    }
    r = await client.get("/api/v1/plans_performance/", params=params)
    data_all = r.json()
    assert r.status_code == HTTPStatus.OK
    if data_all:
        for data in data_all:
            assert "category_name" in data
            if data["category_name"] == "видача":
                assert PlanCreditPerformance.model_validate(data)
            else:
                assert PlanPaymentPerformance.model_validate(data)


async def test_plans_performance_by_invalid_date(client: AsyncClient):
    params = {
        "date": "202101-21",
    }
    r = await client.get("/api/v1/plans_performance/", params=params)
    data_all = r.json()
    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert data_all["detail"] == "Invalid date format. Please use YYYY-MM-DD format."


async def test_plans_performance_by_future_date(client: AsyncClient):
    params = {
        "date": "2074-01-21",
    }
    r = await client.get("/api/v1/plans_performance/", params=params)
    data_all = r.json()
    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert data_all["detail"] == "Date must be not in the future"


async def test_year_performance_by_valid_year(client: AsyncClient):
    params = {
        "year": 2021,
    }
    r = await client.get("/api/v1/year_performance/", params=params)
    data_all = r.json()
    assert r.status_code == HTTPStatus.OK
    if data_all:
        for data in data_all:
            assert YearPerformance.model_validate(data)


async def test_year_performance_by_invalid_year(client: AsyncClient):
    params = {
        "year": "sdf",
    }
    r = await client.get("/api/v1/year_performance/", params=params)
    data_all = r.json()
    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
        data_all["detail"][0]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )


async def test_year_performance_by_future_date(client: AsyncClient):
    params = {
        "year": 2070,
    }
    r = await client.get("/api/v1/year_performance/", params=params)
    data_all = r.json()
    assert r.status_code == HTTPStatus.NOT_FOUND
    today = date.today().year
    assert data_all["detail"] == f"Year must be not in the future, now is {today}"
