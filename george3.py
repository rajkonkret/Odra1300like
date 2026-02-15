import time
import random
from dataclasses import dataclass, field
from typing import List, Dict

# =====================================================
# MODELE SYSTEMOWE
# =====================================================

@dataclass
class User:
    name: str
    account: str
    cpu_used: float = 0.0


@dataclass
class Job:
    id: int
    user: User
    program: str
    cpu_time: float = 0.0
    status: str = "QUEUED"


# =====================================================
# ODRA 1300 SYSTEM (GEORGE-LIKE)
# =====================================================

class Odra1300System:

    def __init__(self):
        self.users: Dict[str, User] = {}
        self.queue: List[Job] = []
        self.completed: List[Job] = []
        self.job_counter = 1
        self.tapes: Dict[str, str] = {}  # symulacja taśm

    # -------------------------------------------------

    def create_user(self, name, account):
        self.users[name] = User(name, account)

    # -------------------------------------------------

    def submit_job(self, username, program_text):
        user = self.users.get(username)
        if not user:
            print("USER NOT FOUND")
            return

        job = Job(self.job_counter, user, program_text)
        self.job_counter += 1

        self.queue.append(job)
        print(f"JOB {job.id} SUBMITTED BY {username}")

    # -------------------------------------------------

    def run_next_job(self):

        if not self.queue:
            print("NO JOBS IN QUEUE")
            return

        job = self.queue.pop(0)
        job.status = "RUNNING"

        print(f"\n=== RUNNING JOB {job.id} ({job.user.name}) ===")

        start = time.time()

        # symulacja kompilacji / wykonania
        execution_time = random.uniform(0.5, 2.0)
        time.sleep(execution_time)

        job.cpu_time = execution_time
        job.user.cpu_used += execution_time
        job.status = "COMPLETED"

        self.completed.append(job)

        print(f"JOB {job.id} COMPLETED")
        print(f"CPU TIME: {execution_time:.2f} sec")

    # -------------------------------------------------

    def operator_console(self):

        print("\nODRA 1300 / GEORGE-3 SYSTEM")
        print("TYPE: STATUS, RUN, USERS, ACCOUNTING, EXIT\n")

        while True:

            cmd = input("OP> ").strip().upper()

            if cmd == "STATUS":
                print("\nQUEUE:")
                for job in self.queue:
                    print(f"JOB {job.id} - {job.user.name} - {job.status}")

            elif cmd == "RUN":
                self.run_next_job()

            elif cmd == "USERS":
                for u in self.users.values():
                    print(f"{u.name} / ACC:{u.account}")

            elif cmd == "ACCOUNTING":
                print("\nCPU USAGE:")
                for u in self.users.values():
                    print(f"{u.name}: {u.cpu_used:.2f} sec")

            elif cmd == "EXIT":
                break

            else:
                print("UNKNOWN COMMAND")


# =====================================================
# DEMO
# =====================================================

if __name__ == "__main__":

    system = Odra1300System()

    system.create_user("KOWALSKI", "ACC01")
    system.create_user("NOWAK", "ACC02")

    system.submit_job("KOWALSKI", "FORTRAN PROGRAM")
    system.submit_job("NOWAK", "COBOL PROGRAM")
    system.submit_job("KOWALSKI", "ALGOL PROGRAM")

    system.operator_console()