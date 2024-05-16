# coding: utf-8

"""
    Pieces Isomorphic OpenAPI

    Endpoints for Assets, Formats, Users, Asset, Format, User.

    The version of the OpenAPI document: 1.0
    Contact: tsavo@pieces.app
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Optional
from pydantic import BaseModel

class SeededTrackedAssetsEventMetadata(BaseModel):
    """
    Additional Metadata as Neeeded i.e. Search + Query, etc  # noqa: E501
    """
    search: Optional[TrackedAssetsEventSearchMetadata] = None
    __properties = ["search"]

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> SeededTrackedAssetsEventMetadata:
        """Create an instance of SeededTrackedAssetsEventMetadata from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of search
        if self.search:
            _dict['search'] = self.search.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> SeededTrackedAssetsEventMetadata:
        """Create an instance of SeededTrackedAssetsEventMetadata from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return SeededTrackedAssetsEventMetadata.parse_obj(obj)

        _obj = SeededTrackedAssetsEventMetadata.parse_obj({
            "search": TrackedAssetsEventSearchMetadata.from_dict(obj.get("search")) if obj.get("search") is not None else None
        })
        return _obj

from pieces_os_client.models.tracked_assets_event_search_metadata import TrackedAssetsEventSearchMetadata
SeededTrackedAssetsEventMetadata.update_forward_refs()

