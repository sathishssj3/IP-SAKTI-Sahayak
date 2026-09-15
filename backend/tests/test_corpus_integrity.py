"""
Unit tests for IP-SAKTI Sahayak Statutory Knowledge Corpus and RAG Chunks
"""

import json
import os
import pytest

DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
KB_PATH = os.path.join(DATA_DIR, "knowledge_base.json")
CHUNKS_PATH = os.path.join(DATA_DIR, "knowledge_base_chunks.jsonl")


def test_knowledge_base_exists_and_valid():
    assert os.path.exists(KB_PATH), f"knowledge_base.json not found at {KB_PATH}"
    with open(KB_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    assert "statutes" in data, "knowledge_base.json must contain 'statutes' key"
    statutes = data["statutes"]
    assert len(statutes) >= 30, f"Expected at least 30 statutes, found {len(statutes)}"

    required_keys = {
        "id", "regime", "act", "section", "amendment_year",
        "in_force", "authority_body", "title", "text", "guidance", "official_link"
    }

    seen_ids = set()
    for s in statutes:
        s_id = s.get("id")
        assert s_id, "Statute must have an id"
        assert s_id not in seen_ids, f"Duplicate statute ID found: {s_id}"
        seen_ids.add(s_id)

        missing = required_keys - set(s.keys())
        assert not missing, f"Statute {s_id} missing keys: {missing}"
        assert s["regime"] in ("national", "international"), f"Invalid regime in {s_id}"
        assert len(s["text"].strip()) > 15, f"Text content empty or too short in {s_id}"
        assert len(s["guidance"].strip()) > 15, f"Guidance empty or too short in {s_id}"
        assert s["official_link"].startswith("http"), f"Invalid link in {s_id}: {s['official_link']}"


def test_coverage_of_all_four_authoritative_sources():
    with open(KB_PATH, "r", encoding="utf-8") as f:
        statutes = json.load(f)["statutes"]

    source_domains = set()
    for s in statutes:
        source_domains.add(s["authority_body"])

    # Verify India Code (Patents Act, BDA, DCA, GI, TM)
    india_code_matches = [s for s in statutes if "patents_act" in s["id"] or "bda_" in s["id"] or "dca_" in s["id"]]
    assert len(india_code_matches) >= 8, "India Code coverage insufficient"

    # Verify IP India (CGPDTM Guidelines GP-1 to GP-6, IPC, GI)
    ipindia_matches = [s for s in statutes if "cgpdtm" in s["id"] or "inpass" in s["id"] or "gi_" in s["id"]]
    assert len(ipindia_matches) >= 6, "IP India coverage insufficient"

    # Verify NBA India (Forms 1-4, ABS Slabs, NTC)
    nba_matches = [s for s in statutes if "nba_" in s["id"]]
    assert len(nba_matches) >= 5, "NBA coverage insufficient"

    # Verify TKDL (Turmeric, Neem, First Schedule texts, Classical formulations)
    tkdl_matches = [s for s in statutes if "tkdl_" in s["id"]]
    assert len(tkdl_matches) >= 4, "TKDL coverage insufficient"


def test_vector_chunks_integrity():
    assert os.path.exists(CHUNKS_PATH), f"knowledge_base_chunks.jsonl not found at {CHUNKS_PATH}"
    with open(CHUNKS_PATH, "r", encoding="utf-8") as f:
        chunks = [json.loads(line) for line in f if line.strip()]

    assert len(chunks) >= 30, f"Expected >= 30 chunks, got {len(chunks)}"
    for c in chunks:
        assert "chunk_id" in c, "Chunk missing chunk_id"
        assert "text" in c and len(c["text"]) > 50, "Chunk text missing or too short"
        assert "metadata" in c, "Chunk missing metadata"
        meta = c["metadata"]
        assert "id" in meta and "act" in meta and "regime" in meta
