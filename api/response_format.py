# -*- coding: UTF-8 -*-


class ResponseFormat:
    def true_return(self, data, msg="success"):
        return {
            "status": 1,
            "data": data,
            "msg": msg
        }

    def false_return(self, data, msg="fail"):
        return {
            "status": 0,
            "error": data,
            "msg": msg
        }
