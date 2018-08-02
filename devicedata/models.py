from django.db import models


class Device(models.Model):
    """
    Model representing slave device.
    """
    id = models.IntegerField(primary_key=True)
    info = models.CharField(max_length=100)
    user_notes = models.CharField(max_length=200, blank=True) #user can set any info to this field

    def __str__(self):
        return 'Device: {0}' .format(self.info)

class Data(models.Model):
    """
    Model representing one received measurement data.
    Values integers:
        collection_date: datetime value
        temperature: 0 - 99
        humidity: 0 - 99
        dust: 0 - 99 (not implemented)
        light: 0 - 9 (not implemented)
        voltage: 0 - 99 (not imlemented)
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE) # Link data to device
    collection_date = models.DateTimeField() # Date and time of data collected
    temperature = models.IntegerField()
    humidity = models.IntegerField()

    # TODO
    dust = models.IntegerField(null=True, blank=True)
    light = models.IntegerField(null=True, blank=True)
    voltage = models.IntegerField(null=True, blank=True)


    def __str__(self):
        return 'Date: {0}, Temp: {1}, Device ID: ({2})' \
        .format(self.collection_date, self.temperature, self.device.info)

    # Converting model in to dict for API
    def as_dict(self):
        # Charts don't use default datetime format, so we need to change it
        date = self.collection_date.strftime("%Y-%m-%dT%H:%M:%S")
        return {
            'device': self.device.id,
            'date': date,
            'temperature': self.temperature,
            'humidity': self.humidity,
        }

