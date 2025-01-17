from unittest.mock import MagicMock
from unittest.mock import patch

from sqlalchemy.orm import Session

from gitlab_monitor.services.bdd.bdd import DB_URL
from gitlab_monitor.services.bdd.bdd import Database


def test_database_initialization():
    """Test the initialization of the Database class."""
    db = Database()
    assert db._session is None


@patch("gitlab_monitor.services.bdd.bdd.create_engine")
@patch("gitlab_monitor.services.bdd.bdd.Base.metadata.create_all")
def test_initialize_database(mock_create_all, mock_create_engine):
    """Test the _initialize_database method."""
    mock_engine = MagicMock()
    mock_session = MagicMock()

    mock_create_engine.return_value = mock_engine
    mock_engine.connect.return_value = True
    mock_sessionmaker = MagicMock(return_value=mock_session)

    with patch("gitlab_monitor.services.bdd.bdd.sessionmaker", mock_sessionmaker):
        db = Database()
        session = db._initialize_database()

        mock_create_engine.assert_called_once_with(DB_URL)
        mock_engine.connect.assert_called_once()
        mock_create_all.assert_called_once_with(bind=mock_engine)
        mock_sessionmaker.assert_called_once_with(bind=mock_engine)

        assert session == mock_session()


@patch.object(Database, "_initialize_database", return_value=MagicMock(spec=Session))
def test_session_property(mock_initialize_database):
    """Test the session property."""
    db = Database()

    session = db.session
    assert session == mock_initialize_database.return_value
    mock_initialize_database.assert_called_once()

    session_again = db.session
    assert session_again == session
    mock_initialize_database.assert_called_once()
