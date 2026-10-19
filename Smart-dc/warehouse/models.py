from dataclasses import dataclass
from typing import List


@dataclass
class Location:
    location_id: str
    x: int
    y: int


@dataclass
class Item:
    item_id: str
    name: str
    location_id: str
    quantity: int


@dataclass
class Worker:
    worker_id: str
    name: str
    zone: str
    available: bool


@dataclass
class Order:
    order_id: str
    item_ids: List[str]
    status: str = "Pending"