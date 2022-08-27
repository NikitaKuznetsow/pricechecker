from dataclasses import dataclass


@dataclass
class Item:
    title: str
    links_image: list
    brand: str
    desc: str
    price: int
    link: str
    rating: float
    review_count: int