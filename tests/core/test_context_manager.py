import unittest
from core.context_manager import ContextManager


class TestContextManager(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.context_manager = ContextManager()

    def test_init(self):
        """Test ContextManager initialization."""
        self.assertEqual(len(self.context_manager), 0)
        self.assertFalse('any_key' in self.context_manager)

    def test_add_single_value(self):
        """Test adding a single value to context."""
        self.context_manager.add('key1', 'value1')
        self.assertEqual(self.context_manager.get('key1'), 'value1')
        self.assertEqual(self.context_manager.get_history('key1'), ['value1'])

    def test_add_multiple_values(self):
        """Test adding multiple values to the same key."""
        self.context_manager.add('key1', 'value1')
        self.context_manager.add('key1', 'value2')
        self.context_manager.add('key1', 'value3')
        
        self.assertEqual(self.context_manager.get('key1'), 'value3')
        self.assertEqual(self.context_manager.get_history('key1'), ['value1', 'value2', 'value3'])

    def test_get_nonexistent_key(self):
        """Test getting a value for a key that doesn't exist."""
        self.assertIsNone(self.context_manager.get('nonexistent'))
        self.assertEqual(self.context_manager.get('nonexistent', 'default'), 'default')

    def test_get_history_nonexistent_key(self):
        """Test getting history for a key that doesn't exist."""
        self.assertEqual(self.context_manager.get_history('nonexistent'), [])

    def test_set_new_key(self):
        """Test setting a value for a new key."""
        self.context_manager.set('key1', 'value1')
        self.assertEqual(self.context_manager.get('key1'), 'value1')
        self.assertEqual(self.context_manager.get_history('key1'), ['value1'])

    def test_set_existing_key_overwrites_history(self):
        """Test that set() overwrites the entire history for a key."""
        self.context_manager.add('key1', 'value1')
        self.context_manager.add('key1', 'value2')
        self.context_manager.set('key1', 'new_value')
        
        self.assertEqual(self.context_manager.get('key1'), 'new_value')
        self.assertEqual(self.context_manager.get_history('key1'), ['new_value'])

    def test_update_multiple_keys(self):
        """Test updating multiple keys using update()."""
        data = {'key1': 'value1', 'key2': 'value2'}
        self.context_manager.update(data)
        
        self.assertEqual(self.context_manager.get('key1'), 'value1')
        self.assertEqual(self.context_manager.get('key2'), 'value2')
        self.assertEqual(self.context_manager.get_history('key1'), ['value1'])
        self.assertEqual(self.context_manager.get_history('key2'), ['value2'])

    def test_update_overwrites_existing_history(self):
        """Test that update() overwrites existing history for keys."""
        self.context_manager.add('key1', 'old_value1')
        self.context_manager.add('key1', 'old_value2')
        
        data = {'key1': 'new_value1', 'key2': 'new_value2'}
        self.context_manager.update(data)
        
        self.assertEqual(self.context_manager.get('key1'), 'new_value1')
        self.assertEqual(self.context_manager.get_history('key1'), ['new_value1'])

    def test_clear(self):
        """Test clearing all context data."""
        self.context_manager.add('key1', 'value1')
        self.context_manager.add('key2', 'value2')
        
        self.context_manager.clear()
        
        self.assertEqual(len(self.context_manager), 0)
        self.assertIsNone(self.context_manager.get('key1'))
        self.assertEqual(self.context_manager.get_history('key1'), [])

    def test_keys(self):
        """Test getting all keys in the context."""
        self.context_manager.add('key1', 'value1')
        self.context_manager.add('key2', 'value2')
        
        keys = list(self.context_manager.keys())
        self.assertIn('key1', keys)
        self.assertIn('key2', keys)
        self.assertEqual(len(keys), 2)

    def test_items(self):
        """Test getting all key-value pairs (most recent values only)."""
        self.context_manager.add('key1', 'value1')
        self.context_manager.add('key1', 'value2')
        self.context_manager.add('key2', 'value3')
        
        items = dict(self.context_manager.items())
        self.assertEqual(items['key1'], 'value2')
        self.assertEqual(items['key2'], 'value3')

    def test_contains(self):
        """Test checking if a key exists in the context."""
        self.context_manager.add('key1', 'value1')
        
        self.assertTrue('key1' in self.context_manager)
        self.assertFalse('nonexistent' in self.context_manager)

    def test_len(self):
        """Test getting the number of keys in the context."""
        self.assertEqual(len(self.context_manager), 0)
        
        self.context_manager.add('key1', 'value1')
        self.assertEqual(len(self.context_manager), 1)
        
        self.context_manager.add('key1', 'value2')
        self.assertEqual(len(self.context_manager), 1)  # Same key, so length stays 1
        
        self.context_manager.add('key2', 'value3')
        self.assertEqual(len(self.context_manager), 2)

    def test_mixed_operations(self):
        """Test a combination of operations to ensure they work together correctly."""
        # Add some initial values
        self.context_manager.add('key1', 'initial')
        self.context_manager.add('key1', 'second')
        self.context_manager.add('key2', 'other')
        
        # Set a new value (should overwrite history)
        self.context_manager.set('key1', 'reset')
        
        # Add more values
        self.context_manager.add('key1', 'after_reset')
        self.context_manager.add('key3', 'new_key')
        
        # Verify final state
        self.assertEqual(self.context_manager.get('key1'), 'after_reset')
        self.assertEqual(self.context_manager.get_history('key1'), ['reset', 'after_reset'])
        self.assertEqual(self.context_manager.get('key2'), 'other')
        self.assertEqual(self.context_manager.get_history('key2'), ['other'])
        self.assertEqual(self.context_manager.get('key3'), 'new_key')
        self.assertEqual(self.context_manager.get_history('key3'), ['new_key'])

    def test_backward_compatibility(self):
        """Test that existing usage patterns still work."""
        # Test the original set/get pattern
        self.context_manager.set('config', {'setting': 'value'})
        config = self.context_manager.get('config')
        self.assertEqual(config['setting'], 'value')
        
        # Test update pattern
        self.context_manager.update({'status': 'running', 'count': 42})
        self.assertEqual(self.context_manager.get('status'), 'running')
        self.assertEqual(self.context_manager.get('count'), 42)


if __name__ == '__main__':
    unittest.main()