import json
import pytest
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, mock_open
from typing import Dict, Any

from core.services.user_data_service import UserDataService

class TestUserDataService:
    """Test suite for UserDataService class"""

    @pytest.fixture
    def valid_user_data(self) -> Dict[str, Any]:
        """Fixture providing valid user data"""
        return {
            'applicant_info': {
                'name': 'John Doe',
                'email': 'john.doe@example.com'
            },
            'experience': [],
            'education': []
        }

    @pytest.fixture
    def invalid_user_data(self) -> Dict[str, Any]:
        """Fixture providing invalid user data"""
        return {
            'applicant_info': {
                'name': '',
                'email': 'invalid-email'
            }
        }

    @pytest.fixture
    def temp_data_file(self, valid_user_data):
        """Fixture creating a temporary data file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(valid_user_data, f)
            temp_path = Path(f.name)
        yield temp_path
        temp_path.unlink()

    @pytest.fixture
    def service_with_temp_file(self, temp_data_file):
        """Fixture providing UserDataService with temporary file"""
        return UserDataService(data_path=temp_data_file)

    def test_init_with_default_path(self):
        with patch('core.services.user_data_service.Settings') as mock_settings:
            mock_settings.USER_DATA_PATH = Path('/default/path/data.json')
            service = UserDataService()
            assert service.data_path == Path('/default/path/data.json')

    def test_init_with_custom_path(self):
        custom_path = Path('/custom/path/data.json')
        service = UserDataService(data_path=custom_path)
        assert service.data_path == custom_path

    def test_load_user_data_success(self, service_with_temp_file, valid_user_data):
        with patch.object(service_with_temp_file, '_should_validate', return_value=False):
            result = service_with_temp_file.load_user_data()
            assert result == valid_user_data

    def test_load_user_data_with_validation(self, service_with_temp_file, valid_user_data):
        with patch.object(service_with_temp_file, '_should_validate', return_value=True), \
             patch.object(service_with_temp_file, 'validate_user_data', return_value=True) as mock_validate:
            
            result = service_with_temp_file.load_user_data()
            
            assert result == valid_user_data
            mock_validate.assert_called_once_with(valid_user_data)

    def test_load_user_data_file_not_found(self):
        non_existent_path = Path('/non/existent/path/data.json')
        service = UserDataService(data_path=non_existent_path)
        
        with pytest.raises(FileNotFoundError) as exc_info:
            service.load_user_data()
        
        assert "User data file not found at" in str(exc_info.value)
        assert str(non_existent_path) in str(exc_info.value)

    def test_load_user_data_invalid_json(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{"invalid": json format}')
            temp_path = Path(f.name)
        
        try:
            service = UserDataService(data_path=temp_path)
            with pytest.raises(ValueError) as exc_info:
                service.load_user_data()
            
            assert "Invalid JSON format in user data file" in str(exc_info.value)
        finally:
            temp_path.unlink()

    @patch('core.services.user_data_service.ResumeDataValidator')
    def test_validate_user_data_success(self, mock_validator, valid_user_data):
        mock_validator.is_valid.return_value = True
        service = UserDataService()
        
        result = service.validate_user_data(valid_user_data)
        
        assert result is True
        mock_validator.is_valid.assert_called_once_with({
            'name': 'John Doe',
            'professional_title': 'Sample Title',
            'email': 'john.doe@example.com'
        })

    @patch('core.services.user_data_service.ResumeDataValidator')
    def test_validate_user_data_failure(self, mock_validator, valid_user_data):
        mock_validator.is_valid.return_value = False
        service = UserDataService()
        
        result = service.validate_user_data(valid_user_data)
        
        assert result is False

    @patch('core.services.user_data_service.ResumeDataValidator')
    def test_validate_user_data_missing_applicant_info(self, mock_validator):
        mock_validator.is_valid.return_value = True
        service = UserDataService()
        user_data = {}
        
        result = service.validate_user_data(user_data)
        
        assert result is True
        mock_validator.is_valid.assert_called_once_with({
            'name': '',
            'professional_title': 'Sample Title',
            'email': ''
        })

    @patch('core.services.user_data_service.ResumeDataValidator')
    def test_validate_user_data_partial_applicant_info(self, mock_validator):
        mock_validator.is_valid.return_value = True
        service = UserDataService()
        user_data = {
            'applicant_info': {
                'name': 'Jane Doe'
                # missing email
            }
        }
        
        result = service.validate_user_data(user_data)
        
        assert result is True
        mock_validator.is_valid.assert_called_once_with({
            'name': 'Jane Doe',
            'professional_title': 'Sample Title',
            'email': ''
        })

    @patch('core.services.user_data_service.ResumeDataValidator')
    @patch('core.services.user_data_service.logger')
    def test_validate_user_data_exception_handling(self, mock_logger, mock_validator):
        mock_validator.is_valid.side_effect = Exception("Validation error")
        service = UserDataService()
        
        result = service.validate_user_data({})
        
        assert result is False
        mock_logger.error.assert_called_once_with("User data validation failed: Validation error")


    def test_integration_load_and_validate(self, temp_data_file, valid_user_data):
        service = UserDataService(data_path=temp_data_file)
        
        with patch.object(service, '_should_validate', return_value=True), \
             patch('core.services.user_data_service.ResumeDataValidator') as mock_validator:
            
            mock_validator.is_valid.return_value = True
            
            result = service.load_user_data()
            
            assert result == valid_user_data
            mock_validator.is_valid.assert_called_once()

    def test_integration_load_with_validation_failure(self, temp_data_file):
        service = UserDataService(data_path=temp_data_file)
        
        with patch.object(service, '_should_validate', return_value=True), \
             patch('core.services.user_data_service.ResumeDataValidator') as mock_validator:
            
            mock_validator.is_valid.return_value = False
            
            # The method should still return the data even if validation fails
            result = service.load_user_data()
            
            assert isinstance(result, dict)
            mock_validator.is_valid.assert_called_once()


# Additional test class for edge cases and error scenarios
class TestUserDataServiceEdgeCases:

    def test_load_empty_json_file(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write('{}')
            temp_path = Path(f.name)
        
        try:
            service = UserDataService(data_path=temp_path)
            with patch.object(service, '_should_validate', return_value=False):
                result = service.load_user_data()
                assert result == {}
        finally:
            temp_path.unlink()

    def test_load_json_with_unicode_characters(self):
        unicode_data = {
            'applicant_info': {
                'name': 'José García',
                'email': 'josé@example.com'
            }
        }
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False, encoding='utf-8') as f:
            json.dump(unicode_data, f, ensure_ascii=False)
            temp_path = Path(f.name)
        
        try:
            service = UserDataService(data_path=temp_path)
            with patch.object(service, '_should_validate', return_value=False):
                result = service.load_user_data()
                assert result == unicode_data
        finally:
            temp_path.unlink()