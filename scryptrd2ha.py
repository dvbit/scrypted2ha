#
# scrypted2ha 
#
# V1
# TODO: Add other attributes
#       Add Snabshot Function
#
# Add a Sensor representing a scrypted camera 
# gets data from scrypted via mqtt
# requires mqtt plugin installed in scrypted 
# requires mqtt plugin installed in appdaemon 
#  
#
# Sample config section for apps.yaml:
#camera1:
#  module: scrypted2ha
#  class: scrypted2ha
#  prefix: prefix
#  camera: camera
#  objects:
#   - person
#   - car
#   - cat
# creates a sensor in HA with
#
# state : true if motion is detected
# attributes:
# personnumner: number of persons detected
# person
# confidencep
# box_xmin
# box_ymin
# box_xmax
# box_ymax
# car
# confidence
# box_xmin
# box_ymin
# box_xmax
# box_ymax
# cat
# box_xmin
# box_ymin
# box_xmax
# box_ymax


# TODO: better input check on entities, translate userid to friendly name of user

import hassapi as hass
import json
import mqttapi as mqtt
from datetime import datetime, timedelta

MQTT_MSG="MQTT_MESSAGE"

class scrypted2ha(hass.Hass):
  def initialize(self):
    """Read parameters."""
    try:
        self.loglevel = self.args.get("loglevel",3)
    except:
      self.log("Error opening parameters!")
      return
    self.mylog("*************************",0) 
    self.mylog("Initializing scrypted2ha.",0) 
    self.mylog("*************************",0) 
    self.mylog("Log Level: {}".format(self.loglevel),0)
    try:
      self.prefix = self.args.get("prefix")
      self.camera = self.args.get("camera")
      self.objects = list(self.args["objects"])
    except:
      self.log("Error opening parameters")
      return
    
    self.mylog("*************************",0) 
    self.mylog("Prefix: {}.".format(self.prefix),3)
    self.mylog("Camera: {}.".format(self.camera),3)
    self.mylog("Objects to report: ".format(self.prefix),3)
    for object in self.objects:
      self.mylog("Object: {}".format(object),3)
    self.mylog("Sensors Created: sensor.scrycam_{}".format(self.name ),3)

    """Set topic Listener"""
#    self.set_namespace('mqtt') 
    self.listen_event(self.on_online, event=MQTT_MSG, namespace = 'mqtt', topic=self.prefix+"/"+self.camera+"/online")
    self.listen_event(self.on_motion, event=MQTT_MSG, namespace = 'mqtt', topic=self.prefix+"/"+self.camera+"/motionDetected")
    self.listen_event(self.on_audio, event=MQTT_MSG, namespace = 'mqtt', topic=self.prefix+"/"+self.camera+"/audioDetected")
    self.listen_event(self.on_objectdetect, event=MQTT_MSG, namespace = 'mqtt', topic=self.prefix+"/"+self.camera+"/ObjectDetector")
    self.set_state(
        entity_id = "sensor.scrycam_"+self.name, 
        attributes = { 
            "device_class": None,
            "entity_id": "sensor.scrycam_"+self.name,
            "friendly_name": self.name,
            "object": False, 
            "last_changed": self.datetime().replace(microsecond=0).isoformat()
        }
    )      
    self.mylog("*************************",0) 
    self.mylog("scrypted2ha for camera {} initialized and listeing to events {}".format(self.camera,self.prefix+"/"+self.camera+"/motionDetected"),1)
    
  def on_online(self, event_name, data, kwargs):
      """Update the sensor based on payload"""
      self.mylog("*************************",3) 
      self.mylog("online detected: mqtt load {}".format(data),3) 
      self.mylog("setting {} to {}".format("sensor.scrycam_"+self.name,json.loads(data['payload']) ),3) 
      self.set_state(
          entity_id = "sensor.scrycam_"+self.name, 
          attributes = { 
              "device_class": None,
              "entity_id": "sensor.scrycam_"+self.name,
              "friendly_name": self.name,
              "online": json.loads(data['payload']), 
              "last_changed": self.datetime().replace(microsecond=0).isoformat()
          }
      )
      for detection in payload['detections']:
        #self.mylog("detected {}".format(detection['className']) ,3) 
        if detection['className'] in self.objects:
          self.set_state(
              entity_id = "sensor.scrycam_"+self.name, 
              attributes = { 
                  "device_class": None,
                  "entity_id": "sensor.scrycam_"+self.name,
                  "friendly_name": self.name,
                  detection['className'] : True,
                  "last_changed": self.datetime().replace(microsecond=0).isoformat()
              }
          )
    
  def on_motion(self, event_name, data, kwargs):
      """Update the sensor based on payload"""
      self.mylog("*************************",3) 
      self.mylog("motion detected: mqtt load {}".format(data),3) 
      self.mylog("setting {} to {}".format("sensor.scrycam_"+self.name,json.loads(data['payload']) ),3) 
      self.set_state(
          entity_id = "sensor.scrycam_"+self.name, 
          state=json.loads(data['payload']),
          attributes = { 
              "device_class": None,
              "entity_id": "sensor.scrycam_"+self.name,
              "friendly_name": self.name,
              "motion": json.loads(data['payload']), 
              "last_changed": self.datetime().replace(microsecond=0).isoformat()
          }
      )
      
  def on_audio(self, event_name, data, kwargs):
      """Update the sensor based on payload"""
      self.mylog("*************************",3) 
      self.mylog("audio detected: mqtt load {}".format(data),3) 
      self.mylog("setting {} to {}".format("sensor.scrycam_"+self.name,json.loads(data['payload']) ),3) 
      self.set_state(
          entity_id = "sensor.scrycam_"+self.name, 
          attributes = { 
              "device_class": None,
              "entity_id": "sensor.scrycam_"+self.name,
              "friendly_name": self.name,
              "audio": json.loads(data['payload']), 
              "last_changed": self.datetime().replace(microsecond=0).isoformat()
          }
      )      
 
  def on_objectdetect(self, event_name, data, kwargs):
      """Update the sensor based on payload"""
      self.mylog("*************************",3) 
      self.mylog("object detected: mqtt load {}".format(data),3) 
      payload=json.loads(data['payload'])
#      self.mylog("setting {} to {}".format("sensor.scrycam_"+self.name,payload['payload']) ,3) 
      if payload['detections'] == []: 
        self.set_state(
            entity_id = "sensor.scrycam_"+self.name, 
            attributes = { 
                "device_class": None,
                "entity_id": "sensor.scrycam_"+self.name,
                "friendly_name": self.name,
                "object": False, 
                "last_changed": self.datetime().replace(microsecond=0).isoformat()
            }
        )      
        for object in self.objects:
          self.set_state(
              entity_id = "sensor.scrycam_"+self.name, 
              attributes = { 
                  "device_class": None,
                  "entity_id": "sensor.scrycam_"+self.name,
                  "friendly_name": self.name,
                  object : False, 
              }
          )
      else:
        self.set_state(
            entity_id = "sensor.scrycam_"+self.name, 
            attributes = { 
                "device_class": None,
                "entity_id": "sensor.scrycam_"+self.name,
                "friendly_name": self.name,
                "object": True, 
                "last_changed": self.datetime().replace(microsecond=0).isoformat()
            }
        )      
        for detection in payload['detections']:
          #self.mylog("detected {}".format(detection['className']) ,3) 
          if detection['className'] in self.objects:
            self.set_state(
                entity_id = "sensor.scrycam_"+self.name, 
                attributes = { 
                    "device_class": None,
                    "entity_id": "sensor.scrycam_"+self.name,
                    "friendly_name": self.name,
                    detection['className'] : True,
                    "last_changed": self.datetime().replace(microsecond=0).isoformat()
                }
            )
            
 

  def mylog(self,logtxt,thislevel):
      if self.loglevel >= thislevel:
          self.log(logtxt,log="dev_log")


