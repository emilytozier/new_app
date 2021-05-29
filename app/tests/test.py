from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker




db_name = 'postgres'
db_user = 'postgres'
db_pass = 'postgres'
db_host = 'my_db'
db_port = '5432'

def pytest_addoption(parser):
    parser.addoption('--dburl',
                     action='store',
                     default='<if needed, whatever your want>',
                     help='postgresql://postgres:postgres@my_db:5432/postgres')
                     
@pytest.fixture(scope='session')
def db_engine(request):
    db_url = request.config.getoption("--dburl")
    engine_ = create_engine('postgresql://{}:{}@{}:{}/{}'.format(db_user, db_pass, db_host, db_port, db_name, echo=True)

    yield engine_

    engine_.dispose()


@pytest.fixture(scope='session')
def db_session_factory(db_engine):
    return scoped_session(sessionmaker(bind=engine))


@pytest.fixture(scope='function')
def db_session(db_session_factory):
    session_ = session_factory()

    yield session_

    session_.rollback()
    session_.close()
