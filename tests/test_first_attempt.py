import pytest
import datetime
from extensions import db
from models import Weight, Distance, Group, Training, Exercise, Set, User

from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.from_pyfile("config_test.py")
    return app


@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def insert_test_data(app):
    db.init_app(app)
    with app.app_context():
        db.session.query(Weight).delete()
        db.session.query(Distance).delete()
        db.session.query(Group).delete()
        db.session.query(Training).delete()
        db.session.query(Exercise).delete()
        db.session.query(Set).delete()
        db.session.query(User).delete()
        new_user = User(id=1, first_name='John', last_name='Doe', email='john.doe@gmail.com', password='password')
        db.session.add(new_user)
        new_weight = Weight(id=1, weight=5.0, units='kg', added_by=1)
        db.session.add(new_weight)
        new_disatance = Distance(id=1, distance=2, units='km', added_by=1)
        db.session.add(new_disatance)
        new_group = Group(id=1, name='Legs', added_by=1)
        db.session.add(new_group)
        new_training = Training(id=1, training_date='2023-06-22', status='started', created_by=1)
        db.session.add(new_training)
        new_exercise = Exercise(id=1, name='Squat', group_id=1, added_by=1)
        db.session.add(new_exercise)
        new_set = Set(id=1, exercise_count=15, added_by=1, exercise_id=1, training_id=1, weight_id=1, distance_id=1)
        db.session.add(new_set)
        db.session.commit()
        yield
        db.session.query(Weight).delete()
        db.session.query(Distance).delete()
        db.session.query(Group).delete()
        db.session.query(Training).delete()
        db.session.query(Exercise).delete()
        db.session.query(Set).delete()
        db.session.query(User).delete()
        db.session.commit()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


@pytest.mark.parametrize("endpoint", [("/groups"), ("/users"), ("/weights"), ("/distances"), ("/exercises"), ("/sets"), ("/trainings")])
def test_status_code_get_all_groups(client, endpoint):
    response = client.get(endpoint)
    assert response.status_code == 200
    

@pytest.mark.parametrize("endpoint", [("/group"), ("/user"), ("/weight"), ("/distance"), ("/exercise"), ("/set"), ("/training")])
def test_status_code_get_first_weight(client, endpoint, insert_test_data):
    response = client.get(f'{endpoint}/1')
    assert response.status_code == 200
    
