from django.db import models

# for unique device id's
import uuid


class Device(models.Model):
    """
    Model representing slave device.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text="Unique ID for this device")
    info = models.CharField(max_length=200)

    def __str__(self):
        return 'Device: {0}' .format(self.info)

class Data(models.Model):
    """
    Model representing one received measurement data.
    """
    device = models.ForeignKey(Device, on_delete=models.CASCADE) # Link data to device
    collection_date = models.DateTimeField() # Date and time of data collected
    temperature = models.FloatField()
    humidity = models.IntegerField()

    def __str__(self):
        return 'Date: {0}, Temp: {1}, Device ID: ({2})' \
        .format(self.collection_date, self.temperature, self.device.info)

