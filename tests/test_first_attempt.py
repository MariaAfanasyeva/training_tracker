import pytest

from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.from_pyfile("config_test.py")

    # other setup can go here

    yield app
    #TODO: add here drop database
    # clean up / reset resources here


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.mark.parametrize("endpoint", [("/groups"), ("/users"), ("/weights"), ("/distances"), ("/exercises"), ("/sets"), ("/trainings")])
def test_status_code_get_all_groups(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200
