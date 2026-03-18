class MemoryStore:
    def __init__(self):
        self.store = {}

    def add(self, session_id: str, role: str, content: str):
        if not session_id:
            return
        self.store.setdefault(session_id, []).append(
            {"role": role, "content": content}
        )

    def get(self, session_id: str):
        if not session_id:
            return []
        return self.store.get(session_id, [])


memory_store = MemoryStore()