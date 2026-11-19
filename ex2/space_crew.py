#!/usr/bin/env python3

from pydantic import BaseModel, Field, model_validator, ValidationError
from enum import StrEnum
from datetime import datetime


class Rank(StrEnum):
    CADET = "cadet"
    OFFICER = "officer"
    LIEUTENANT = "lieutenant"
    CAPTAIN = "captain"
    COMMANDER = "commander"


class CrewMember(BaseModel):
    member_id: str = Field(..., min_length=3, max_length=10)
    name: str = Field(..., min_length=2, max_length=50)
    rank: Rank
    age: int = Field(..., ge=18, le=80)
    specialization: str = Field(..., min_length=3, max_length=30)
    years_experience: int = Field(..., ge=0, le=50)
    is_active: bool = (True)


class SpaceMission(BaseModel):
    mission_id: str = Field(..., min_length=5, max_length=15)
    mission_name: str = Field(..., min_length=3, max_length=100)
    destination: str = Field(..., min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(..., ge=1, le=3650)
    crew: list[CrewMember] = Field(..., min_length=1, max_length=12)
    mission_status: str = Field("planned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode='after')
    def validator(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")
        if (Rank.COMMANDER not in [member.rank for member in self.crew] and
           Rank.CAPTAIN not in [member.rank for member in self.crew]):
            raise ValueError("Mission must have at least one Commander "
                             "or Captain")
        if (self.duration_days > 365 and
           len([member for member in self.crew if
                member.years_experience > 4]) < len(self.crew)/2):
            raise ValueError("Long missions (> 365 days) need 50% "
                             "experienced crew")
        if not all(member.is_active for member in self.crew):
            raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("========================================")

    sara = CrewMember(member_id="C123",
                      name="Sarah Connor",
                      rank=Rank.COMMANDER,
                      age=40,
                      specialization="Mission Command",
                      years_experience=10,
                      is_active=True)

    john = CrewMember(member_id="C234",
                      name="John Smith",
                      rank=Rank.LIEUTENANT,
                      age=40,
                      specialization="Navigation",
                      years_experience=7,
                      is_active=True)

    alice = CrewMember(member_id="C345",
                       name="Alice Jhonson",
                       rank=Rank.OFFICER,
                       age=40,
                       specialization="Engineering",
                       years_experience=4,
                       is_active=True)

    try:
        station2 = SpaceMission(mission_id="M2024_MARS",
                                mission_name="Mars Colony Establishment",
                                destination="Mars",
                                launch_date=datetime(2026, 11, 18, 20, 45),
                                duration_days=900,
                                crew=[sara, john, alice],
                                mission_status="ongoing",
                                budget_millions=2500)
    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print("Valid mission created:")
    print(f"Mission: {station2.mission_name}")
    print(f"ID: {station2.mission_id}")
    print(f"Destination: {station2.destination}")
    print(f"Duration: {station2.duration_days} days")
    print(f"Budget: ${station2.budget_millions}M")
    print(f"Crew size: {len(station2.crew)}")
    print("Crew members:")
    for member in station2.crew:
        print(f"- {member.name} ({member.rank}) - {member.specialization}")

    print("\n========================================")
    print("Excpected validation error:")
    try:
        station2 = SpaceMission(mission_id="M2024_MARS",
                                mission_name="Mars Colony Establishment",
                                destination="Mars",
                                launch_date=datetime(2026, 11, 18, 20, 45),
                                duration_days=900,
                                crew=[john, alice],
                                mission_status="ongoing",
                                budget_millions=2500)
    except ValidationError as e:
        print(e.errors()[0]["msg"][13:])


if __name__ == "__main__":
    main()
