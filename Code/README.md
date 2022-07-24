This folder contains the pieces of code and necessary instructions on how to get started.

  - `main.py`: includes the source code to run the project
  - `display/`
    - `face_detection`: uses OpenCV to check whether there are faces in the frame.
    - `video_feed.py`: connects Droidcam feed to OpenCV and shows the live video.
  - `distance/hy_srf05.py`: Contains methods and params to test the ultrasonic distance measurement sensor.
  - `environment/dht22.py`: Contains methods and params to test the temperature and humidity sensor.
  - `sound/ky038.py`: Contains methods and params to test the sound sensor. The threshold for sound detection needs to be configured manually.

### How to run

Create a virtual environment and activate it:

```bash
python -m venv venv
. venv/bin/activate
```

Run the main code (Don't forget to set the `VIDEO_URL` var to the url Droidcam uses):

```bash
python3 main.py
```
