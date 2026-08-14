# app/services/blockchain.py
import random
import hashlib
from datetime import datetime
from typing import Optional, Dict, List
import logging

logger = logging.getLogger(__name__)


class BlockchainService:
    """
    Blockchain service for Digital Twin Farmer.
    Handles digital identity creation, smart contracts, and transaction logging.
    """
    
    def __init__(self):
        self.blockchain = "celo"  # Using Celo blockchain
        self.network = "alfajores"  # Testnet
        
    def create_digital_identity(
        self,
        farmer_id: int,
        national_id: str,
        farmer_name: str,
        district: str,
        gps_coordinates: Optional[Dict] = None
    ) -> Dict:
        """
        Create a Soulbound Token (SBT) identity for a farmer.
        """
        # Generate wallet address (simulated)
        wallet_address = self._generate_wallet_address(national_id)
        
        # Generate token ID
        token_id = self._generate_token_id(farmer_id, national_id)
        
        # Generate transaction hash
        transaction_hash = self._generate_transaction_hash(farmer_id, token_id)
        
        logger.info(f"Digital identity created for farmer {farmer_id}")
        
        return {
            "farmer_id": farmer_id,
            "wallet_address": wallet_address,
            "token_id": token_id,
            "blockchain": self.blockchain,
            "network": self.network,
            "transaction_hash": transaction_hash,
            "block_number": random.randint(1000000, 9999999),
            "created_at": datetime.now().isoformat(),
            "is_verified": True,
            "token_uri": f"ipfs://Qm{token_id[:44]}",
            "metadata": {
                "farmer_name": farmer_name,
                "national_id": national_id[-4:],  # Last 4 digits only
                "district": district,
                "gps": gps_coordinates or {"lat": 0, "lng": 0},
                "token_type": "Soulbound Token (SBT)",
                "non_transferable": True
            }
        }
    
    def create_smart_contract(
        self,
        loan_id: int,
        farmer_id: int,
        lender_id: int,
        amount: float,
        crop_type: str,
        expected_yield: float,
        repayment_date: str
    ) -> Dict:
        """
        Create a smart contract for a loan.
        """
        contract_address = self._generate_contract_address(loan_id, farmer_id)
        transaction_hash = self._generate_transaction_hash(loan_id, contract_address)
        
        logger.info(f"Smart contract created for loan {loan_id}")
        
        return {
            "contract_address": contract_address,
            "loan_id": loan_id,
            "farmer_id": farmer_id,
            "lender_id": lender_id,
            "amount": amount,
            "crop_type": crop_type,
            "expected_yield": expected_yield,
            "repayment_date": repayment_date,
            "blockchain": self.blockchain,
            "transaction_hash": transaction_hash,
            "block_number": random.randint(1000000, 9999999),
            "status": "active",
            "created_at": datetime.now().isoformat(),
            "terms": {
                "interest_rate": 0.08,  # 8%
                "repayment_type": "harvest_settlement",
                "grace_period_days": 30,
                "penalty_rate": 0.02
            }
        }
    
    def record_harvest_settlement(
        self,
        loan_id: int,
        actual_yield: float,
        repayment_amount: float,
        surplus_amount: float
    ) -> Dict:
        """
        Record harvest settlement on blockchain.
        """
        transaction_hash = self._generate_transaction_hash(loan_id, "harvest")
        
        logger.info(f"Harvest settlement recorded for loan {loan_id}")
        
        return {
            "loan_id": loan_id,
            "transaction_hash": transaction_hash,
            "block_number": random.randint(1000000, 9999999),
            "actual_yield": actual_yield,
            "repayment_amount": repayment_amount,
            "surplus_amount": surplus_amount,
            "settlement_date": datetime.now().isoformat(),
            "status": "completed",
            "verified": True
        }
    
    def get_identity_status(self, wallet_address: str) -> Dict:
        """
        Get the status of a digital identity.
        """
        return {
            "wallet_address": wallet_address,
            "is_verified": True,
            "blockchain": self.blockchain,
            "network": self.network,
            "last_updated": datetime.now().isoformat(),
            "status": "active"
        }
    
    def _generate_wallet_address(self, seed: str) -> str:
        """Generate a simulated wallet address"""
        hash_obj = hashlib.sha256(seed.encode())
        return f"0x{hash_obj.hexdigest()[:40]}"
    
    def _generate_token_id(self, farmer_id: int, national_id: str) -> str:
        """Generate a unique token ID"""
        raw = f"{farmer_id}{national_id}{datetime.now().timestamp()}"
        hash_obj = hashlib.sha256(raw.encode())
        return f"DTF-{hash_obj.hexdigest()[:12].upper()}"
    
    def _generate_transaction_hash(self, *args) -> str:
        """Generate a simulated transaction hash"""
        raw = "".join(str(a) for a in args)
        hash_obj = hashlib.sha256(raw.encode())
        return f"0x{hash_obj.hexdigest()[:64]}"
    
    def _generate_contract_address(self, loan_id: int, farmer_id: int) -> str:
        """Generate a simulated contract address"""
        raw = f"contract_{loan_id}_{farmer_id}_{datetime.now().timestamp()}"
        hash_obj = hashlib.sha256(raw.encode())
        return f"0x{hash_obj.hexdigest()[:40]}"