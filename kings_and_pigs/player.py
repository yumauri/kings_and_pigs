import os
import glob
import random
import pygame
from .database import Database
from .events import AUTO_NEXT_TRACK


music_location = "kings_and_pigs/data/music"
sounds_location = "kings_and_pigs/data/sounds"


class Player:
    def __init__(self):
        self.use_midi = False
        self.playlist = self.load_playlist(music_location)
        self.sounds = self.load_sounds(sounds_location)
        self.idx = 0
        self.get_volumes()

    def get_volumes(self):
        # by default
        self.volume_music = 0.5
        self.volume_sounds = 0.5
        self.mute_music = False
        self.mute_sounds = False

        # get from database
        db = Database()
        settings = db.get_settings()
        db.close()

        # parse values
        if "volume_music" in settings and settings["volume_music"] is not None:
            self.volume_music = float(settings["volume_music"])
        if "volume_sounds" in settings and settings["volume_sounds"] is not None:
            self.volume_sounds = float(settings["volume_sounds"])
        if "mute_music" in settings and settings["mute_music"] is not None:
            self.mute_music = settings["mute_music"] == "yes"
        if "mute_sounds" in settings and settings["mute_sounds"] is not None:
            self.mute_sounds = settings["mute_sounds"] == "yes"

    def load_playlist(self, path):
        # unfortunately MIDI doesn't support pausing/unpausing :(
        # so, I've converted all of the music to OGG Vorbis format
        # though it has increased file sizes up to x100 times, ouch...
        return glob.glob(f"{path}/*.{'mid' if self.use_midi else 'ogg'}")

    def load_sounds(self, path):
        # find all sound files and fill the dict {name->sound}
        sounds = {}
        file_names = sorted(glob.glob(f"{path}/*.*"))
        for file_name in file_names:
            sound = pygame.mixer.Sound(file_name)
            name = os.path.basename(file_name)[:-4]  # expect 3 symbol extension
            sounds[name] = sound
        return sounds

    def play(self):
        # shuffle music, so each new game it will start from new track
        random.shuffle(self.playlist)
        self.play_next()

    def play_next(self):
        # load first track and queue seconds one
        # pygame.mixer.music allows to queue only one track,
        # so, in order to play more, we need to handle events,
        # and queue tracks one by one, when previous track ends
        pygame.mixer.music.load(self.playlist[self.idx])
        self.queue_next()
        pygame.mixer.music.set_endevent(AUTO_NEXT_TRACK)
        pygame.mixer.music.set_volume(0 if self.mute_music else self.volume_music)
        pygame.mixer.music.play()

    def queue_next(self):
        self.idx = (self.idx + 1) % len(self.playlist)
        pygame.mixer.music.queue(self.playlist[self.idx])

    def pause(self):
        if self.use_midi:
            # pygame mixer doesn't support pausing/unpausing MIDI playback
            pygame.mixer.music.stop()
        else:
            pygame.mixer.music.pause()

    def unpause(self):
        if self.use_midi:
            # pygame mixer doesn't support pausing/unpausing MIDI playback
            pygame.mixer.music.play()
        else:
            pygame.mixer.music.unpause()

    def stop(self):
        pygame.mixer.music.fadeout(2000)
        # pygame.mixer.music.stop()
        # pygame.mixer.music.unload()

    def sound(self, name):
        if name in self.sounds:
            self.sounds[name].set_volume(0 if self.mute_sounds else self.volume_sounds)
            self.sounds[name].play()

    def set_volume(self, *, music=None, sound=None):
        db = Database()
        if music is not None:
            self.volume_music = music
            pygame.mixer.music.set_volume(self.volume_music)
            db.set_settings({"volume_music": music})
        if sound is not None:
            self.volume_sounds = sound
            db.set_settings({"volume_sounds": sound})
        db.close()

    def mute(self, *, music=None, sound=None):
        db = Database()
        if music is not None:
            self.mute_music = music
            pygame.mixer.music.set_volume(0 if music else self.volume_music)
            db.set_settings({"mute_music": "yes" if music else "no"})
        if sound is not None:
            self.mute_sounds = sound
            db.set_settings({"mute_sounds": "yes" if sound else "no"})
        db.close()
