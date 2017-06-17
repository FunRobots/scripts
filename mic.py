import pyaudio

if __name__ == '__main__':
    audio = pyaudio.PyAudio()
    dev_num = audio.get_device_count()
    print('audio devices info: \n\n')
    for i in range(dev_num):
        print(i, ') ', audio.get_device_info_by_index(i), '\n')
