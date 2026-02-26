"""
Firebase Manager for ASES
Handles all Firestore operations with robust error handling
"""
import logging
from typing import Dict, Any, List, Optional, Union
import firebase_admin
from firebase_admin import credentials, firestore, exceptions
from google.cloud.firestore_v1.base_query import FieldFilter
from datetime import datetime, timedelta
import json
import traceback

from ases_config import config

logger = logging.getLogger(__name__)

class FirebaseManager:
    """Manages Firebase Firestore operations for ASES"""
    
    def __init__(self):
        """Initialize Firebase connection"""
        self.db = None
        self._initialize_firebase()
        
    def _initialize_firebase(self) -> None:
        """Initialize Firebase app with error handling"""
        try:
            # Check if already initialized
            if not firebase_admin._apps:
                cred_path = config.firebase.credential_path
                if not os.path.exists(cred_path):
                    raise FileNotFoundError(
                        f"Firebase credentials not found at {cred_path}. "
                        "Please download serviceAccountKey.json from Firebase Console."
                    )
                
                cred = credentials.Certificate(cred_path)
                firebase_admin.initialize_app(cred, {
                    'projectId': config.firebase.project_id
                })
                logger.info("Firebase initialized successfully")
            
            self.db = firestore.client()
            
        except exceptions.FirebaseError as e:
            logger.error(f"Firebase initialization failed: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error during Firebase init: {str(e)}")
            raise
    
    def get_collection(self, entity_name: str):
        """Get Firestore collection reference"""
        collection_name = config.firebase.get_collection_name(entity_name)
        return self.db.collection(collection_name)
    
    def save_strategy(self, strategy_data: Dict[str, Any]) -> Optional[str]:
        """Save a trading strategy to Firestore"""
        try:
            # Validate required fields