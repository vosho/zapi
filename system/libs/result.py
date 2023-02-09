from enum import Enum


class ResultStatus(Enum):
    SUCCESS = 1
    FAILURE = 2


class Result(object):
    data: any = None
    status = ResultStatus.SUCCESS
    error = None

    def __init__(self, status: ResultStatus = ResultStatus.SUCCESS, data=dict(), error=None):
        self.data = data
        self.status = status
        self.error = error

    @staticmethod
    def failure(error):
        return Result(status=ResultStatus.FAILURE, error=error)
