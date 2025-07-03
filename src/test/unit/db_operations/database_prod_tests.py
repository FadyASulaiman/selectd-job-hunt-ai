import pytest
import random
import hashlib
from typing import Dict, Any

from core.database.database_manager import DatabaseManager


@pytest.mark.prod
def test_create_user_happy_path_production():
    """
    Production test for create_user happy path.
    This test creates an actual user record in the production database.
    """
    # Generate random number for unique test user
    random_number = random.randint(10000, 99999)
    test_username = f"test_user_{random_number}"
    test_email = f"test_user_{random_number}@example.com"
    
    # Create test user data
    user_data: Dict[str, Any] = {
        'username': test_username,
        'email': test_email,
        'password_hash': hashlib.sha256('test_password'.encode()).hexdigest(),
        'first_name': 'Test',
        'last_name': 'User',
        'is_active': True
    }
    
    # Initialize database manager (will use production DB via Settings.DB_PATH)
    db_manager = DatabaseManager()
    
    # Create user in production database
    user_id = db_manager.create_user(user_data)
    
    # Verify user was created successfully
    assert user_id is not None
    assert isinstance(user_id, int)
    assert user_id > 0
    
    # Verify the user exists in the database by querying directly
    with db_manager.connection_manager.get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT user_id, username, email, first_name, last_name, is_active FROM users WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        
        assert result is not None
        assert result['user_id'] == user_id
        assert result['username'] == test_username
        assert result['email'] == test_email
        assert result['first_name'] == 'Test'
        assert result['last_name'] == 'User'
        assert result['is_active'] == 1  # SQLite stores boolean as integer
    
    print(f"Successfully created test user with ID: {user_id}, username: {test_username}")

# pytest -m prod src/test/unit/db_operations/database_prod_tests.py::test_create_user_happy_path_production
