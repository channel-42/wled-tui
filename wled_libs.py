import json
import urllib3

#urllib Pool Manager is needed for http requests
http = urllib3.PoolManager()

class effect(object):
    def __init__(self, name=None, speed=None, intensity=None):
        self._name = name
        self._speed = speed
        self._intensity = intensity

    #properties
    @property
    def name(self):
        return self._name

    @property
    def speed(self):
        return self._speed

    @property
    def intensity(self):
        return self._intensity

    #setters
    @name.setter
    def name(self, name):
        self._name = name

    @speed.setter
    def speed(self, speed):
        if 0 <= speed <= 255:
            self._speed = speed
        elif speed > 255:
            self._speed = 255
        else:
            self._speed = 0

    @intensity.setter
    def intensity(self, intensity):
        if 0 <= intensity <= 255:
            self._intensity=intensity 
        elif intensity > 255:
                self._intensity= 255
        else:
            self._intensity= 0

class strip(object):
    def __init__(self, bri=0, rgb=[0,0,0]):
        self._brightness = bri 
        self._color = rgb
        self._effect = effect()
    
    #properties
    @property
    def brightness(self):
        return self._brightness

    @property
    def color(self):
        return self._color

    @property
    def effect(self):
        return self._effect
    
    #setters
    @brightness.setter
    def brightness(self, bri):
        if 0 <= bri <= 255:
            self._brightness = bri
        elif bri > 255:
            self._brightness = 255
        elif bri < 0:
            self._brightness = 0

        return self._brightness

    @color.setter
    def color(self, color):
        cnt = 0
        for col in color:
            if 0 <= col <= 255:
                self._color[cnt] = col  
            elif col > 255:
                self._color[cnt] = 255
            elif col < 0:
                self._color[cnt] = 0 
            cnt += 1

        return self._color 

    @effect.setter
    def effect(self, effect):
        self._effect = effect
        return self._effect

#methods only working for one segment ie [0]
class Wled(object):
    def __init__(self, ip=None):
        self.ip = ip
        #how will we store multiple strips? list of instances?
        self.strip = strip()

        self.on = None
        self.addr = f"{ip}/json/" 

        self.presets = None
        self.pallete = None
    
    def req(self, mode='GET', addr=None, data=None):
        if addr is None:
            addr = self.addr
            if mode == 'GET':
                json_raw = json.loads(
                    http.request(mode, addr).data.decode('utf-8')) 
                return dict(json_raw)
            elif mode == 'POST' or mode == 'PUT':
                http.request(mode, addr, body=data, headers={'Content-Type': 'application/json'})
                return 0
    
    def get_initial_data(self):
        data = self.req()
        self.on = data["state"]["on"]
        if self.on == True:
            self.strip.brightness = int(data["state"]["bri"])
            self.strip.color = list(data["state"]["seg"][0]["col"][0])
            self.pallete = list(data["palettes"])
            self.presets = list(data["effects"])

            # add loop to iterate over segments 
            temp_fx = data["state"]["seg"][0]["fx"]
            temp_sx = data["state"]["seg"][0]["sx"]
            temp_ix = data["state"]["seg"][0]["ix"]
            self.strip.effect = effect(self.presets[temp_fx], temp_sx, temp_ix)
    
Hub = Wled("192.168.178.195")
Hub.get_initial_data()

