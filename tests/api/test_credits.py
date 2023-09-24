from http import HTTPStatus

from httpx import AsyncClient

from credit.schemas import CreditCloseRead, CreditOpenRead


async def test_credits_get_by_id(client: AsyncClient):
    r = await client.get("/api/v1/user_credits/8/")
    data_all = r.json()
    assert r.status_code == HTTPStatus.OK
    if data_all:
        for data in data_all:
            assert "credit_close" in data
            if data["credit_close"]:
                assert CreditCloseRead.model_validate(data)
            else:
                assert CreditOpenRead.model_validate(data)


async def test_credits_get_by_wrong_id(client: AsyncClient):
    r = await client.get("/api/v1/user_credits/dfer/")
    data_all = r.json()
    assert r.status_code == HTTPStatus.UNPROCESSABLE_ENTITY
    assert (
            data_all["detail"][0]["msg"]
            == "Input should be a valid integer, unable to parse string as an integer"
    )


async def test_credits_get_by_no_id(client: AsyncClient):
    r = await client.get("/api/v1/user_credits//")
    data_all = r.json()
    assert r.status_code == HTTPStatus.NOT_FOUND
    assert data_all["detail"] == "Not Found"
