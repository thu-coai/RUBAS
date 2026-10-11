from BaseEnv import BaseEnv

class IndoorRobot(BaseEnv):
    def __init__(self, *, parameters=None):
        super().__init__()
        self.parameters = parameters if parameters is not None else {}
        self.rooms = self.parameters.get("rooms", [
            {"id": "room1", "name": "Living Room"},
            {"id": "room2", "name": "Kitchen"},
            {"id": "room3", "name": "Bedroom"}
        ])
        self.current_room_id = self.parameters.get("current_room_id", self.rooms[0]["id"])
        self.objects = self.parameters.get("objects", [
            {"id": "obj1", "name": "Chair", "room_id": "room1"},
            {"id": "obj2", "name": "Table", "room_id": "room1"},
            {"id": "obj3", "name": "Knife", "room_id": "room2"},
            {"id": "obj4", "name": "Orange", "room_id": "room2"}
        ])
        self.people = self.parameters.get("people", [
            {"id": "person1", "name": "Alice", "room_id": "room1"},
            {"id": "person2", "name": "Bob", "room_id": "room2"}
        ])
        self.grabbed_objects = []
        self.last_allowed_operations = {}

    def get_current_state(self):
        grabbed_objs = [obj for obj in self.objects if obj["id"] in self.grabbed_objects]
        return {
            "success": True,
            "data": {
                "current_room_id": self.current_room_id,
                "grabbed_objects": grabbed_objs
            }
        }

    def list_rooms(self):
        return {
            "success": True,
            "data": {
                "rooms": self.rooms
            }
        }

    def go_to_room(self, *, room_id):
        room_ids = [room["id"] for room in self.rooms]
        if room_id not in room_ids:
            return {
                "success": False,
                "message": f"Room {room_id} does not exist."
            }
        self.current_room_id = room_id
        return {
            "success": True,
            "message": f"Moved to room {room_id}."
        }

    def find_objects(self, *, query):
        objs = [
            obj for obj in self.objects
            if obj["room_id"] == self.current_room_id and query.lower() in obj.get("name", "").lower()
        ]
        return {
            "success": True,
            "data": {
                "objects": objs
            }
        }

    def look_around_object(self, 
        *, object_id
    ):
        objs_in_room = [obj for obj in self.objects if obj["room_id"] == self.current_room_id]
        if not any(obj["id"] == object_id for obj in objs_in_room):
            return {
                "success": False,
                "message": f"Object {object_id} not found in current room."
            }
        around_objs = [obj for obj in objs_in_room if obj["id"] != object_id]
        return {
            "success": True,
            "data": {
                "objects_around": around_objs
            }
        }

    def get_allowed_operations(self, *, target_object_id, interact_grabbed_object_ids=None):
        objs_in_room = [obj for obj in self.objects if obj["room_id"] == self.current_room_id]
        if not any(obj["id"] == target_object_id for obj in objs_in_room):
            return {
                "success": False,
                "message": f"Target object {target_object_id} not found in current room."
            }
        allowed_ops = [
            {
                "operation_id": "grab",
                "name": "Grab",
                "arguments": {}
            },
            {
                "operation_id": "place",
                "name": "Place",
                "arguments": {}
            },
            {
                "operation_id": "interact",
                "name": "Interact",
                "arguments": {
                    "tool_object_ids": interact_grabbed_object_ids or []
                }
            }
        ]
        self.last_allowed_operations[target_object_id] = allowed_ops
        return {
            "success": True,
            "data": {
                "allowed_operations": allowed_ops
            }
        }

    def apply_allowed_operation(self, *, target_object_id, operation_id, arguments=None):
        allowed_ops = self.last_allowed_operations.get(target_object_id, [])
        op = next((op for op in allowed_ops if op["operation_id"] == operation_id), None)
        if not op:
            return {
                "success": False,
                "message": "Operation not allowed or not retrieved. Please call get_allowed_operations first."
            }
        if operation_id == "grab":
            if target_object_id in self.grabbed_objects:
                return {
                    "success": False,
                    "message": "Object already grabbed."
                }
            self.grabbed_objects.append(target_object_id)
            return {
                "success": True,
                "message": f"Object {target_object_id} grabbed."
            }
        elif operation_id == "place":
            if target_object_id not in self.grabbed_objects:
                return {
                    "success": False,
                    "message": "Object not grabbed."
                }
            self.grabbed_objects.remove(target_object_id)
            return {
                "success": True,
                "message": f"Object {target_object_id} placed."
            }
        elif operation_id == "interact":
            return {
                "success": True,
                "message": f"Interacted with object {target_object_id} using {arguments.get('tool_object_ids', []) if arguments else []}."
            }
        else:
            return {
                "success": False,
                "message": "Unknown operation."
            }

    def find_people(self, *, query):
        people_in_room = [
            person for person in self.people
            if person["room_id"] == self.current_room_id and query.lower() in person.get("name", "").lower()
        ]
        return {
            "success": True,
            "data": {
                "people": people_in_room
            }
        }

    def hand_objects_to_person(self, *, object_ids, person_id):
        people_in_room = [person for person in self.people if person["room_id"] == self.current_room_id]
        if not any(person["id"] == person_id for person in people_in_room):
            return {
                "success": False,
                "message": "Person not found in current room."
            }
        for oid in object_ids:
            if oid not in self.grabbed_objects:
                return {
                    "success": False,
                    "message": f"Object {oid} is not grabbed."
                }
        for oid in object_ids:
            self.grabbed_objects.remove(oid)
        return {
            "success": True,
            "message": f"Handed objects {object_ids} to person {person_id}."
        }