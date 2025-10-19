"""
MQTT Service for Real-time Communication
Handles MQTT connections, publishing, and subscribing
"""

import json
import logging
from typing import Callable, Dict, Any
import paho.mqtt.client as mqtt
from config.services import config

logger = logging.getLogger(__name__)

class MQTTService:
    """MQTT Service for real-time communication"""
    
    def __init__(self):
        self.client = None
        self.is_connected = False
        self.subscriptions = {}
        self.message_handlers = {}
        
    def connect(self):
        """Connect to MQTT broker"""
        try:
            self.client = mqtt.Client(client_id=config.MQTT_CLIENT_ID)
            
            # Set credentials if provided
            if config.MQTT_USERNAME and config.MQTT_PASSWORD:
                self.client.username_pw_set(config.MQTT_USERNAME, config.MQTT_PASSWORD)
            
            # Set callbacks
            self.client.on_connect = self._on_connect
            self.client.on_message = self._on_message
            self.client.on_disconnect = self._on_disconnect
            
            # For FastAPI compatibility, don't start the loop here
            # The loop will be managed by the FastAPI event loop
            # self.client.loop_start()
            
            # Try to connect synchronously
            self.client.connect(
                config.MQTT_BROKER_HOST, 
                config.MQTT_BROKER_PORT, 
                config.MQTT_KEEPALIVE
            )
            
            # Set connected flag immediately for synchronous operation
            self.is_connected = True
            logger.info("MQTT service initialized (synchronous mode for FastAPI)")
            return True
            
        except Exception as e:
            logger.error(f"Failed to connect to MQTT broker: {e}")
            raise
    
    def _on_connect(self, client, userdata, flags, rc):
        """Callback when connected to MQTT broker"""
        if rc == 0:
            self.is_connected = True
            logger.info("Connected to MQTT broker successfully")
            
            # Resubscribe to all topics
            for topic in self.subscriptions.keys():
                client.subscribe(topic)
                logger.info(f"Resubscribed to topic: {topic}")
        else:
            logger.error(f"Failed to connect to MQTT broker with code: {rc}")
    
    def _on_message(self, client, userdata, msg):
        """Callback when message is received"""
        try:
            topic = msg.topic
            payload = msg.payload.decode('utf-8')
            
            # Parse JSON payload
            data = json.loads(payload)
            
            # Call registered handlers for this topic
            if topic in self.message_handlers:
                for handler in self.message_handlers[topic]:
                    try:
                        handler(topic, data)
                    except Exception as e:
                        logger.error(f"Error in message handler for topic {topic}: {e}")
            
            logger.debug(f"Received message on {topic}: {data}")
            
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON payload received on topic {msg.topic}")
        except Exception as e:
            logger.error(f"Error processing MQTT message: {e}")
    
    def _on_disconnect(self, client, userdata, rc):
        """Callback when disconnected from MQTT broker"""
        self.is_connected = False
        if rc != 0:
            logger.warning("Unexpected disconnection from MQTT broker")
        else:
            logger.info("Disconnected from MQTT broker")
    
    def publish(self, topic: str, payload: Dict[str, Any], qos: int = 0, retain: bool = False):
        """Publish message to MQTT topic"""
        if not self.is_connected:
            logger.warning("MQTT not connected, cannot publish message")
            return False
        
        try:
            json_payload = json.dumps(payload)
            result = self.client.publish(topic, json_payload, qos, retain)
            
            if result.rc == mqtt.MQTT_ERR_SUCCESS:
                logger.debug(f"Published message to {topic}: {payload}")
                return True
            else:
                logger.error(f"Failed to publish message to {topic}: {result.rc}")
                return False
                
        except Exception as e:
            logger.error(f"Error publishing MQTT message: {e}")
            return False
    
    def subscribe(self, topic: str, handler: Callable):
        """Subscribe to MQTT topic with handler"""
        if not self.is_connected:
            logger.warning("MQTT not connected, cannot subscribe")
            return False
        
        try:
            # Subscribe to topic
            result = self.client.subscribe(topic)
            
            if result[0] == mqtt.MQTT_ERR_SUCCESS:
                # Register handler
                if topic not in self.message_handlers:
                    self.message_handlers[topic] = []
                self.message_handlers[topic].append(handler)
                
                self.subscriptions[topic] = True
                logger.info(f"Subscribed to topic: {topic}")
                return True
            else:
                logger.error(f"Failed to subscribe to topic {topic}: {result[0]}")
                return False
                
        except Exception as e:
            logger.error(f"Error subscribing to MQTT topic: {e}")
            return False
    
    def unsubscribe(self, topic: str, handler: Callable = None):
        """Unsubscribe from MQTT topic"""
        if not self.is_connected:
            return False
        
        try:
            if handler:
                # Remove specific handler
                if topic in self.message_handlers and handler in self.message_handlers[topic]:
                    self.message_handlers[topic].remove(handler)
            else:
                # Remove all handlers for topic
                if topic in self.message_handlers:
                    del self.message_handlers[topic]
            
            # Unsubscribe if no more handlers
            if topic not in self.message_handlers or not self.message_handlers[topic]:
                self.client.unsubscribe(topic)
                if topic in self.subscriptions:
                    del self.subscriptions[topic]
                logger.info(f"Unsubscribed from topic: {topic}")
            
            return True
            
        except Exception as e:
            logger.error(f"Error unsubscribing from MQTT topic: {e}")
            return False
    
    def disconnect(self):
        """Disconnect from MQTT broker"""
        if self.client:
            self.client.loop_stop()
            self.client.disconnect()
            self.is_connected = False
            logger.info("MQTT service disconnected")

# Global MQTT service instance
mqtt_service = MQTTService()

def get_mqtt_service():
    """Get global MQTT service instance"""
    return mqtt_service