import pytest
from httpx import AsyncClient

TEST_EMAIL = "admin@gmail.com"
TEST_USER_PASSWORD = "admin123"
INVALID_TEST_PASSWORD = "incorrect-test-password"


@pytest.mark.asyncio
async def test_login_success(client: AsyncClient) -> None:
    """Unit test. Login returns token, role, and permissions."""
    response = await client.post(
        "/api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_USER_PASSWORD,
        },
    )
    data = response.json()

    assert response.status_code == 200
    assert "access_token" in data
    assert "role" in data
    assert "permissions" in data


@pytest.mark.asyncio
async def test_login_wrong_password(client: AsyncClient) -> None:
    """Unit test. Wrong password returns 401."""
    response = await client.post(
        "/api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": INVALID_TEST_PASSWORD,
        },
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_get_users_without_token(client: AsyncClient) -> None:
    """Unit test. No token blocks access."""
    response = await client.get("/api/users/")
    assert response.status_code in [401, 403]


@pytest.mark.asyncio
async def test_get_reports_without_token(client: AsyncClient) -> None:
    """Unit test. No token blocks reports."""
    response = await client.get("/api/reports/")
    assert response.status_code in [401, 403]


@pytest.mark.asyncio
async def test_login_returns_correct_role(client: AsyncClient) -> None:
    """Unit test. Correct role is returned."""
    response = await client.post(
        "/api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_USER_PASSWORD,
        },
    )

    assert response.status_code == 200
    assert response.json()["role"] is not None


@pytest.mark.asyncio
async def test_get_roles_with_token(client: AsyncClient) -> None:
    """Integration test. Login then get roles."""
    login = await client.post(
        "/api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_USER_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = await client.get(
        "/api/roles/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_users_with_token(client: AsyncClient) -> None:
    """Integration test. Login then get users."""
    login = await client.post(
        "/api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_USER_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = await client.get(
        "/api/users/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_permissions_in_login_response(client: AsyncClient) -> None:
    """Integration test. Permissions are returned on login."""
    response = await client.post(
        "/api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_USER_PASSWORD,
        },
    )

    data = response.json()

    assert response.status_code == 200
    assert isinstance(data["permissions"], dict)


@pytest.mark.asyncio
async def test_get_reports_with_token(client: AsyncClient) -> None:
    """Integration test. Login then get reports."""
    login = await client.post(
        "/api/auth/login",
        json={
            "email": TEST_EMAIL,
            "password": TEST_USER_PASSWORD,
        },
    )

    assert login.status_code == 200

    token = login.json()["access_token"]

    response = await client.get(
        "/api/reports/",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)
