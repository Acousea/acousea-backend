from datetime import datetime


class RecordingStats:
    def __init__(self, epoch_time: datetime, number_of_clicks: int, recorded_minutes: int, number_of_files: int):
        self.epoch_time = epoch_time
        self.number_of_clicks = number_of_clicks
        self.recorded_minutes = recorded_minutes
        self.number_of_files = number_of_files

    def __repr__(self):
        return f"RecordingStats(epoch_time={self.epoch_time}, number_of_clicks={self.number_of_clicks}, recorded_minutes={self.recorded_minutes}, number_of_files={self.number_of_files})"
