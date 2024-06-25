from typing import List, Dict, Tuple

from pydantic import BaseModel


class RecordingStatsReadModel(BaseModel):
    """ List of RecordingStats object attributes"""
    datetime_clicks: List[Dict[str, int]]  # Lista de diccionarios con 'datetime' y 'num_clicks'
    total_num_clicks: int
    total_recorded_minutes: int
    total_number_of_files: int
