"""Provisional API models pending the authoritative §6.0 contract.

Do not treat these as frozen until the source document containing §6.0 is supplied
and reviewed. Fields are deliberately conservative and versioned for JSON exchange.
"""
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, ConfigDict, Field

class ContractModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

class LocatorSpec(ContractModel):
    strategy: Literal["role", "label", "text", "test_id", "css", "xpath"]
    value: str = Field(min_length=1, max_length=2048)

class ElementFingerprint(ContractModel):
    schema_version: Literal["1.0"] = "1.0"
    tag_name: str = Field(min_length=1, max_length=64)
    text: str = Field(default="", max_length=2000)
    classes: list[str] = Field(default_factory=list, max_length=100)
    attributes: dict[str, str] = Field(default_factory=dict)
    role: str | None = Field(default=None, max_length=128)
    parent_tag: str | None = Field(default=None, max_length=64)
    parent_text: str | None = Field(default=None, max_length=1000)
    x: float | None = None
    y: float | None = None
    width: float | None = Field(default=None, ge=0)
    height: float | None = Field(default=None, ge=0)
    original_locator: LocatorSpec | None = None

class ScoringWeights(ContractModel):
    text: float = Field(default=0.30, ge=0, le=1)
    class_name: float = Field(default=0.20, ge=0, le=1)
    attribute: float = Field(default=0.15, ge=0, le=1)
    position: float = Field(default=0.15, ge=0, le=1)
    parent: float = Field(default=0.10, ge=0, le=1)
    aria_role: float = Field(default=0.10, ge=0, le=1)

    def validate_sum(self) -> "ScoringWeights":
        if abs(sum(self.model_dump().values()) - 1.0) > 1e-8:
            raise ValueError("Scoring weights must sum to 1.0")
        return self

class HealingDecision(ContractModel):
    schema_version: Literal["1.0"] = "1.0"
    status: Literal["candidate", "accepted", "rejected", "ambiguous"]
    old_locator: LocatorSpec
    proposed_locator: LocatorSpec | None = None
    confidence: float = Field(ge=0, le=1)
    runner_up_confidence: float | None = Field(default=None, ge=0, le=1)
    reason: str = Field(min_length=1, max_length=2000)
    requires_human_review: bool = True
