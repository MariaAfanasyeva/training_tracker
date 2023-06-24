import pytest
from extensions import db
from models import Weight

from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.from_pyfile("config_test.py")
    return app


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture(autouse=True)
def insert_weight(app):
    db.init_app(app)
    with app.app_context():
        db.session.query(Weight).delete()
        insert_command = """
        INSERT INTO weight(id, weight, units, added_by) VALUES (1, 5.0, 'kg', 1);
        """
        db.session.execute(insert_command)
        db.session.commit()
        yield
        db.session.query(Weight).delete()
        db.session.commit()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.mark.parametrize("endpoint", [("/groups"), ("/users"), ("/weights"), ("/distances"), ("/exercises"), ("/sets"), ("/trainings")])
def test_status_code_get_all_groups(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200
    

@pytest.mark.usefixtures('insert_weight')
def test_get_first_weight(client):
    response = client.get('/weight/1')
    assert response.status_code == 200
    
