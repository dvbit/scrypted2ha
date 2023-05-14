# scrypted2ha

A simple app to generate Homeassistant sensors starting from Scrypted Camera Devices

Requirements:
Scrypted
mqtt plugin enabled in appdaemon and scrypted

Appdaemon App Configuration:

##========================================================================================
##                                                                                      ##
##                                        scrypted2ha                                   ##
##                                                                                      ##
##========================================================================================

sensorname:
  module: scrypted2ha
  class: scrypted2ha
  prefix: scrypted
  camera: cameraname
  objects:
    - person
    - cat
    - dog
  loglevel: 3

You can list all objects recognized in/by Scrypted

Will create in Homeassistant a sensor named sensorname with state True if motion is detected and the following attributes:

Motion : True if motion is detected
Online : True if camera is online is detected
Last changed: date time of last update
Audio: True if audio is detected
Object : True if an object is detected
one attribute for each object in the app configuration : True if object is detected
