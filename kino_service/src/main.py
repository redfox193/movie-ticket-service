from concurrent import futures
import random

import grpc
import generated_code.iticket_pb2_grpc as iticket_pb2_grpc
from generated_code.iticket_pb2 import Film, PremieresResponse, CodeResponse, DatesResponse, UserRequest
from signal import signal, SIGTERM

from db.database import engine, SessionLocal
from db import tables

from datetime import datetime


class GRPCKinoService(
    iticket_pb2_grpc.ITicketServicer
):
    def genCode(self, request, context):

        with SessionLocal() as session:
            random.seed(request.film_id + datetime.now().timestamp())
            new_code = ''.join([str(random.randint(0, 9)) for _ in range(8)])
            session.add(
                tables.Code(code=new_code, film_id=request.film_id)
            )
            session.commit()
        return CodeResponse(code=new_code)

    def getPremieres(self, request, context):
        with SessionLocal() as session:
            films = [Film(id=film.id, name=film.name, cost=film.cost) for film in session.query(tables.Film).all()]
        return PremieresResponse(premieres=films)

    def getDates(self, request, context):
        with SessionLocal() as session:
            film = session.query(tables.Film).get(request.film_id)
            film_dates = [str(info.date) for info in film.dates]
        return DatesResponse(dates=film_dates)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    iticket_pb2_grpc.add_ITicketServicer_to_server(
        GRPCKinoService(), server
    )
    server.add_insecure_port("[::]:50051")
    server.start()

    def handle_sigterm(*_):
        print("Received shutdown signal")
        all_rpcs_done_event = server.stop(30)
        all_rpcs_done_event.wait(30)
        print("Shut down gracefully")

    signal(SIGTERM, handle_sigterm)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
