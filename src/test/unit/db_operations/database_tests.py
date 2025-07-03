import unittest
import sqlite3
import tempfile
import os

import shutil
import pytest
import threading
import time

from core.database.database_manager import DatabaseManager
from core.database.db_connection_manager import DatabaseConnectionManager
from core.database.db_schema_manager import DatabaseSchema
from core.repositories.user_repository import UserRepository
from core.validators.db_data_validator import DataValidator


@pytest.mark.unit
class TestDataValidator(unittest.TestCase):
    """Unit tests for DataValidator"""
    
    def test_validate_user_data_success(self):
        """Test successful user data validation"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        result = DataValidator.validate_user_data(user_data)
        
        self.assertEqual(result['username'], 'testuser')
        self.assertEqual(result['email'], 'test@example.com')
        self.assertEqual(result['first_name'], 'Test')
        self.assertEqual(result['last_name'], 'User')
        self.assertTrue(result['is_active'])
    
    def test_validate_user_data_missing_required_field(self):
        """Test validation fails with missing required field"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com'
            # Missing password_hash
        }
        
        with self.assertRaises(ValueError) as context:
            DataValidator.validate_user_data(user_data)
        
        self.assertIn("Required field 'password_hash' is missing", str(context.exception))
    
    def test_validate_user_data_invalid_email(self):
        """Test validation fails with invalid email"""
        user_data = {
            'username': 'testuser',
            'email': 'invalid_email',
            'password_hash': 'hashed_password'
        }
        
        with self.assertRaises(ValueError) as context:
            DataValidator.validate_user_data(user_data)
        
        self.assertIn("Invalid email format", str(context.exception))
    
    def test_validate_user_data_with_defaults(self):
        """Test validation with minimal data uses defaults"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password'
        }
        
        result = DataValidator.validate_user_data(user_data)
        
        self.assertIsNone(result['first_name'])
        self.assertIsNone(result['last_name'])
        self.assertTrue(result['is_active'])
    
    def test_validate_job_application_data_success(self):
        """Test successful job application data validation"""
        company_info = {
            'company_name': 'Test Company',
            'job_title': 'Developer',
            'location': 'New York',
            'user_id': 123
        }
        
        result = DataValidator.validate_job_application_data(company_info)
        
        self.assertEqual(result['company_name'], 'Test Company')
        self.assertEqual(result['job_title'], 'Developer')
        self.assertEqual(result['user_id'], 123)
    
    def test_validate_job_application_data_with_defaults(self):
        """Test job application validation with minimal data"""
        company_info = {}
        
        result = DataValidator.validate_job_application_data(company_info)
        
        self.assertEqual(result['company_name'], 'Unknown')
        self.assertEqual(result['job_title'], 'Unknown')
        self.assertEqual(result['location'], 'Not specified')
        self.assertEqual(result['user_id'], 1)

@pytest.mark.unit
class TestUserRepository(unittest.TestCase):
    """Unit tests for UserRepository"""
    
    def setUp(self):
        """Set up test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, 'test.db')
        self.connection_manager = DatabaseConnectionManager(self.test_db_path)
        self.repository = UserRepository(self.connection_manager)
        
        # Create the users table
        schema = DatabaseSchema()
        with self.connection_manager.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(schema.get_users_table_sql())
            conn.commit()
    
    def tearDown(self):
        """Clean up after each test"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_user_success(self):
        """Test successful user creation"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password',
            'first_name': 'Test',
            'last_name': 'User'
        }
        
        user_id = self.repository.create_user(user_data)
        
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
    
    def test_create_user_duplicate_username(self):
        """Test creating user with duplicate username fails"""
        user_data = {
            'username': 'testuser',
            'email': 'test1@example.com',
            'password_hash': 'hashed_password'
        }
        
        # Create first user
        self.repository.create_user(user_data)
        
        # Try to create second user with same username
        user_data['email'] = 'test2@example.com'
        
        with self.assertRaises(sqlite3.IntegrityError):
            self.repository.create_user(user_data)
    
    def test_get_user_by_id_exists(self):
        """Test getting user by ID when user exists"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password'
        }
        
        user_id = self.repository.create_user(user_data)
        result = self.repository.get_user_by_id(user_id)
        
        self.assertIsNotNone(result)
        self.assertEqual(result['username'], 'testuser')
        self.assertEqual(result['email'], 'test@example.com')
    
    def test_get_user_by_id_not_exists(self):
        """Test getting user by ID when user doesn't exist"""
        result = self.repository.get_user_by_id(999)
        self.assertIsNone(result)
    
    def test_get_user_by_username(self):
        """Test getting user by username"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password'
        }
        
        self.repository.create_user(user_data)
        result = self.repository.get_user_by_username('testuser')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['email'], 'test@example.com')
    
    def test_get_user_by_email(self):
        """Test getting user by email"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password'
        }
        
        self.repository.create_user(user_data)
        result = self.repository.get_user_by_email('test@example.com')
        
        self.assertIsNotNone(result)
        self.assertEqual(result['username'], 'testuser')
    
    def test_update_last_login(self):
        """Test updating user's last login"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password'
        }
        
        user_id = self.repository.create_user(user_data)
        self.repository.update_last_login(user_id)
        
        result = self.repository.get_user_by_id(user_id)
        self.assertIsNotNone(result['last_login'])
        self.assertIsNotNone(result['updated_at'])
    
    def test_deactivate_user(self):
        """Test user deactivation"""
        user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password_hash': 'hashed_password'
        }
        
        user_id = self.repository.create_user(user_data)
        self.repository.deactivate_user(user_id)
        
        result = self.repository.get_user_by_id(user_id)
        self.assertFalse(result['is_active'])
        self.assertIsNotNone(result['updated_at'])


@pytest.mark.integration
class TestDatabaseManagerIntegration(unittest.TestCase):
    """Integration tests for the DatabaseManager"""
    
    def setUp(self):
        """Set up test environment with real database"""
        self.temp_dir = tempfile.mkdtemp()
        self.test_db_path = os.path.join(self.temp_dir, 'integration_test.db')
        self.db_manager = DatabaseManager(self.test_db_path)
    
    def tearDown(self):
        """Clean up after each test"""
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_create_user_integration(self):
        """Test complete user creation flow"""
        user_data = {
            'username': 'integrationuser',
            'email': 'integration@example.com',
            'password_hash': 'secure_hash_123',
            'first_name': 'Integration',
            'last_name': 'User'
        }
        
        user_id = self.db_manager.create_user(user_data)
        
        # Verify user was created
        self.assertIsInstance(user_id, int)
        self.assertGreater(user_id, 0)
        
        # Verify user can be retrieved
        retrieved_user = self.db_manager.get_user_by_id(user_id)
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user['username'], 'integrationuser')
        self.assertEqual(retrieved_user['email'], 'integration@example.com')
        self.assertEqual(retrieved_user['first_name'], 'Integration')
        self.assertTrue(retrieved_user['is_active'])
    
    def test_user_and_job_application_workflow(self):
        """Test complete workflow: create user, then create job application"""
        # Create user
        user_data = {
            'username': 'workflowuser',
            'email': 'workflow@example.com',
            'password_hash': 'secure_hash_456'
        }
        
        user_id = self.db_manager.create_user(user_data)
        
        # Create job application for the user
        company_info = {
            'company_name': 'Workflow Company',
            'job_title': 'Integration Tester',
            'location': 'Remote',
            'user_id': user_id
        }
        
        app_id = self.db_manager.save_job_application(company_info, ats_score=88)
        
        # Verify job application was created
        self.assertIsInstance(app_id, int)
        self.assertGreater(app_id, 0)
        
        # Verify job application can be retrieved
        application = self.db_manager.get_application_by_id(app_id)
        self.assertIsNotNone(application)
        self.assertEqual(application['company_name'], 'Workflow Company')
        self.assertEqual(application['user_id'], user_id)
        
        # Verify user's applications can be retrieved
        user_applications = self.db_manager.get_applications_by_user(user_id)
        self.assertEqual(len(user_applications), 1)
        self.assertEqual(user_applications[0]['application_id'], app_id)
    
    def test_user_email_case_insensitive(self):
        """Test that email lookup is case insensitive"""
        user_data = {
            'username': 'caseuser',
            'email': 'CaseTest@Example.COM',
            'password_hash': 'secure_hash_789'
        }
        
        user_id = self.db_manager.create_user(user_data)
        
        # Should find user with lowercase email
        user_lower = self.db_manager.get_user_by_email('casetest@example.com')
        self.assertIsNotNone(user_lower)
        self.assertEqual(user_lower['user_id'], user_id)
        
        # Should find user with mixed case email
        user_mixed = self.db_manager.get_user_by_email('CaseTest@Example.COM')
        self.assertIsNotNone(user_mixed)
        self.assertEqual(user_mixed['user_id'], user_id)
    
    def test_user_lifecycle_operations(self):
        """Test complete user lifecycle: create, login, deactivate"""
        user_data = {
            'username': 'lifecycleuser',
            'email': 'lifecycle@example.com',
            'password_hash': 'secure_hash_000'
        }
        
        user_id = self.db_manager.create_user(user_data)
        
        # Initially, last_login should be None
        user = self.db_manager.get_user_by_id(user_id)
        self.assertIsNone(user['last_login'])
        
        # Update last login
        self.db_manager.update_last_login(user_id)
        user = self.db_manager.get_user_by_id(user_id)
        self.assertIsNotNone(user['last_login'])
        
        # User should be active
        self.assertTrue(user['is_active'])
        
        # Deactivate user
        self.db_manager.deactivate_user(user_id)
        user = self.db_manager.get_user_by_id(user_id)
        self.assertFalse(user['is_active'])


@pytest.mark.e2e
class TestDatabaseManagerReal(unittest.TestCase):
    """Real tests for the DatabaseManager"""
    
    @classmethod
    def setUpClass(cls):
        """Set up real test database"""
        cls.real_test_dir = tempfile.mkdtemp(prefix='real_db_test_')
        cls.real_db_path = os.path.join(cls.real_test_dir, 'real_test.db')
        cls.db_manager = DatabaseManager(cls.real_db_path)
    
    @classmethod
    def tearDownClass(cls):
        """Clean up real test database"""
        shutil.rmtree(cls.real_test_dir, ignore_errors=True)
    
    def test_concurrent_user_creation(self):
        """Test concurrent user creation"""
        results = []
        errors = []
        
        def create_user_worker(worker_id):
            try:
                user_data = {
                    'username': f'concurrent_user_{worker_id}_{int(time.time()*1000)}',
                    'email': f'concurrent_{worker_id}_{int(time.time()*1000)}@example.com',
                    'password_hash': f'hash_{worker_id}'
                }
                user_id = self.db_manager.create_user(user_data)
                results.append(user_id)
            except Exception as e:
                errors.append(str(e))
        
        # Create multiple threads to create users concurrently
        threads = []
        for i in range(10):
            thread = threading.Thread(target=create_user_worker, args=(i,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # Verify results
        self.assertEqual(len(errors), 0, f"No errors should occur: {errors}")
        self.assertEqual(len(results), 10, "All user creations should succeed")
        self.assertEqual(len(set(results)), 10, "All user IDs should be unique")
    
    def test_user_data_integrity(self):
        """Test user data integrity with edge cases"""
        # Test with special characters
        user_data = {
            'username': 'special_user_àáâã',
            'email': 'special.user+test@example.com',
            'password_hash': 'complex_hash_!@#$%^&*()',
            'first_name': 'José María',
            'last_name': "O'Connor-Smith"
        }
        
        user_id = self.db_manager.create_user(user_data)
        retrieved_user = self.db_manager.get_user_by_id(user_id)
        
        self.assertEqual(retrieved_user['username'], 'special_user_àáâã')
        self.assertEqual(retrieved_user['first_name'], 'José María')
        self.assertEqual(retrieved_user['last_name'], "O'Connor-Smith")

# Usage example

# pytest src/test/unit/db_operations/database_tests.py -m e2e -xsvv