class Auth:
    _instance = None

    def __new__(cls, token: str = "", expires_in: int = 0):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.token = token
            cls._instance.expires_in = expires_in
        return cls._instance

    def update(self, token: str, expires_in: int):
        self.token = token
        self.expires_in = expires_in

    def __repr__(self):
        return f"<Auth token='{self.token[:6]}...' expires_in={self.expires_in}>"
