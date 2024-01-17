from configstore.log import get_logger
import logging


def test_get_log_with_default_values(caplog):
    """Test the default log factory."""

    logger = get_logger()

    assert logger.name == "confstore"
    assert logger.level == logging.INFO
    assert logger.hasHandlers() is True

    assert logger.info("test info") is None

    assert "test" in caplog.text


def test_log_debug(caplog):
    """Test the default log factory with debug enabled."""

    logger = get_logger(debug=True)

    assert logger.name == "confstore"
    assert logger.level == logging.DEBUG
    assert logger.hasHandlers() is True

    assert logger.info("test info") is None
    assert logger.debug("test debug") is None

    assert "test info" in caplog.text
    assert "test debug" in caplog.text


def test_get_info_log_filters_debug(caplog):
    """Test the default log factory."""

    logger = get_logger()

    assert logger.name == "confstore"
    assert logger.level == logging.INFO
    assert logger.hasHandlers() is True

    assert logger.info("test info") is None
    assert logger.debug("test debug") is None

    assert "test info" in caplog.text
    assert "test debug" not in caplog.text


def test_log_stdout(caplog):
    """Test the default log factory with output to stdout."""

    logger = get_logger(stdout=True)

    assert logger.name == "confstore"
    assert logger.level == logging.INFO
    assert logger.hasHandlers() is True

    assert logger.info("test info") is None

    assert "test" in caplog.text
