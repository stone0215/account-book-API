class ResponseFormat:
    def true_return(self, data, msg="请求成功"):
        return {
            "status": 1,
            "data": data,
            "msg": msg
        }

    def false_return(self, data, msg="请求失败"):
        return {
            "status": 0,
            "error": data,
            "msg": msg
        }
