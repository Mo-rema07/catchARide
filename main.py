from fastapi import FastAPI, HTTPException, Query
from sqlmodel import select

from db import *
from models import TripRequest

create_db_and_tables()

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Welcome to Catch A Ride!"}


@app.post("/trip")
async def request_trip(trip_req: TripRequest, session: SessionDep):
    session.add(trip_req)
    session.commit()
    session.refresh(trip_req)
    return {
        "message": "your trip has been requested!",
        "trip": trip_req
    }


@app.get("/trip/{trip_req_id}")
async def show_trip_request(trip_req_id: int, session: SessionDep) -> TripRequest:
    trip_req = session.get(TripRequest, trip_req_id)
    if not trip_req:
        raise HTTPException(status_code=404, detail="Trip Request not found")
    return trip_req


@app.patch("/trip/{trip_req_id}")
async def accept_trip_request(trip_req_id: int, session: SessionDep):
    trip_req = session.get(TripRequest, trip_req_id)

    if not trip_req:
        raise HTTPException(status_code=404, detail="Trip Request not found")

    if not trip_req.accepted:
        trip_req_update = trip_req
        trip_req_update.accepted = True
        trip_req.sqlmodel_update(trip_req_update)
        session.add(trip_req)
        session.commit()
        session.refresh(trip_req)
        return {
            "message": f"Trip #{trip_req.id} has just been accepted!",
            "trip": trip_req
        }
    return {
        "message": f"Trip #{trip_req.id} has already been accepted!",
        "trip": trip_req
    }


@app.get("/trips/requested")
async def show_trip_requests(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100,
                             ) -> list[TripRequest]:
    trip_requests = session.exec(select(TripRequest).offset(offset).limit(limit)).all()
    return trip_requests


@app.get("/trips/accepted")
async def show_trip_requests(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100,
                             ) -> list[TripRequest]:
    trip_requests = session.exec(
        select(TripRequest).where(TripRequest.accepted == True).offset(offset).limit(limit)).all()
    return trip_requests


@app.get("/trips/not_accepted")
async def show_trip_requests(session: SessionDep, offset: int = 0, limit: Annotated[int, Query(le=100)] = 100,
                             ) -> list[TripRequest]:
    trip_requests = session.exec(
        select(TripRequest).where(TripRequest.accepted == False).offset(offset).limit(limit)).all()
    return trip_requests
