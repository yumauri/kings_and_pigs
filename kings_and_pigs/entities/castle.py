import os
import glob
from .chamber import Chamber


maps_location = "kings_and_pigs/data/maps"


class Castle:
    def __init__(self):
        self.chambers, self.chamber = self.load_chambers(maps_location)
        self.next_chamber = None
        self.prev_chamber = None
        self.next_door = None
        self.prev_door = None

    def load_chambers(self, path):
        chambers = {}

        # find all maps files and fill the dict {name->chamber}
        file_names = sorted(glob.glob(f"{path}/*.tmx"))
        initial, dead_end = None, None
        for file_name in file_names:
            chamber = Chamber(file_name)
            name = os.path.basename(file_name)[:-4]
            if initial is None:
                initial = name
            dead_end = name
            chambers[name] = chamber

        # connect all doors (visible and invisible ones)
        for name, chamber in chambers.items():
            for door in [*chamber.doors, *chamber.invisible_doors]:
                if door.type is not None and door.type in chambers:
                    destination = chambers[door.type]
                    door.chamber = destination
                    for backdoor in [*destination.doors, *destination.invisible_doors]:
                        if backdoor.type is not None and backdoor.type == name:
                            backdoor.backdoor = door
                elif name != dead_end:
                    destination = chambers[dead_end]
                    door.chamber = destination

        # return connected chambers
        return chambers, chambers[initial]

    def use_door(self, door):
        if door.chamber is not None:
            self.next_chamber = door.chamber
        else:
            self.next_chamber = self.prev_chamber

        self.prev_chamber = self.chamber

        if door.backdoor is not None:
            self.next_door = door.backdoor
        elif self.prev_door is not None and self.prev_door in [
            *self.next_chamber.doors,
            *self.next_chamber.invisible_doors,
        ]:
            self.next_door = self.prev_door
        else:
            self.next_door = self.next_chamber.doors.sprites()[0]

        self.prev_door = door

    def swap_chamber(self):
        self.chamber = self.next_chamber
        return self.next_door
