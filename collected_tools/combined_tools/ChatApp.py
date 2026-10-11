from BaseEnv import BaseEnv

class ChatApp(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.users = self.parameters.get("users", [
            {"name": "alice", "last_chat_time": "2024-06-01T10:00:00"},
            {"name": "bob", "last_chat_time": "2024-06-02T12:00:00"},
            {"name": "carol", "last_chat_time": "2024-06-03T09:00:00"}
        ])
        self.chats = self.parameters.get("chats", [])
        # Each chat: {"from": "alice", "to": "bob", "content": "hi", "time": "2024-06-01T10:00:00"}

    def filter_users(self, *, last_chat_time_earlier=None):
        if last_chat_time_earlier is None:
            return {"success": True, "data": {"users": self.users}}
        filtered = []
        for user in self.users:
            if user.get("last_chat_time", "") < last_chat_time_earlier:
                filtered.append(user)
        return {"success": True, "data": {"users": filtered}}

    def delete_users(self, *, names):
        if not isinstance(names, list):
            return {"success": False, "message": "names must be a list"}
        before_count = len(self.users)
        self.users = [u for u in self.users if u.get("name") not in names]
        after_count = len(self.users)
        return {"success": True, "message": f"Deleted {before_count - after_count} users."}

    def send_message(self, *, user_name, content):
        if not any(u.get("name") == user_name for u in self.users):
            return {"success": False, "message": f"User {user_name} not found."}
        msg = {
            "from": "system",
            "to": user_name,
            "content": content,
            "time": "2024-06-04T12:00:00"
        }
        self.chats.append(msg)
        for user in self.users:
            if user.get("name") == user_name:
                user["last_chat_time"] = msg["time"]
        return {"success": True, "message": "Message sent."}

    def retrieve_chat_history(self, *, user_1, user_2):
        history = []
        for chat in self.chats:
            if ((chat.get("from") == user_1 and chat.get("to") == user_2) or
                (chat.get("from") == user_2 and chat.get("to") == user_1)):
                history.append(chat)
        return {"success": True, "data": {"history": history}}