from msgflow.memory import ConversationMemory


def test_context_memory():
    memory = ConversationMemory()

    memory.add("user1", "message1")
    memory.add("user1", "message2")
    memory.add("user2", "message3")

    assert memory.get("user1") == ["message1", "message2"]
    assert memory.get("user2") == ["message3"]
    assert memory.get("user3") == []


def test_context_memory_max_history():
    memory = ConversationMemory(max_history=1)

    memory.add("user1", "message1")
    memory.add("user1", "message2")
    memory.add("user2", "message3")

    assert memory.get("user1") == ["message2"]
    assert memory.get("user2") == ["message3"]
    assert memory.get("user3") == []
