import sys
import os
from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
from time import sleep
import time
from servo_control import setup_gpio_and_servo, move_servo
from stepper_control import setup_stepper_motor, rotate_stepper_motor, cleanup_stepper
import spotipy
from spotipy.oauth2 import SpotifyOAuth

# Spotify API credentials
SPOTIPY_CLIENT_ID = 'your_client_id'
SPOTIPY_CLIENT_SECRET = 'your_client_secret'
SPOTIPY_REDIRECT_URI = 'your_redirect_uri'
SPOTIPY_USERNAME = 'your_spotify_username'

def setup_spotify():
    sp_oauth = SpotifyOAuth(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET, SPOTIPY_REDIRECT_URI, scope='user-library-read user-modify-playback-state')
    token_info = sp_oauth.get_access_token(username=SPOTIPY_USERNAME)
    return spotipy.Spotify(auth=token_info['access_token'])

def main():
    servo = setup_gpio_and_servo()
    motor_params = setup_stepper_motor()
    spotify = setup_spotify()

    try:
        while True:
            reader = SimpleMFRC522()

            try:
                print("Waiting for RFID card...")
                id, text = reader.read()

                print("Card detected! Moving servo to 70 degrees.")
                move_servo(servo, 70)

                print("Rotating stepper motor continuously.")
                rotate_stepper_motor(*motor_params)

                # Get playlist URI from the RFID card data and play it on Spotify
                playlist_uri = get_playlist_uri_from_card_data(text)
                play_playlist(spotify, playlist_uri)

            except Exception as e:
                print(f"Error reading RFID card: {e}")
                print("Moving servo back to 0 degrees.")
                move_servo(servo, 0)
                # Stop the stepper motor rotation
                cleanup_stepper()
                # Stop the Spotify playback
                stop_spotify_playback(spotify)

            finally:
                sleep(2)

    except KeyboardInterrupt:
        pass

    finally:
        servo.stop()
        GPIO.cleanup()
        print("Goodbye")

def get_playlist_uri_from_card_data(card_data):
    # Implement your logic to extract the playlist URI from the card data
    # For example, you may encode the playlist URI in the card during card setup
    # or fetch it from a database.
    return card_data

def play_playlist(spotify, playlist_uri):
    # Start playing the specified playlist on Spotify
    spotify.start_playback(context_uri=playlist_uri)

def stop_spotify_playback(spotify):
    # Stop the Spotify playback
    spotify.pause_playback()

if __name__ == "__main__":
    main()
