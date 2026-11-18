#!/usr/bin/env python3

from pydantic import BaseModel, Field, ValidationError, NaiveDatetime, \
    TypeAdapter


class SpaceStation(BaseModel):
    station_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=1, max_length=50)
    crew_size: int = Field(..., ge=1, le=20)
    power_level: float = Field(..., ge=0.0, le=100.0)
    oxygen_level: float = Field(..., gt=0.0, le=100.0)
    last_maintenance: NaiveDatetime
    is_operational: bool = Field(True)
    notes: str | None = Field(max_length=200)


def main() -> None:
    print("Space Station Sata Validation")
    print("========================================")

    try:
        station2 = SpaceStation(station_id="ISS001",
                                name="International Space Station",
                                crew_size=6,
                                power_level=85.5,
                                oxygen_level=92.3,
                                last_maintenance=TypeAdapter(NaiveDatetime).
                                validate_python("2026-11-17T23:27:00"),
                                is_operational=True,
                                notes=None)
    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print("Valid station createad:")
    print(f"ID: {station2.station_id}")
    print(f"Name: {station2.name}")
    print(f"Crew: {station2.crew_size} people")
    print(f"Power: {station2.power_level:.1f}%")
    print(f"Oxygen: {station2.oxygen_level:.1f}%")
    print(f"Status: {'Operational' if station2.is_operational is True else
                     'Inoperational'}"
          )

    print("\n========================================")
    print("Excpected validation error:")
    try:
        station2 = SpaceStation(station_id="ISS001",
                                name="International Space Station",
                                crew_size=23,
                                power_level=85.5,
                                oxygen_level=92.3,
                                last_maintenance=TypeAdapter(NaiveDatetime).
                                validate_python("2026-11-17 23:27:00"),
                                is_operational=True,
                                notes=None)
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
