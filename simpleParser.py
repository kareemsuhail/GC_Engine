import sys
import re
import numpy as np
import  json


class PauseTimeAnalysis:

    def __init__(self, log_file_path):
        self.log_file_path = log_file_path
        self.pause_time_np_array = self.extract_pause_time()
        self.out  = {}
        self.out["gcDurationSummary"] = {}
        self.out["gcDurationSummary"]["groups"] = []
        self.out["gcKPI"] = {}
        self.generate_pause_time_kpis()
        self.generate_duration_summery()
        self.generate_result_file()

    def extract_pause_time(self):
        pause_time_list = []
        file = open(self.log_file_path, 'r')
        float_regex = r'\d+\.\d+'
        lines = file.readlines()
        for line in lines:
            if re.match(r', \d+\.\d+ secs]', line):
                matched = re.search(float_regex, line)
                pause_time_list.append(float(matched.group(0)))
        return np.array(pause_time_list)

    def generate_pause_time_kpis(self):

        self.out["gcKPI"]["maxPauseTime"] = float(round(self.pause_time_np_array.max() * 1000, 3))
        self.out["gcKPI"]["averagePauseTime"] = float(round(np.average(self.pause_time_np_array) * 1000, 6))
        return self.out

    def generate_duration_summery(self):
        floored_arr = np.floor(self.pause_time_np_array * 10) / 10
        categories_count = np.unique(floored_arr).size - 1
        categories_arr = np.arange(floored_arr.min() , floored_arr.max()+ .1, 0.1)
        unique, counts = np.unique(floored_arr, return_counts=True)
        duration_summery = dict(zip(unique, counts))

        for category in categories_arr:
            temp_dic = {"start":round(category,1),"end":round(category+0.1,1),"numberOfGCs":int(duration_summery[round(category,1)])}
            self.out["gcDurationSummary"]["groups"].append(temp_dic)

    def generate_result_file(self):
        print(type(self.out['gcDurationSummary']['groups'][0]["numberOfGCs"]))
        print(self.out)
        with open('result.json', 'w') as file:
            json.dump(self.out, file,indent=4,sort_keys=True)



if __name__ == '__main__':
    pause = PauseTimeAnalysis(sys.argv[1])
    pause.generate_duration_summery()
