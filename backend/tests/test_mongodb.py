from src.database.mongodb_client import get_mongodb_client, get_collection

def test_mongodb_connection():
    """Test that we can connect to MongoDB"""
    client = get_mongodb_client()
    assert client is not None
    
def test_get_collection():
    """Test that we can get the specified collection"""
    collection = get_collection()
    assert collection is not None