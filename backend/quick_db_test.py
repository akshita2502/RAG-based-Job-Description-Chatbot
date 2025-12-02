"""
Quick Database Connection Test
A simpler, faster version for quick diagnostics.

Usage:
    python quick_db_test.py
"""

import sys
import os
from pathlib import Path

# Add backend directory to path
sys.path.insert(0, str(Path(__file__).parent))

def quick_test():
    print("🔍 Quick Database Connection Test\n")
    
    # Test 1: Configuration
    print("1️⃣  Checking configuration...")
    try:
        from app.core.config import settings
        print(f"   ✅ Config loaded: {settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}")
        print(f"password is {settings.POSTGRES_PASSWORD}")
    except Exception as e:
        print(f"   ❌ Config failed: {e}")
        return False
    
    # Test 2: Direct connection
    print("2️⃣  Testing direct connection...")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            database=settings.POSTGRES_DB
        )
        
        conn.close()
        print(f"   ✅ Connected successfully")
    except Exception as e:
        print(f"   ❌ Connection failed: {e}")
        return False
    
    # Test 3: SQLAlchemy
    print("3️⃣  Testing SQLAlchemy...")
    try:
        from sqlalchemy import create_engine, text
        from sqlalchemy.pool import NullPool
        
        # Build connection string for sync driver
        DATABASE_URL = (
            f"postgresql+psycopg2://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}"
            f"@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"
        )
        
        # Create engine with NullPool to avoid greenlet/asyncpg issues
        engine = create_engine(DATABASE_URL, poolclass=NullPool, echo=False)
        
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
            connection.commit()
        
        engine.dispose()
        print(f"   ✅ SQLAlchemy works")
    except Exception as e:
        print(f"   ❌ SQLAlchemy failed: {e}")
        print(f"\n   💡 Tip: Make sure you're using the sync driver (postgresql+psycopg2)")
        return False
    
    print("\n✅ All tests passed! Database is ready.\n")
    return True

if __name__ == "__main__":
    success = quick_test()
    sys.exit(0 if success else 1)
