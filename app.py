import os
import subprocess
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status, BackgroundTasks
from fastapi.security import HTTPBasic, HTTPBasicCredentials

test_runner_username = os.environ["TEST_RUNNER_USERNAME"]
test_runner_password = os.environ["TEST_RUNNER_PASSWORD"]
test_runner_tests_path = os.environ["TEST_RUNNER_TESTS_PATH"]


app = FastAPI()
security = HTTPBasic()


def run_tests():
    res = subprocess.run(
        ["sh", "run-tests.sh"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=test_runner_tests_path,
    )
    with open("data/results.txt", "ab") as fd:
        fd.write(res.stdout)


@app.post("/submit")
async def submit(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    tasks: BackgroundTasks,
):
    if (
        credentials.username != test_runner_username
        or credentials.password != test_runner_password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    tasks.add_task(run_tests)
    return {"message": "this too shall pass"}
