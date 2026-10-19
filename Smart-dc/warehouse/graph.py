
from pathlib import Path

from .models import Location


class WarehouseGraph:
    """
    Graph representation of the distribution center.

    Locations are nodes.
    Aisles/connections are weighted edges.
    """

    def __init__(self):
        self.locations = {}
        self.edges = {}

    def add_location(self, location):
        self.locations[location.location_id] = location
        self.edges.setdefault(location.location_id, [])

    def add_edge(self, location_a, location_b, cost):
        self.edges.setdefault(location_a, [])
        self.edges.setdefault(location_b, [])

        self.edges[location_a].append((location_b, cost))
        self.edges[location_b].append((location_a, cost))

    def get_neighbors(self, location_id):
        return self.edges.get(location_id, [])

    def get_location(self, location_id):
        return self.locations.get(location_id)

    def get_cost(self, start, goal):
        for neighbour, cost in self.edges.get(start, []):
            if neighbour == goal:
                return cost

        return None

    def display(self):
        print("WAREHOUSE GRAPH")
        print("=" * 50)

        for location_id in self.locations:
            print(f"{location_id}: {self.edges.get(location_id, [])}")


def load_warehouse(filename):
    """
    Load warehouse locations and weighted aisle connections
    from a text file.

    File format:

    LOCATION,L01,0,0
    LOCATION,L02,5,0
    EDGE,L01,L02,5
    """

    graph = WarehouseGraph()

    filename = Path(filename)

    with filename.open("r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split(",")

            record_type = parts[0].strip().upper()

            if record_type == "LOCATION":
                location_id = parts[1].strip()
                x = int(parts[2])
                y = int(parts[3])

                graph.add_location(
                    Location(
                        location_id=location_id,
                        x=x,
                        y=y,
                    )
                )

            elif record_type == "EDGE":
                start = parts[1].strip()
                end = parts[2].strip()
                cost = int(parts[3])

                graph.add_edge(start, end, cost)

    return graph


if __name__ == "__main__":
    data_file = Path(__file__).parent.parent / "data" / "warehouse.txt"

    warehouse = load_warehouse(data_file)

    warehouse.display()