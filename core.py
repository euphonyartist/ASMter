import os
import sys
import pygame
from pydub import AudioSegment
import numpy as np
from tkinter import Tk, filedialog, messagebox

# Function to calculate LUFS
def calculate_lufs(audio_segment):
    samples = np.array(audio_segment.get_array_of_samples())
    lufs = 10 * np.log10(np.mean(samples**2) / 0.00002**2)
    return lufs

# Function to limit audio
def limit_audio(audio_segment, threshold=-1.0):
    return audio_segment.apply_gain(threshold - audio_segment.dBFS)

# Function to process the audio file
def process_audio(file_path):
    audio = AudioSegment.from_file(file_path)
    lufs = calculate_lufs(audio)
    
    if lufs < -16:  # Example threshold
        audio = limit_audio(audio)
        output_path = os.path.splitext(file_path)[0] + "_limited.wav"
        audio.export(output_path, format="wav")
        return lufs, output_path
    return lufs, None

# Function to open a file dialog and get the audio file
def open_file():
    Tk().withdraw()  # Prevents an empty tkinter window from appearing
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav;*.mp3")])
    if file_path:
        lufs, output_path = process_audio(file_path)
        if output_path:
            messagebox.showinfo("Processing Complete", f"LUFS: {lufs:.2f}\nLimited audio saved as: {output_path}")
        else:
            messagebox.showinfo("Processing Complete", f"LUFS: {lufs:.2f}\nNo limiting applied.")

# Pygame GUI
def main():
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption("ASMR Safety Level Meter")

    # Main loop
    while True:
        screen.fill((255, 255, 255))
        font = pygame.font.Font(None, 36)
        text = font.render("Press 'O' to open audio file", True, (0, 0, 0))
        screen.blit(text, (50, 100))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_o:
                    open_file()

if __name__ == "__main__":
    main()
