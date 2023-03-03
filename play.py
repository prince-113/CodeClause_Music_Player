import os
import tkinter as tk
import tkinter.filedialog
import pygame

class MusicPlayer:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.playlist = []
        self.current_track = 0
        self.paused = False

    def add_track(self, track_path):
        self.playlist.append(track_path)

    def play(self):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(self.playlist[self.current_track])
            pygame.mixer.music.play()
        else:
            self.paused = False
            pygame.mixer.music.unpause()

    def pause(self):
        pygame.mixer.music.pause()
        self.paused = True

    def stop(self):
        pygame.mixer.music.stop()

    def next_track(self):
        self.current_track = (self.current_track + 1) % len(self.playlist)
        self.play()

    def previous_track(self):
        self.current_track = (self.current_track - 1) % len(self.playlist)
        self.play()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(volume)

class MusicPlayerGUI:
    def __init__(self):
        self.player = MusicPlayer()
        self.root = tk.Tk()
        self.root.title("Music Player")
        self.create_widgets()

    def create_widgets(self):
        # Create the menu bar
        menubar = tk.Menu(self.root)

        # Create the file menu
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_file)
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)

        # Create the playback menu
        playbackmenu = tk.Menu(menubar, tearoff=0)
        playbackmenu.add_command(label="Play", command=self.player.play)
        playbackmenu.add_command(label="Pause", command=self.player.pause)
        playbackmenu.add_command(label="Stop", command=self.player.stop)
        playbackmenu.add_separator()
        playbackmenu.add_command(label="Next track", command=self.player.next_track)
        playbackmenu.add_command(label="Previous track", command=self.player.previous_track)
        menubar.add_cascade(label="Playback", menu=playbackmenu)

        # Create the volume slider
        self.volume_slider = tk.Scale(self.root, from_=0, to=1, resolution=0.01, orient=tk.HORIZONTAL, command=self.set_volume)
        self.volume_slider.set(0.5)

        # Create the track label
        self.track_label = tk.Label(self.root, text="No track selected")

        # Add the widgets to the window
        self.root.config(menu=menubar)
        self.volume_slider.pack()
        self.track_label.pack()

    def open_file(self):
        filetypes = [("MP3 files", "*.mp3")]
        filename = tkinter.filedialog.askopenfilename(title="Select a file", filetypes=filetypes)
        if filename:
            self.player.add_track(filename)
            self.track_label.config(text=os.path.basename(filename))
            self.player.play()

    def set_volume(self, volume):
        self.player.set_volume(float(volume))

    def run(self):
        self.root.mainloop()

player = MusicPlayerGUI()
player.run()
