from msgflow.memory import DialogMemory


def test_context_memory():
    memory = DialogMemory()

    memory.add("user1", "message1")
    memory.add("user1", "message2")
    memory.add("user2", "message3")

    assert memory.get("user1") == ["message1", "message2"]
    assert memory.get("user2") == ["message3"]
    assert memory.get("user3") == []


def test_context_memory_max_history():
    memory = DialogMemory(max_history=1)

    memory.add("user1", "message1")
    memory.add("user1", "message2")
    memory.add("user2", "message3")

    assert memory.get("user1") == ["message2"]
    assert memory.get("user2") == ["message3"]
    assert memory.get("user3") == []


def test_context_memory_clear():
    memory = DialogMemory()

    memory.add("user1", "message1")
    memory.add("user1", "message2")
    memory.add("user2", "message3")

    memory.clear("user1")
    memory.clear("user4")  # Case when the id is not registered yet

    assert memory.get("user1") == []
    assert memory.get("user2") == ["message3"]
    assert memory.get("user3") == []
