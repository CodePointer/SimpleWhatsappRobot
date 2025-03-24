# -*- coding: utf-8 -*-

import os
import requests
from bs4 import BeautifulSoup
import re
import logging


GYM_URL = "https://unisasport.edu.au/citywestcourts"


class BadmintonRobot:
    def __init__(self):
        self.url = GYM_URL
        self.response = requests.get(self.url)
        self.soup = BeautifulSoup(self.response.text, 'html.parser')
        self.valid_date_range = self.get_valid_date_range()
        self.court_tables = self.get_court_tables()
        self.court_1_schedule = self.parse_timetable(self.court_tables["Court 1"]) if "Court 1" in self.court_tables else {}
        self.court_2_schedule = self.parse_timetable(self.court_tables["Court 2"]) if "Court 2" in self.court_tables else {}
        self.court_1_badminton = self.filter_badminton(self.court_1_schedule)
        self.court_2_badminton = self.filter_badminton(self.court_2_schedule)

    def get_valid_date_range(self):
        valid_text = self.soup.get_text(separator=" ", strip=True)
        match = re.search(r"Valid\s+\d{1,2}\s+\w+\s+\d{4}\s*-\s*\d{1,2}\s+\w+\s+\d{4}", valid_text)
        valid_date_range = match.group() if match else "Valid date range not found"
        logging.info(f"Valid date range: {valid_date_range}")
        return valid_date_range
    
    def get_court_tables(self):
        court_tables = {}
        courts = ["Court 1", "Court 2"]
        for court in courts:
            court_header = self.soup.find("h2", string=lambda text: text and court in text)
            if court_header:
                table = court_header.find_next("table")
                if table:
                    court_tables[court] = table
        return court_tables
    
    def parse_timetable(self, table):
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        rows = table.find_all("tr")
        schedule = {day: [] for day in days}
        for row in rows[1:]:
            columns = row.find_all("td")
            for i, col in enumerate(columns):
                activity = col.get_text(separator=" ", strip=True)
                if activity:
                    schedule[days[i]].append(activity)
        logging.info(f"Schedule: {schedule}")
        return schedule
    
    def filter_badminton(self, schedule):
        badminton_schedule = {}
        for day, activities in schedule.items():
            badminton_times = [activity for activity in activities if "Badminton" in activity]
            if badminton_times:
                badminton_schedule[day] = badminton_times
        return badminton_schedule
    
    def get_badminton_schedule(self, court_name, schedule):
        schedule_str = ""
        if schedule:
            schedule_str += f"\n🎾 {court_name} - Badminton Available:\n"
            for day, times in schedule.items():
                schedule_str += f"\n📆 {day}\n"
                for time in times:
                    schedule_str += f"⏰ {time}\n"
        return schedule_str

    def report_badminton_schedule(self):
        report_str = f"\n📅 {self.valid_date_range}\n"
        report_str += self.get_badminton_schedule("Court 1", self.court_1_badminton)
        report_str += self.get_badminton_schedule("Court 2", self.court_2_badminton)
        report_str += f"\n URL: {GYM_URL}\n"
        # logging.info(f"Report: {report_str}")
        return report_str


def generate_response():
    robot = BadmintonRobot()
    return robot.report_badminton_schedule()

