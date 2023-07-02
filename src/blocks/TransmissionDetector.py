import numpy as np
import threading
import time

from .BaseBlock import BaseBlock

# Dev tools
import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('agg')


class TransmissionDetector(BaseBlock):
    def __init__(self):
        BaseBlock.__init__(self)
        self.max_power = 0

    def startSelf(self):
        print('Starting TransmissionDetector')
        self.STOP = False
        self.thread = threading.Thread(target=self.detector)
        self.thread.start()

    def stopSelf(self):
        print('Stopping TransmissionDetector')
        self.STOP = True
        self.thread.join()

    def detect(self, samples):
        plt.clf()

        freqs = np.fft.fft(samples)
        # Set ends to 0 to remove DC Spike
        width = 10
        freqs[:width] = 0
        freqs[-width:] = 0
        freqs = np.fft.fftshift(freqs)
        freqs = np.abs(freqs)
        # Smooth with rolling mean
        width = len(freqs) // 500
        w = width
        t = w // 2
        kernel = np.array([-1] * t + [1] * w + [-1] * t) / width
        freqs = np.convolve(freqs, kernel, mode='same')
        freqs[freqs < 0] = 0

        # plt.plot(freqs)
        # plt.ylim(0, 5)
        # plt.savefig('./tmp/freqs-pre.png')

        noise_floor = 1.2 * np.percentile(freqs, 99)
        # noise_floor = 4

        freqs[freqs < noise_floor] = 0

        stations = []
        start = None
        for i in range(len(freqs)):
            if start == None:
                if freqs[i] > 0:
                    start = i
            else:
                if freqs[i] == 0:
                    station_center = (start + i) // 2
                    frequency_center = len(freqs) // 2
                    frequency_offset = station_center - frequency_center
                    frequency_offset *= 24e5 / len(freqs)
                    stations.append({
                        'range': (start, i),
                        'center': (start + i) // 2,
                        'power': np.mean(freqs[start:i]),
                        'width': i - start,
                        'frequency_offset': frequency_offset,
                        'absoute_frequency': frequency_offset + 123.85e6,
                    })
                    start = None
        
        plt.clf()
        plt.plot(freqs)
        plt.savefig('./tmp/freqs-post.png')
        
        return stations


        if len(stations) == 0:
            print('.', end='', flush=True)
            return
        print('---')
        print(f'Found {len(stations)} stations')
        for station in stations:
            print(f'    {station["center"]:5}, {station["power"]:.2f}, {station["width"]}, {station["frequency_offset"] / 1e6:.2f} MHz, {station["absoute_frequency"] / 1e6:.2f} MHz')



    def detector(self):
        active_stations = set()
        station_times = {}
        total_times = {}
        while True:
            if self.STOP: return
            if len(self.buffer) == 0:
                time.sleep(0.1)
                continue
            samples = self.buffer.pop(0)
            stations = self.detect(samples)
            current_stations = set()
            for station in stations:
                f = station['absoute_frequency'] // 1e6 // 0.05 * 0.05
                current_stations.add(f)
            
            for station in active_stations.difference(current_stations):
                dt = time.time() - station_times[station]
                tot = total_times.get(station, 0) + dt
                print(f'Stopped transmitting on {station} MHz after {dt:.2f} seconds (total: {tot:.2f} seconds)')
                total_times[station] = tot
                active_stations.remove(station)
                
            
            for station in current_stations.difference(active_stations):
                print(f'Started transmitting on {station} MHz')
                active_stations.add(station)
                station_times[station] = time.time()
