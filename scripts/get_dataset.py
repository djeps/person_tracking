import sys
import signal
import argparse
import configparser
import dataset_tools as dtools

DEFAULT_DATASET = "KITTI Object Detection"
DEFAULT_OUTPUT = "~/"

class DatasetDownloader:

    def __init__(self):
        self.__parser__ = argparse.ArgumentParser(description="A dataset downloader. Downloads datasets used in ML.")
        
        self.__parser__.add_argument("-d", "--dataset", type=str, help="The name of the dataset", default=DEFAULT_DATASET)
        self.__parser__.add_argument("-o", "--output_dir", type=str, help="The output storage folder/directory", default=DEFAULT_OUTPUT)

        self.__args__ = self.__parser__.parse_args()
        
        signal.signal(signal.SIGINT, self.__signal_handler__)

    def __signal_handler__(self, signal, frame):
        print("")
        print("You pressed Ctrl+C")
        print("Exiting application...")
        sys.exit(0)


    def get_dataset(self):
        print(f"Downloading dataset       : {self.__args__.dataset}")
        print(f"Download output directory : {self.__args__.output_dir}")
        
        dtools.download(dataset=self.__args__.dataset, dst_dir=self.__args__.output_dir)
    

    def run(self):
        self.get_dataset()

        
if __name__ == "__main__":
    DatasetDownloader().run()
