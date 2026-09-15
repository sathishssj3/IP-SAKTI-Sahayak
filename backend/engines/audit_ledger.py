"""
IP-SAKTI Sahayak: DPDP 2023 Hash-Chained Cryptographic Audit Ledger
Maintains an immutable, tamper-evident SHA-256 chain of regulatory queries,
retrieved statutory citations, confidence metrics, and anonymized session hashes.
"""

import hashlib
import json
import time
from typing import Dict, Any, List, Optional
from pydantic import BaseModel


class AuditBlock(BaseModel):
    block_index: int
    timestamp: float
    query_hash: str
    citations_bound: List[str]
    confidence_score: float
    previous_hash: str
    current_hash: str


class AuditLedger:
    def __init__(self):
        self.chain: List[AuditBlock] = []
        self._create_genesis_block()

    def _calculate_hash(
        self,
        block_index: int,
        timestamp: float,
        query_hash: str,
        citations_bound: List[str],
        confidence_score: float,
        previous_hash: str
    ) -> str:
        payload = f"{block_index}|{timestamp:.4f}|{query_hash}|{','.join(sorted(citations_bound))}|{confidence_score:.2f}|{previous_hash}"
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()

    def _create_genesis_block(self):
        genesis_prev = "0" * 64
        genesis_hash = self._calculate_hash(0, 0.0, "GENESIS_BLOCK", ["GENESIS"], 1.0, genesis_prev)
        block = AuditBlock(
            block_index=0,
            timestamp=0.0,
            query_hash="GENESIS_BLOCK",
            citations_bound=["GENESIS"],
            confidence_score=1.0,
            previous_hash=genesis_prev,
            current_hash=genesis_hash
        )
        self.chain.append(block)

    def record_query(
        self,
        query: str,
        citations: List[str],
        confidence_score: float
    ) -> AuditBlock:
        # Anonymize query per DPDP 2023
        query_hash = hashlib.sha256(query.strip().lower().encode("utf-8")).hexdigest()
        last_block = self.chain[-1]
        new_index = last_block.block_index + 1
        now = time.time()
        
        curr_hash = self._calculate_hash(
            new_index,
            now,
            query_hash,
            citations,
            confidence_score,
            last_block.current_hash
        )

        block = AuditBlock(
            block_index=new_index,
            timestamp=now,
            query_hash=query_hash,
            citations_bound=citations,
            confidence_score=confidence_score,
            previous_hash=last_block.current_hash,
            current_hash=curr_hash
        )
        self.chain.append(block)
        return block

    def verify_chain_integrity(self) -> bool:
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            if curr.previous_hash != prev.current_hash:
                return False

            recalculated = self._calculate_hash(
                curr.block_index,
                curr.timestamp,
                curr.query_hash,
                curr.citations_bound,
                curr.confidence_score,
                curr.previous_hash
            )
            if recalculated != curr.current_hash:
                return False

        return True


AUDIT_LEDGER = AuditLedger()
